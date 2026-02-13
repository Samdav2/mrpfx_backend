from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, Header, BackgroundTasks
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import get_session
from app.dependencies.auth import get_current_user
from app.model.user import User
from app.schema.crypto_payment import (
    CryptoPaymentRead,
    NOWPaymentsInvoiceRequest,
    NOWPaymentsPaymentRequest,
    NOWPaymentsIPNPayload,
)
from app.service.nowpayments_service import NOWPaymentsService

router = APIRouter(prefix="/crypto-payments", tags=["Crypto Payments"])


@router.get("/status")
async def get_api_status(
    session: AsyncSession = Depends(get_session),
):
    """Check NOWPayments API status"""
    service = NOWPaymentsService(session)
    return await service.get_api_status()


@router.get("/currencies")
async def get_available_currencies(
    session: AsyncSession = Depends(get_session),
):
    """Get list of available cryptocurrencies"""
    service = NOWPaymentsService(session)
    currencies = await service.get_available_currencies()
    return {"currencies": currencies}


@router.get("/min-amount")
async def get_minimum_amount(
    currency_from: str,
    currency_to: str | None = None,
    is_fixed_rate: bool = False,
    is_fee_paid_by_user: bool = False,
    session: AsyncSession = Depends(get_session),
):
    """Get minimum payment amount for currency pair"""
    service = NOWPaymentsService(session)
    return await service.get_minimum_amount(
        currency_from=currency_from,
        currency_to=currency_to,
        is_fixed_rate=is_fixed_rate,
        is_fee_paid_by_user=is_fee_paid_by_user
    )


@router.get("/estimate")
async def get_estimated_price(
    amount: float,
    currency_from: str,
    currency_to: str,
    session: AsyncSession = Depends(get_session),
):
    """Get estimated price for conversion"""
    service = NOWPaymentsService(session)
    return await service.get_estimated_price(
        amount=amount,
        currency_from=currency_from,
        currency_to=currency_to
    )


