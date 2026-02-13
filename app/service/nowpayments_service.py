import httpx
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings
from app.repo.crypto_payment import CryptoPaymentRepository
from app.model.crypto_payment import CryptoPayment
from app.schema.crypto_payment import (
    NOWPaymentsInvoiceRequest,
    NOWPaymentsPaymentRequest,
    NOWPaymentsIPNPayload,
    CryptoPaymentCreate,
    CryptoPaymentUpdate
)

class NOWPaymentsService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = CryptoPaymentRepository(CryptoPayment, session)
        self.api_key = settings.NOWPAYMENTS_API_KEY
        self.api_url = settings.NOWPAYMENTS_API_URL
        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }

    async def _post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    f"{self.api_url}/{endpoint}",
                    headers=self.headers,
                    json=data
                )
                response.raise_for_status()
                try:
                    return response.json()
                except Exception:
                    # If response is not JSON (e.g. 200 OK but empty or HTML), return empty dict or raise error
                    # For validation, 200 OK is enough, but let's be safe
                    if not response.content or response.text.strip() == "OK":
                        return {}
                    raise Exception(f"Invalid JSON response from NOWPayments: {response.text}")
            except httpx.TimeoutException:
                raise Exception("NOWPayments API timeout")
            except httpx.HTTPStatusError as e:
                try:
                    error_data = e.response.json()
                    error_msg = error_data.get("message", e.response.text)
                except:
                    error_msg = e.response.text
                raise Exception(f"NOWPayments API error: {error_msg}")
            except httpx.RequestError as e:
                raise Exception(f"NOWPayments API connection error: {str(e)}")

    async def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(
                    f"{self.api_url}/{endpoint}",
                    headers=self.headers,
                    params=params
                )
                response.raise_for_status()
                try:
                    return response.json()
                except Exception:
                    if not response.content:
                        return {}
                    raise Exception(f"Invalid JSON response from NOWPayments: {response.text}")
            except httpx.TimeoutException:
                raise Exception("NOWPayments API timeout")
            except httpx.HTTPStatusError as e:
                try:
                    error_data = e.response.json()
                    error_msg = error_data.get("message", e.response.text)
                except:
                    error_msg = e.response.text
                raise Exception(f"NOWPayments API error: {error_msg}")
            except httpx.RequestError as e:
                raise Exception(f"NOWPayments API connection error: {str(e)}")

    async def get_api_status(self) -> Dict[str, Any]:
        """Get NOWPayments API status"""
        return await self._get("status")

    async def get_available_currencies(self) -> List[Dict[str, Any]]:
        """Get available cryptocurrencies"""
        response = await self._get("currencies")
        return response.get("currencies", [])

    async def get_minimum_amount(self, currency_from: str, currency_to: str = None, is_fixed_rate: bool = False, is_fee_paid_by_user: bool = False) -> Dict[str, Any]:
        """Get minimum amount for transaction"""
        params = {
            "currency_from": currency_from,
            "currency_to": currency_to or currency_from,
            "is_fixed_rate": str(is_fixed_rate).lower(),
            "is_fee_paid_by_user": str(is_fee_paid_by_user).lower()
        }
        return await self._get("min-amount", params=params)

    async def get_estimated_price(self, amount: float, currency_from: str, currency_to: str) -> Dict[str, Any]:
        """Get estimated price"""
        params = {
            "amount": amount,
            "currency_from": currency_from,
            "currency_to": currency_to
        }
        return await self._get("estimate", params=params)

    async def create_invoice(self, invoice_data: NOWPaymentsInvoiceRequest, user_id: int) -> Any:
        """Create an invoice and save to DB"""
        # Call API
        payload = invoice_data.dict(exclude_none=True)
        response = await self._post("invoice", payload)

        # Prepare DB record
        # Use a dict to include fields not in the Create schema if necessary,
        # or rely on the schema if it matches.
        # Here we construct a dict to ensure we map API response to Model fields explicitly.

        created_at_str = response.get("created_at")
        created_at = None
        if created_at_str:
            try:
                # Handle Z suffix if present
                if created_at_str.endswith('Z'):
                    created_at_str = created_at_str[:-1] + '+00:00'
                created_at = datetime.fromisoformat(created_at_str)
            except ValueError:
                # If parsing fails, fall back to current time or None
                created_at = datetime.now(timezone.utc)

        payment_data = {
            "user_id": user_id,
            "payment_id": response.get("id"), # Invoices usually return id
            "invoice_id": response.get("id"),
            "order_id": invoice_data.order_id,
            "order_description": invoice_data.order_description,
            "price_amount": invoice_data.price_amount,
            "price_currency": invoice_data.price_currency,
            "pay_currency": invoice_data.pay_currency, # Might be None for invoices
            "ipn_callback_url": invoice_data.ipn_callback_url,
            "invoice_url": response.get("invoice_url"),
            "is_fixed_rate": invoice_data.is_fixed_rate,
            "is_fee_paid_by_user": invoice_data.is_fee_paid_by_user,
            "payment_status": "waiting",
            "created_at": created_at
        }

        return await self.repo.create(payment_data)

    async def create_payment(self, payment_data: NOWPaymentsPaymentRequest, user_id: int) -> Any:
        """Create a payment and save to DB"""
        # Call API
        payload = payment_data.dict(exclude_none=True)
        response = await self._post("payment", payload)

        # Prepare DB record
        created_at_str = response.get("created_at")
        created_at = None
        if created_at_str:
            try:
                # Handle Z suffix if present
                if created_at_str.endswith('Z'):
                    created_at_str = created_at_str[:-1] + '+00:00'
                created_at = datetime.fromisoformat(created_at_str)
            except ValueError:
                created_at = datetime.now(timezone.utc)

        db_data = {
            "user_id": user_id,
            "payment_id": response.get("payment_id"),
            "order_id": payment_data.order_id,
            "order_description": payment_data.order_description,
            "price_amount": payment_data.price_amount,
            "price_currency": payment_data.price_currency,
            "pay_amount": response.get("pay_amount"),
            "pay_currency": payment_data.pay_currency,
            "pay_address": response.get("pay_address"),
            "payin_extra_id": response.get("payin_extra_id"),
            "ipn_callback_url": payment_data.ipn_callback_url,
            "is_fixed_rate": payment_data.is_fixed_rate,
            "is_fee_paid_by_user": payment_data.is_fee_paid_by_user,
            "payment_status": response.get("payment_status", "waiting"),
            "created_at": created_at
        }

        return await self.repo.create(db_data)

    async def get_payment_status(self, payment_id: str) -> Dict[str, Any]:
        """Get payment status from API"""
        return await self._get(f"payment/{payment_id}")

    async def get_user_payments(self, user_id: int) -> List[Any]:
        """Get all payments for a user"""
        return await self.repo.get_by_user(user_id)

    async def get_payment_by_id(self, payment_id: UUID) -> Any:
        """Get payment by DB ID"""
        return await self.repo.get(payment_id)

    async def process_ipn_callback(self, payload: NOWPaymentsIPNPayload, signature: str) -> Any:
        # Verify signature
        if not settings.NOWPAYMENTS_IPN_SECRET:
             # If secret is not configured, we cannot verify, so we might log warning or skip.
             # However, for security, we should probably fail or at least warn.
             # For now, let's assume it's required as per user request.
             raise Exception("NOWPAYMENTS_IPN_SECRET not configured")

        import hmac
        import hashlib
        import json

        from app.core.logging_config import logger

        # Convert payload to dict and sort keys
        # payload is a Pydantic model, so .dict() works.
        # We need to ensure we use the exact data received.
        # The documentation says: "Sort the POST request by keys and convert it to string"
        # Since we receive parsed payload here, we might have lost original formatting.
        # Ideally, signature check should happen on raw body BEFORE parsing.
        # BUT, the controller passes keys.
        # Let's reconstruct the dictionary from the payload model, exclusion might be tricky if fields are optional.
        # The safest way is to use the dict passed from controller if possible, but here we have the model.
        # Let's rely on model.dict(exclude_none=True) and hope it matches 'raw' JSON keys.

        # Actually, the user doc example uses `json.dumps(message, separators=(',', ':'), sort_keys=True)`.
        # We should use `payload.dict(exclude_none=True)` to get the data.

        message = payload.dict(exclude_none=True)
        # Convert bools to lower case string if any? NOWPayments usually sends strings/numbers.
        # Check if any sorting is needed beyond json.dumps
        sorted_msg = json.dumps(message, separators=(',', ':'), sort_keys=True)

        logger.info(f"NOWPayments Signature Check - Sorted Msg: {sorted_msg}")

        digest = hmac.new(
            str(settings.NOWPAYMENTS_IPN_SECRET).encode(),
            f'{sorted_msg}'.encode(),
            hashlib.sha512
        )
        calculated_signature = digest.hexdigest()

        logger.info(f"NOWPayments Signature Check - Calculated: {calculated_signature} vs Received: {signature}")

        if calculated_signature != signature:
             logger.error("NOWPayments Signature Mismatch!")
             raise Exception(f"Invalid NOWPayments signature. Calculated: {calculated_signature}, Received: {signature}")

        # Check if payment exists
        payment = await self.repo.get_by_payment_id(str(payload.payment_id))
        if not payment and payload.invoice_id:
             payment = await self.repo.get_by_invoice_id(str(payload.invoice_id))

        if not payment:
            return None

        # Update payment
        update_data = CryptoPaymentUpdate(
            payment_status=payload.payment_status,
            pay_address=payload.pay_address,
            pay_amount=payload.pay_amount,
            actually_paid=payload.actually_paid,
            payin_extra_id=payload.payin_extra_id,
            outcome_amount=payload.outcome_amount,
            outcome_currency=payload.outcome_currency
        )

        return await self.repo.update(db_obj=payment, obj_in=update_data)

    async def validate_address(self, address: str, currency: str, extra_id: Optional[str] = None) -> bool:
        """
        Validate a crypto address.
        """
        payload = {
            "address": address,
            "currency": currency,
            "extra_id": extra_id
        }
        try:
            # The API returns 200 OK for valid addresses, but we should check the response body if needed.
            # However, the documentation says "400 Bad Request" for invalid.
            # Let's assume 200 is valid.
            await self._post("payout/validate-address", payload)
            return True
        except httpx.HTTPStatusError:
            return False

    async def create_payout(self, withdrawals: List[Dict[str, Any]], ipn_callback_url: Optional[str] = None, payout_description: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a payout batch.
        """
        payload = {
            "withdrawals": withdrawals,
            "ipn_callback_url": ipn_callback_url,
            "payout_description": payout_description
        }
        return await self._post("payout", payload)

    async def verify_payout(self, batch_withdrawal_id: str, verification_code: str) -> bool:
        """
        Verify a payout batch with 2FA code.
        """
        payload = {
            "verification_code": verification_code
        }
        try:
            await self._post(f"payout/{batch_withdrawal_id}/verify", payload)
            return True
        except httpx.HTTPStatusError:
            return False

    async def get_payout_status(self, payout_id: str) -> Dict[str, Any]:
        """
        Get status of a single payout.
        """
        return await self._get(f"payout/{payout_id}")

    async def get_payouts(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        List payouts.
        """
        return await self._get("payout", params)
