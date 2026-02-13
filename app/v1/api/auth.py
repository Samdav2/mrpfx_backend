"""
Authentication API endpoints.
"""
from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import get_session
from app.service.auth import AuthService
from app.service.email import send_welcome_email
from app.schema.auth import (
    SignupRequest,
    LoginRequest,
    TokenResponse,
    VerifyEmailRequest,
    ResendVerificationRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    RefreshTokenRequest,
    MessageResponse,
)
from app.schema.user import UserResponse, ChangePasswordRequest
from app.dependencies.auth import get_current_active_user, get_current_user
from app.model.user import User


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/signup",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user"
)
async def signup(
    request: SignupRequest,
    session: AsyncSession = Depends(get_session)
):
    """
    Register a new user account.

    - Validates email and username uniqueness
    - Hashes password with bcrypt (WordPress 6.8+ compatible)
    - Sends verification email with 6-digit code
    """
    auth_service = AuthService(session)
    user, _ = await auth_service.signup(request)

    return MessageResponse(
        message=f"Account created successfully. Please check your email ({user.user_email}) for verification code.",
        success=True
    )


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="User login"
)
async def login(
    request: LoginRequest,
    session: AsyncSession = Depends(get_session)
):
    """
    Authenticate user and return JWT tokens.

    - Accepts email or username for login
    - Supports both WordPress phpass and bcrypt password hashes
    - Returns access token and refresh token
    """
    auth_service = AuthService(session)
    return await auth_service.login(request)


@router.post(
    "/admin/login",
    response_model=TokenResponse,
    summary="Admin login"
)
async def admin_login(
    request: LoginRequest,
    session: AsyncSession = Depends(get_session)
):
    """
    Authenticate admin user and return JWT tokens.

    - Accepts email or username for login
    - Checks if user status is 1 (Admin)
    - Returns access token and refresh token
    """
    auth_service = AuthService(session)
    return await auth_service.admin_login(request)


@router.post(
    "/verify-email",
    response_model=MessageResponse,
    summary="Verify email address"
)
async def verify_email(
    request: VerifyEmailRequest,
    session: AsyncSession = Depends(get_session)
):
    """
    Verify user email with 6-digit code.

    - Code is sent via email during signup
    - Activates the user account upon successful verification
    """
    auth_service = AuthService(session)
    user = await auth_service.verify_email(request.email, request.code)

    # Send welcome email
    if user:
        await send_welcome_email(user.user_email, user.display_name or user.user_login)

    return MessageResponse(
        message="Email verified successfully. You can now log in.",
        success=True
    )


@router.post(
    "/resend-verification",
    response_model=MessageResponse,
    summary="Resend verification email"
)
async def resend_verification(
    request: ResendVerificationRequest,
    session: AsyncSession = Depends(get_session)
):
    """
    Resend email verification code.

    - Generates a new 6-digit code
    - Sends new verification email
    """
    auth_service = AuthService(session)
    await auth_service.resend_verification(request.email)

    return MessageResponse(
        message="Verification email sent. Please check your inbox.",
        success=True
    )


@router.post(
    "/forgot-password",
    response_model=MessageResponse,
    summary="Request password reset"
)
async def forgot_password(
    request: ForgotPasswordRequest,
    session: AsyncSession = Depends(get_session)
):
    """
    Request password reset link.

    - Sends password reset link to email
    - Always returns success to prevent email enumeration
    """
    auth_service = AuthService(session)
    await auth_service.forgot_password(request.email)

    return MessageResponse(
        message="If an account exists with this email, you will receive a password reset link.",
        success=True
    )


@router.post(
    "/reset-password",
    response_model=MessageResponse,
    summary="Reset password with token"
)
async def reset_password(
    request: ResetPasswordRequest,
    session: AsyncSession = Depends(get_session)
):
    """
    Reset password using token from email.

    - Validates reset token
    - Updates password with bcrypt hash
    """
    auth_service = AuthService(session)
    await auth_service.reset_password(request.email, request.token, request.new_password)

    return MessageResponse(
        message="Password reset successfully. You can now log in with your new password.",
        success=True
    )


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh access token"
)
async def refresh_token(
    request: RefreshTokenRequest,
    session: AsyncSession = Depends(get_session)
):
    """
    Get new access token using refresh token.

    - Validates refresh token
    - Returns new access and refresh tokens
    """
    auth_service = AuthService(session)
    return await auth_service.refresh_token(request.refresh_token)


@router.post(
    "/change-password",
    response_model=MessageResponse,
    summary="Change password"
)
async def change_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Change password for authenticated user.

    - Requires current password for verification
    - Updates to new bcrypt-hashed password
    """
    auth_service = AuthService(session)
    await auth_service.change_password(
        current_user,
        request.current_password,
        request.new_password
    )

    return MessageResponse(
        message="Password changed successfully.",
        success=True
    )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user"
)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current authenticated user's profile.
    """
    return current_user
