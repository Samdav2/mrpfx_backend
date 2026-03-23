from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from cryptography.fernet import Fernet
from typing import Dict, Optional
import random
import string
import base64
import hashlib
from datetime import datetime, timezone

from app.db.session import get_session
from app.core.config import settings
from app.model.user import User
from app.model.services import AccountManagementConnection, CopyTradingConnection, PropFirmRegistration
from app.dependencies.auth import get_current_active_user, get_current_admin
from app.schema.services import (
    AccountManagementConnectRequest,
    CopyTradingConnectRequest,
    PropFirmRegisterRequest,
    PropFirmRegisterResponse,
    PropFirmRegisterData,
    PropFirmRegistrationsResponse,
    PropFirmUpdateStatusRequest,
    PropFirmRegistrationAdminRead,
    PropFirmAdminRegistrationsResponse,
    AccountManagementListResponse,
    AccountManagementData,
    AccountManagementAdminListResponse,
    AccountManagementAdminRead,
    AccountManagementResponse,
    AccountManagementUpdateStatusRequest,
    CopyTradingData,
    CopyTradingResponse,
    CopyTradingListResponse,
    CopyTradingUpdateStatusRequest,
    CopyTradingAdminRead,
    CopyTradingAdminListResponse,
)
from app.service.email import (
    send_propfirm_status_update_email,
    send_admin_propfirm_status_update_notification,
    send_admin_account_mgmt_connection_notification,
    send_account_mgmt_status_update_email,
    send_copy_trading_status_update_email,
    send_admin_copy_trading_connection_notification
)
from fastapi import BackgroundTasks
from sqlmodel import select
from uuid import UUID

router = APIRouter(tags=["Services"])

# Initialize Fernet for symmetric encryption/decryption
fernet = Fernet(settings.ENCRYPTION_KEY.encode())

@router.post("/account-management/connect", status_code=status.HTTP_201_CREATED)
async def connect_account_management(
    request: AccountManagementConnectRequest,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, str]:
    """
    Connect an MT5 account to a verified manager for Account Management.
    """
    try:
        # 1. Encrypt the password securely
        encrypted_password = fernet.encrypt(request.password.encode()).decode()

        # 2. Store in Database
        new_connection = AccountManagementConnection(
            user_id=current_user.ID,
            account_id=request.accountId,
            broker=request.broker,
            password=encrypted_password,
            server=request.server,
            capital=request.capital,
            manager=request.manager,
            agreed=request.agreed
        )

        # Capture user info before commit expires the object
        user_name = current_user.display_name
        user_email = current_user.user_email

        session.add(new_connection)
        await session.commit()
        await session.refresh(new_connection)

        # 3. Notify Admin
        if settings.ADMIN_EMAIL:
            background_tasks.add_task(
                send_admin_account_mgmt_connection_notification,
                admin_email=settings.ADMIN_EMAIL,
                username=user_name,
                user_email=user_email,
                account_id=new_connection.account_id,
                capital=new_connection.capital,
                status=new_connection.status
            )

        return {
            "message": "Account connected successfully. Your information has been securely stored and is pending review.",
            "status": "pending"
        }

    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing your request: {str(e)}"
        )

