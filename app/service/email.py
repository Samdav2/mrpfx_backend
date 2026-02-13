"""
Email service for sending verification and password reset emails.
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import os
from jinja2 import Environment, FileSystemLoader

from app.core.config import settings


logger = logging.getLogger(__name__)

# Setup Jinja2 environment
template_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "templates")
env = Environment(loader=FileSystemLoader(template_dir))


async def send_email(
    to_email: str,
    subject: str,
    html_content: str,
    text_content: str = ""
) -> bool:
    """
    Send an email using SMTP.

    Args:
        to_email: Recipient email address
        subject: Email subject
        html_content: HTML email body
        text_content: Plain text fallback

    Returns:
        True if email sent successfully, False otherwise
    """
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        logger.warning("SMTP not configured. Email not sent to %s", to_email)
        logger.info("Email content: Subject=%s, To=%s", subject, to_email)
        return True  # Return True to not block auth flow during development

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL}>"
        msg["To"] = to_email

        # Attach both plain text and HTML versions
        if text_content:
            msg.attach(MIMEText(text_content, "plain"))
        msg.attach(MIMEText(html_content, "html"))

        # Connect and send
        if settings.SMTP_TLS:
            server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
            server.starttls()
        else:
            server = smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT)

        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(settings.SMTP_FROM_EMAIL, to_email, msg.as_string())
        server.quit()

        logger.info("Email sent successfully to %s", to_email)
        return True

    except Exception as e:
        logger.error("Failed to send email to %s: %s", to_email, str(e))
        return False


def render_template(template_name: str, **context) -> str:
    """Render a Jinja2 template."""
    template = env.get_template(template_name)
    # Add common context variables
    context["app_name"] = settings.APP_NAME
    return template.render(**context)


async def send_verification_email(email: str, code: str, username: str) -> bool:
    """
    Send email verification code to user.
    """
    subject = f"Verify your email - {settings.APP_NAME}"

    html_content = render_template(
        "email/verification.html",
        username=username,
        code=code
    )

    text_content = f"""
    Hello {username},

    Thank you for signing up! Please use the verification code below to verify your email address:

    {code}

    This code will expire in 24 hours.

    If you didn't create an account, you can safely ignore this email.
    """

    return await send_email(email, subject, html_content, text_content)


async def send_password_reset_email(email: str, token: str, username: str) -> bool:
    """
    Send password reset link to user.
    """
    reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token}&email={email}"
    subject = f"Reset your password - {settings.APP_NAME}"

    html_content = render_template(
        "email/reset_password.html",
        username=username,
        reset_link=reset_link
    )

    text_content = f"""
    Hello {username},

    We received a request to reset your password. Click the link below to create a new password:

    {reset_link}

    This link will expire in 1 hour.

    If you didn't request a password reset, you can safely ignore this email.
    """

    return await send_email(email, subject, html_content, text_content)


async def send_welcome_email(email: str, username: str) -> bool:
    """
    Send welcome email to user after verification.
    """
    subject = f"Welcome to {settings.APP_NAME}!"

    html_content = render_template(
        "email/welcome.html",
        username=username,
        dashboard_url=f"{settings.FRONTEND_URL}/dashboard"
    )

    text_content = f"""
    Welcome {username}!

    Your account has been successfully verified. We are thrilled to have you on board.

    You can now explore our courses and start learning:
    {settings.FRONTEND_URL}/dashboard
    """

    return await send_email(email, subject, html_content, text_content)


async def send_order_confirmation_email(
    email: str,
    order_id: int,
    total: float,
    currency: str,
    items: list
) -> bool:
    """
    Send order confirmation email.
    """
    subject = f"Order Confirmation #{order_id} - {settings.APP_NAME}"

    html_content = render_template(
        "email/order_confirmation.html",
        order_id=order_id,
        total=total,
        currency=currency,
        items=items
    )

    items_text = "\n".join([f"- {item}" for item in items])
    text_content = f"""
    Order Confirmed

    Thank you for your order! Here are the details:

    Order ID: #{order_id}
    Total: {total} {currency}
    Items:
    {items_text}

    We will notify you when your order status changes.
    """

    return await send_email(email, subject, html_content, text_content)


async def send_order_status_update_email(
    email: str,
    order_id: int,
    new_status: str
) -> bool:
    """
    Send order status update email.
    """
    subject = f"Order #{order_id} Update - {settings.APP_NAME}"

    html_content = render_template(
        "email/order_status.html",
        order_id=order_id,
        new_status=new_status
    )

    text_content = f"""
    Order Update

    The status of your order #{order_id} has changed to: {new_status.upper()}

    You can check the details in your dashboard.
    """

    return await send_email(email, subject, html_content, text_content)