@router.post("/invoice", response_model=CryptoPaymentRead)
async def create_invoice(
    invoice_data: NOWPaymentsInvoiceRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Create a payment invoice (redirect flow)"""
    service = NOWPaymentsService(session)
    return await service.create_invoice(invoice_data, current_user.ID)


@router.post("/payment", response_model=CryptoPaymentRead)
async def create_payment(
    payment_data: NOWPaymentsPaymentRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Create a direct payment (white-label flow)"""
    service = NOWPaymentsService(session)
    return await service.create_payment(payment_data, current_user.ID)


@router.get("/payment/{payment_id}/status")
async def get_payment_status(
    payment_id: str,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Get payment status from NOWPayments API"""
    service = NOWPaymentsService(session)

    # Verify the payment belongs to the user
    crypto_payment = await service.repo.get_by_payment_id(payment_id)
    if not crypto_payment or crypto_payment.user_id != current_user.ID:
        raise HTTPException(status_code=404, detail="Payment not found")

    try:
        # Get status from API
        api_status_data = await service.get_payment_status(payment_id)
        payment_status = api_status_data.get("payment_status")

        if payment_status and payment_status != crypto_payment.payment_status:
            # Update local DB if status changed
            from app.schema.crypto_payment import CryptoPaymentUpdate
            update_data = CryptoPaymentUpdate(payment_status=payment_status)
            await service.repo.update(db_obj=crypto_payment, obj_in=update_data)

            # Trigger side effects if successful
            if payment_status in ["finished", "confirmed"]:
                background_tasks.add_task(
                    process_payment_update,
                    payment_id=crypto_payment.id,
                    payment_status=payment_status,
                    user_id=crypto_payment.user_id
                )

        return api_status_data
    except Exception as e:
        from app.core.logging_config import logger
        logger.error(f"Error polling NOWPayments status for {payment_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Backend Error: {str(e)}"
        )


@router.get("", response_model=List[CryptoPaymentRead])
async def list_user_payments(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Get all crypto payments for the current user"""
    service = NOWPaymentsService(session)
    return await service.get_user_payments(current_user.ID)


@router.get("/{payment_db_id}", response_model=CryptoPaymentRead)
async def get_payment_by_id(
    payment_db_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Get a specific crypto payment by database ID"""
    service = NOWPaymentsService(session)
    payment = await service.get_payment_by_id(payment_db_id)

    if not payment or payment.user_id != current_user.ID:
        raise HTTPException(status_code=404, detail="Payment not found")

    return payment


@router.post("/ipn-callback")
async def ipn_callback(
    request: Request,
    background_tasks: BackgroundTasks,
    x_nowpayments_sig: str = Header(None),
    session: AsyncSession = Depends(get_session),
):
    """
    IPN webhook endpoint for NOWPayments callbacks.
    This endpoint does not require authentication.
    Handles payment status updates and triggers background tasks for notifications.
    """
    from app.core.logging_config import logger

    if not x_nowpayments_sig:
        logger.error("NOWPayments IPN: Missing signature header")
        raise HTTPException(status_code=400, detail="Missing signature header")

    # Get the raw request body
    body = await request.json()
    logger.info(f"NOWPayments IPN Received. Signature: {x_nowpayments_sig}")
    logger.info(f"NOWPayments IPN Body: {body}")

    try:
        # Parse the payload
        ipn_payload = NOWPaymentsIPNPayload(**body)
        logger.info(f"NOWPayments IPN Parsed Status: {ipn_payload.payment_status}")

        # Process the callback
        service = NOWPaymentsService(session)
        updated_payment = await service.process_ipn_callback(
            payload=ipn_payload,
            signature=x_nowpayments_sig
        )

        if not updated_payment:
            logger.error(f"NOWPayments IPN: Payment not found for ID: {ipn_payload.payment_id}")
            raise HTTPException(status_code=404, detail="Payment not found")

        logger.info(f"NOWPayments IPN: Payment {updated_payment.id} updated to {updated_payment.payment_status}")

        # Add background task for notifications and additional processing
        background_tasks.add_task(
            process_payment_update,
            payment_id=updated_payment.id,
            payment_status=updated_payment.payment_status,
            user_id=updated_payment.user_id
        )

        return {"status": "ok", "payment_id": str(updated_payment.id)}

    except ValueError as e:
        logger.error(f"NOWPayments IPN Value Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"NOWPayments IPN Internal Error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


async def process_payment_update(payment_id: UUID, payment_status: str, user_id: int):
    """
    Background task to process payment updates.
    Add your business logic here for:
    - Sending email notifications
    - Updating order status
    - Triggering fulfillment
    - Updating inventory
    - Notifying admins
    """
    from app.service.email import send_email
    from app.core.config import settings
    from app.db.session import engine
    from app.model.user import User
    from sqlmodel.ext.asyncio.session import AsyncSession

    # Get user details
    async with AsyncSession(engine) as session:
        user = await session.get(User, user_id)
        if not user:
            return

        user_email = user.user_email
        user_name = user.display_name

    # Send email notification based on payment status
    if payment_status in ["finished", "confirmed"]:
        # Payment successful - send confirmation
        await send_email(
            email_to=user_email,
            subject="Payment Successful - Crypto Payment Confirmed",
            template_name="crypto_payment_success.html",
            context={
                "user_name": user_name,
                "payment_id": str(payment_id),
                "status": payment_status
            }
        )

        # Notify admin
        if settings.ADMIN_EMAIL:
            await send_email(
                email_to=settings.ADMIN_EMAIL,
                subject="New Crypto Payment Received",
                template_name="admin_crypto_payment_received.html",
                context={
                    "user_email": user_email,
                    "payment_id": str(payment_id),
                    "status": payment_status
                }
            )

    elif payment_status == "partially_paid":
        # Partially paid - notify user
        await send_email(
            email_to=user_email,
            subject="Payment Partially Received",
            template_name="crypto_payment_partial.html",
            context={
                "user_name": user_name,
                "payment_id": str(payment_id),
                "status": payment_status
            }
        )

    elif payment_status == "failed":
        # Payment failed - send notification
        await send_email(
            email_to=user_email,
            subject="Payment Failed",
            template_name="crypto_payment_failed.html",
            context={
                "user_name": user_name,
                "payment_id": str(payment_id),
                "status": payment_status
            }
        )

    # Add your additional business logic here:
    # - Update related orders
    # - Trigger product delivery
    # - Update user subscriptions
    # - Log analytics events
    # etc.

    # Update propfirm registration payment status if order_id is present
    if payment_status in ["finished", "confirmed", "failed"]:
        async with AsyncSession(engine) as session:
            from app.model.crypto_payment import CryptoPayment
            # from app.service.propfirm_registration_service import PropFirmRegistrationService
            # from app.models.propfirm_registration import AccountStatus, PaymentStatus
            # from app.schema.propfirm_registration import PropFirmRegistrationUpdate

            # Get the crypto payment to find the order_id
            crypto_payment = await session.get(CryptoPayment, payment_id)
            if crypto_payment and crypto_payment.order_id:
                # Use service to handle registration updates and notifications
                service = PropFirmRegistrationService(session)
                registration = await service.repo.get_by_order_id(crypto_payment.order_id)

                if registration:
                    # IDEMPOTENCY CHECK
                    # If already completed/in_progress, skip side effects
                    if registration.account_status != AccountStatus.pending or registration.payment_status == PaymentStatus.completed:
                        # Log this event?
                        # from app.core.logging_config import logger
                        # logger.info(f"Skipping NOWPayments side effects for {registration.id} - already processed.")
                        return

                    # Update payment status based on payment result
                    new_payment_status = PaymentStatus.completed if payment_status in ["finished", "confirmed"] else PaymentStatus.failed

                    # If payment is finished/confirmed, keep account status as pending
                    new_account_status = AccountStatus.pending if payment_status in ["finished", "confirmed"] else None

                    update_data = PropFirmRegistrationUpdate(
                        payment_status=new_payment_status,
                        account_status=new_account_status
                    )


                    # Pass background_tasks=None to force immediate email sending
                    await service.update_registration(registration.id, update_data, background_tasks=None)

                    # Process referral earnings
                    if registration.user_id:
                        user = await session.get(User, registration.user_id)
                        if user and user.referred_by:
                            from app.service.wallet_service import process_referral_purchase

                            await process_referral_purchase(
                                db=session,
                                referred_user_id=user.id,
                                referrer_code=user.referred_by,
                                pass_type=registration.pass_type,
                                purchase_amount=registration.propfirm_account_cost,
                                registration_id=registration.id
                            )

                    await session.commit()