@router.get("/account-management/connections", response_model=AccountManagementListResponse)
async def get_my_account_management_connections(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve all account management connections for the current user.
    """
    try:
        statement = select(AccountManagementConnection).where(
            AccountManagementConnection.user_id == current_user.ID
        ).order_by(AccountManagementConnection.created_at.desc())
        results = await session.exec(statement)
        connections = results.all()

        data = [
            AccountManagementData(
                id=c.id,
                account_id=c.account_id,
                broker=c.broker,
                server=c.server,
                capital=c.capital,
                manager=c.manager,
                status=c.status,
                created_at=c.created_at,
                updated_at=c.updated_at
            ) for c in connections
        ]

        return AccountManagementListResponse(
            success=True,
            count=len(data),
            data=data
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve connections: {str(e)}"
        )

@router.get("/admin/account-management/connections", response_model=AccountManagementAdminListResponse)
async def get_all_account_management_connections(
    session: AsyncSession = Depends(get_session),
    current_admin: User = Depends(get_current_admin),
    limit: int = 50,
    offset: int = 0
):
    """
    Get all account management connection requests (Admin only).
    """
    try:
        statement = select(AccountManagementConnection, User).join(
            User, AccountManagementConnection.user_id == User.ID
        ).order_by(AccountManagementConnection.created_at.desc()).limit(limit).offset(offset)

        results = await session.exec(statement)
        rows = results.all()

        data = []
        for c, u in rows:
            decrypted_password = c.password
            if c.password:
                try:
                    decrypted_password = fernet.decrypt(c.password.encode()).decode()
                except Exception:
                    # If decryption fails, it might be already plain or wrong key
                    pass

            data.append(
                AccountManagementAdminRead(
                    id=c.id,
                    account_id=c.account_id,
                    broker=c.broker,
                    server=c.server,
                    capital=c.capital,
                    manager=c.manager,
                    status=c.status,
                    created_at=c.created_at,
                    updated_at=c.updated_at,
                    user_name=u.display_name,
                    user_email=u.user_email,
                    password=decrypted_password
                )
            )

        return AccountManagementAdminListResponse(
            success=True,
            count=len(data),
            data=data
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve connections: {str(e)}"
        )

@router.patch("/admin/account-management/connections/{connection_id}", response_model=AccountManagementResponse)
async def update_account_management_status(
    connection_id: UUID,
    request: AccountManagementUpdateStatusRequest,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
    current_admin: User = Depends(get_current_admin),
):
    """
    Update the status of an account management connection and notify the user.
    """
    try:
        connection = await session.get(AccountManagementConnection, connection_id)
        if not connection:
            raise HTTPException(status_code=404, detail="Connection not found")

        connection.status = request.status
        connection.updated_at = datetime.now(timezone.utc)

        session.add(connection)
        await session.commit()
        await session.refresh(connection)

        # Send Email Notification to User
        user = await session.get(User, connection.user_id)
        if user:
            background_tasks.add_task(
                send_account_mgmt_status_update_email,
                email=user.user_email,
                username=user.display_name,
                account_id=connection.account_id,
                status=connection.status
            )

        return AccountManagementResponse(
            success=True,
            message="Status updated successfully",
            data=AccountManagementData(
                id=connection.id,
                account_id=connection.account_id,
                broker=connection.broker,
                server=connection.server,
                capital=connection.capital,
                manager=connection.manager,
                status=connection.status,
                created_at=connection.created_at,
                updated_at=connection.updated_at
            )
        )
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update status: {str(e)}"
        )


@router.post("/copy-trading/connect", status_code=status.HTTP_201_CREATED)
async def connect_copy_trading(
    request: CopyTradingConnectRequest,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, str]:
    """
    Connect an MT5 account for the Copy Trading service.
    """
    try:
        # 1. Encrypt the password securely
        encrypted_password = fernet.encrypt(request.password.encode()).decode()

        # 2. Store in Database
        new_connection = CopyTradingConnection(
            user_id=current_user.ID,
            account_id=request.accountId,
            password=encrypted_password,
            server=request.server
        )

        # Capture user info before commit
        user_name = current_user.display_name
        user_email = current_user.user_email

        session.add(new_connection)
        await session.commit()
        await session.refresh(new_connection)

        # 3. Notify Admin
        if settings.ADMIN_EMAIL:
            background_tasks.add_task(
                send_admin_copy_trading_connection_notification,
                admin_email=settings.ADMIN_EMAIL,
                username=user_name,
                user_email=user_email,
                account_id=new_connection.account_id,
                status=new_connection.status
            )

        return {
            "message": "Copy Trading account connected successfully. Initialization is pending.",
            "status": "pending"
        }

    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing your request: {str(e)}"
        )


@router.get("/copy-trading/connections", response_model=CopyTradingListResponse)
async def get_my_copy_trading_connections(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve all copy trading connections for the current user.
    """
    try:
        statement = select(CopyTradingConnection).where(
            CopyTradingConnection.user_id == current_user.ID
        ).order_by(CopyTradingConnection.created_at.desc())
        results = await session.exec(statement)
        connections = results.all()

        data = [
            CopyTradingData(
                id=c.id,
                account_id=c.account_id,
                server=c.server,
                status=c.status,
                created_at=c.created_at,
                updated_at=c.updated_at
            ) for c in connections
        ]

        return CopyTradingListResponse(
            success=True,
            count=len(data),
            data=data
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve connections: {str(e)}"
        )


@router.get("/admin/copy-trading/connections", response_model=CopyTradingAdminListResponse)
async def get_all_copy_trading_connections(
    session: AsyncSession = Depends(get_session),
    current_admin: User = Depends(get_current_admin),
    limit: int = 50,
    offset: int = 0
):
    """
    Get all copy trading connection requests (Admin only).
    """
    try:
        statement = select(CopyTradingConnection, User).join(
            User, CopyTradingConnection.user_id == User.ID
        ).order_by(CopyTradingConnection.created_at.desc()).limit(limit).offset(offset)

        results = await session.exec(statement)
        rows = results.all()

        data = []
        for c, u in rows:
            decrypted_password = c.password
            if c.password:
                try:
                    decrypted_password = fernet.decrypt(c.password.encode()).decode()
                except Exception:
                    pass

            data.append(
                CopyTradingAdminRead(
                    id=c.id,
                    account_id=c.account_id,
                    server=c.server,
                    status=c.status,
                    created_at=c.created_at,
                    updated_at=c.updated_at,
                    user_name=u.display_name,
                    user_email=u.user_email,
                    password=decrypted_password
                )
            )

        return CopyTradingAdminListResponse(
            success=True,
            count=len(data),
            data=data
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve connections: {str(e)}"
        )


@router.delete("/copy-trading/connections/{connection_id}", status_code=status.HTTP_200_OK)
async def disconnect_copy_trading(
    connection_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    Disconnect/Delete a copy trading connection for the current user.
    """
    try:
        connection = await session.get(CopyTradingConnection, connection_id)
        if not connection or connection.user_id != current_user.ID:
            raise HTTPException(status_code=404, detail="Connection not found")

        await session.delete(connection)
        await session.commit()

        return {"success": True, "message": "Account disconnected successfully"}
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to disconnect account: {str(e)}"
        )


@router.patch("/admin/copy-trading/connections/{connection_id}", response_model=CopyTradingResponse)
async def update_copy_trading_status(
    connection_id: UUID,
    request: CopyTradingUpdateStatusRequest,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
    current_admin: User = Depends(get_current_admin),
):
    """
    Update the status of a copy trading connection and notify the user.
    """
    try:
        connection = await session.get(CopyTradingConnection, connection_id)
        if not connection:
            raise HTTPException(status_code=404, detail="Connection not found")

        connection.status = request.status
        connection.updated_at = datetime.now(timezone.utc)

        session.add(connection)
        await session.commit()
        await session.refresh(connection)

        # Send Email Notification to User
        user = await session.get(User, connection.user_id)
        if user:
            background_tasks.add_task(
                send_copy_trading_status_update_email,
                email=user.user_email,
                username=user.display_name,
                account_id=connection.account_id,
                status=connection.status
            )

        return CopyTradingResponse(
            success=True,
            message="Status updated successfully",
            data=CopyTradingData(
                id=connection.id,
                account_id=connection.account_id,
                server=connection.server,
                status=connection.status,
                created_at=connection.created_at,
                updated_at=connection.updated_at
            )
        )
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update status: {str(e)}"
        )


@router.post("/prop-firm/register", response_model=PropFirmRegisterResponse, status_code=status.HTTP_201_CREATED)
async def register_prop_firm(
    request: PropFirmRegisterRequest,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    Register a new Prop Firm (Pass Funded Accounts) account.
    Collects trading credentials, prop firm details, and contact info.
    """
    try:
        # 1. Encrypt the password securely
        encrypted_password = fernet.encrypt(request.password.encode()).decode()

        # 2. Generate a custom order_id: FP-random_digits or similar based on user req
        # "FP-38319 (thr firs =t row owrd od the propfirm account and ramdom cosddes)"
        # We'll take the first word of propfirm_name + a random 5-digit number
        first_word = request.propfirm_name.split()[0].upper()
        random_suffix = ''.join(random.choices(string.digits, k=5))
        generated_order_id = f"{first_word}-{random_suffix}"

        # 3. Store in Database
        registration = PropFirmRegistration(
            user_id=current_user.ID,
            login_id=request.login_id,
            password=encrypted_password,
            propfirm_name=request.propfirm_name,
            propfirm_website_link=request.propfirm_website_link,
            server_name=request.server_name,
            server_type=request.server_type,
            challenges_step=request.challenges_step,
            propfirm_account_cost=request.propfirm_account_cost,
            account_size=request.account_size,
            account_phases=request.account_phases,
            trading_platform=request.trading_platform,
            propfirm_rules=request.propfirm_rules,
            whatsapp_no=request.whatsapp_no,
            telegram_username=request.telegram_username,
            payment_method=request.payment_method,
            order_id=generated_order_id
        )

        session.add(registration)
        await session.commit()
        await session.refresh(registration)

        return PropFirmRegisterResponse(
            success=True,
            message="Registration created successfully",
            data=PropFirmRegisterData(
                registration_id=str(registration.id),
                order_id=registration.order_id,
                login_id=registration.login_id,
                propfirm_name=registration.propfirm_name,
                propfirm_website_link=registration.propfirm_website_link,
                server_name=registration.server_name,
                server_type=registration.server_type,
                challenges_step=registration.challenges_step,
                propfirm_account_cost=registration.propfirm_account_cost,
                account_size=registration.account_size,
                account_phases=registration.account_phases,
                trading_platform=registration.trading_platform,
                propfirm_rules=registration.propfirm_rules,
                whatsapp_no=registration.whatsapp_no,
                telegram_username=registration.telegram_username,
                payment_method=registration.payment_method,
                status=registration.status,
                payment_status=registration.payment_status,
                created_at=registration.created_at,
                updated_at=registration.updated_at
            )
        )

    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "message": f"Registration failed: {str(e)}"
            }
        )

@router.get("/prop-firm/registrations", response_model=PropFirmRegistrationsResponse)
async def get_prop_firm_registrations(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
    limit: int = 20,
    offset: int = 0
):
    """
    Retrieve a list of all Prop Firm registrations for the current user.
    """
    try:
        statement = select(PropFirmRegistration).where(
            PropFirmRegistration.user_id == current_user.ID
        ).limit(limit).offset(offset)
        results = await session.exec(statement)
        registrations = results.all()

        data = [
            PropFirmRegisterData(
                registration_id=str(r.id),
                order_id=r.order_id,
                login_id=r.login_id,
                propfirm_name=r.propfirm_name,
                propfirm_website_link=r.propfirm_website_link,
                server_name=r.server_name,
                server_type=r.server_type,
                challenges_step=r.challenges_step,
                propfirm_account_cost=r.propfirm_account_cost,
                account_size=r.account_size,
                account_phases=r.account_phases,
                trading_platform=r.trading_platform,
                propfirm_rules=r.propfirm_rules,
                whatsapp_no=r.whatsapp_no,
                telegram_username=r.telegram_username,
                payment_method=r.payment_method,
                status=r.status,
                payment_status=r.payment_status,
                created_at=r.created_at,
                updated_at=r.updated_at
            ) for r in registrations
        ]

        return PropFirmRegistrationsResponse(
            success=True,
            count=len(data),
            data=data
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve registrations: {str(e)}"
        )

@router.get("/prop-firm/registrations/{registration_id}", response_model=PropFirmRegisterResponse)
@router.get("/prop-firm/account/{registration_id}", response_model=PropFirmRegisterResponse)
async def get_prop_firm_registration(
    registration_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve a specific Prop Firm registration by ID for the current user.
    """
    try:
        registration = await session.get(PropFirmRegistration, registration_id)
        if not registration or registration.user_id != current_user.ID:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Registration with ID {registration_id} not found"
            )

        return PropFirmRegisterResponse(
            success=True,
            message="Registration found",
            data=PropFirmRegisterData(
                registration_id=str(registration.id),
                order_id=registration.order_id,
                login_id=registration.login_id,
                propfirm_name=registration.propfirm_name,
                propfirm_website_link=registration.propfirm_website_link,
                server_name=registration.server_name,
                server_type=registration.server_type,
                challenges_step=registration.challenges_step,
                propfirm_account_cost=registration.propfirm_account_cost,
                account_size=registration.account_size,
                account_phases=registration.account_phases,
                trading_platform=registration.trading_platform,
                propfirm_rules=registration.propfirm_rules,
                whatsapp_no=registration.whatsapp_no,
                telegram_username=registration.telegram_username,
                payment_method=registration.payment_method,
                status=registration.status,
                payment_status=registration.payment_status,
                created_at=registration.created_at,
                updated_at=registration.updated_at
            )
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )

@router.patch("/admin/prop-firm/registrations/{registration_id}", response_model=PropFirmRegisterResponse)
async def update_prop_firm_status(
    registration_id: int,
    request: PropFirmUpdateStatusRequest,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
    current_admin: User = Depends(get_current_admin),
):
    """
    Update the status and/or payment status of a Prop Firm registration.
    (Admin only in production - currently open for development)
    """
    try:
        registration = await session.get(PropFirmRegistration, registration_id)
        if not registration:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Registration with ID {registration_id} not found"
            )

        updated = False
        if request.status is not None:
            registration.status = request.status
            updated = True
        if request.payment_status is not None:
            registration.payment_status = request.payment_status
            updated = True

        if updated:
            registration.updated_at = datetime.now(timezone.utc)
            session.add(registration)
            await session.commit()
            await session.refresh(registration)

            # Send Email Notifications
            if request.status is not None:
                # Fetch user details
                user = await session.get(User, registration.user_id)
                if user:
                    # Notify User
                    background_tasks.add_task(
                        send_propfirm_status_update_email,
                        email=user.user_email,
                        username=user.display_name,
                        order_id=registration.order_id,
                        status=registration.status
                    )

                    # Notify Admin
                    if settings.ADMIN_EMAIL:
                        background_tasks.add_task(
                            send_admin_propfirm_status_update_notification,
                            admin_email=settings.ADMIN_EMAIL,
                            username=user.display_name,
                            user_email=user.user_email,
                            order_id=registration.order_id,
                            status=registration.status
                        )

        return PropFirmRegisterResponse(
            success=True,
            message="Registration updated successfully",
            data=PropFirmRegisterData(
                registration_id=str(registration.id),
                order_id=registration.order_id,
                login_id=registration.login_id,
                propfirm_name=registration.propfirm_name,
                propfirm_website_link=registration.propfirm_website_link,
                server_name=registration.server_name,
                server_type=registration.server_type,
                challenges_step=registration.challenges_step,
                propfirm_account_cost=registration.propfirm_account_cost,
                account_size=registration.account_size,
                account_phases=registration.account_phases,
                trading_platform=registration.trading_platform,
                propfirm_rules=registration.propfirm_rules,
                whatsapp_no=registration.whatsapp_no,
                telegram_username=registration.telegram_username,
                payment_method=registration.payment_method,
                status=registration.status,
                payment_status=registration.payment_status,
                created_at=registration.created_at,
                updated_at=registration.updated_at
            )
        )
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update registration: {str(e)}"
        )

@router.get("/admin/prop-firm/registrations", response_model=PropFirmAdminRegistrationsResponse)
async def get_all_prop_firm_registrations(
    session: AsyncSession = Depends(get_session),
    current_admin: User = Depends(get_current_admin),
    limit: int = 50,
    offset: int = 0
):
    """
    Retrieve ALL Prop Firm registrations in the system with user details (Admin only).
    """
    try:
        statement = select(PropFirmRegistration, User).join(
            User, PropFirmRegistration.user_id == User.ID
        ).limit(limit).offset(offset)
        results = await session.exec(statement)
        registrations_with_users = results.all()

        data = []
        for r, u in registrations_with_users:
            decrypted_password = r.password
            if r.password:
                try:
                    decrypted_password = fernet.decrypt(r.password.encode()).decode()
                except Exception:
                    pass

            data.append(
                PropFirmRegistrationAdminRead(
                    registration_id=str(r.id),
                    order_id=r.order_id,
                    login_id=r.login_id,
                    password=decrypted_password,
                    propfirm_name=r.propfirm_name,
                    propfirm_website_link=r.propfirm_website_link,
                    server_name=r.server_name,
                    server_type=r.server_type,
                    challenges_step=r.challenges_step,
                    propfirm_account_cost=r.propfirm_account_cost,
                    account_size=r.account_size,
                    account_phases=r.account_phases,
                    trading_platform=r.trading_platform,
                    propfirm_rules=r.propfirm_rules,
                    whatsapp_no=r.whatsapp_no,
                    telegram_username=r.telegram_username,
                    payment_method=r.payment_method,
                    status=r.status,
                    payment_status=r.payment_status,
                    created_at=r.created_at,
                    updated_at=r.updated_at,
                    user_name=u.display_name,
                    user_email=u.user_email
                )
            )

        return PropFirmAdminRegistrationsResponse(
            success=True,
            count=len(data),
            data=data
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve registrations: {str(e)}"
        )
