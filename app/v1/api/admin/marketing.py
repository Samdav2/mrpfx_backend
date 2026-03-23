from typing import List, Optional
import os
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from pydantic import BaseModel

from datetime import datetime
from app.db.session import engine
from app.service.email import send_email, render_template
from app.model.wordpress.core import WPUser
from app.model.services import PropFirmRegistration, AccountManagementConnection
from app.dependencies.auth import get_current_user
from app.model.user import User
from app.core.config import settings

router = APIRouter()

class EmailTemplate(BaseModel):
    id: str
    name: str
    subject: str
    body: str

class SendEmailPayload(BaseModel):
    targetOption: str # 'all' or 'specific'
    userIds: List[int]
    templateId: str
    subject: str
    message: str

@router.get("/templates", response_model=List[EmailTemplate])
async def get_templates(current_user: User = Depends(get_current_user)):
    """Get available email templates from the filesystem (metadata only)."""
    app_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    template_dir = os.path.join(app_dir, "templates", "email")
    templates = []

    if os.path.exists(template_dir):
        # Always provide a generic Marketing template first
        templates.append(EmailTemplate(
            id="marketing.html",
            name="Standard Marketing",
            subject="Personalized update for you",
            body="" # We keep the body empty so the editor stays clean
        ))

        for filename in os.listdir(template_dir):
            if filename.endswith(".html") and filename not in ["base.html", "marketing.html"]:
                name = filename.replace(".html", "").replace("_", " ").title()
                templates.append(EmailTemplate(
                    id=filename,
                    name=name,
                    subject=name,
                    body="" # Do not return HTML source code as the content
                ))

    return templates

async def process_email_campaign(payload: SendEmailPayload):
    """Process email campaign in background with a dedicated session from the primary engine."""
    try:
        async with AsyncSession(engine) as session:
            # Fetch users from primary database (where WP data is synced/imported)
            if payload.targetOption == 'all':
                statement = select(WPUser)
            else:
                statement = select(WPUser).where(WPUser.ID.in_(payload.userIds))

            result = await session.exec(statement)
            users = result.all()

            for user in users:
                if user.user_email:
                    # Fetch latest Prop Firm Account for this user if it exists
                    prop_stmt = select(PropFirmRegistration).where(PropFirmRegistration.user_id == user.ID).order_by(PropFirmRegistration.created_at.desc())
                    prop_res = await session.exec(prop_stmt)
                    prop = prop_res.first()

                    # Fetch latest Account Management Connection
                    am_stmt = select(AccountManagementConnection).where(AccountManagementConnection.user_id == user.ID).order_by(AccountManagementConnection.created_at.desc())
                    am_res = await session.exec(am_stmt)
                    am = am_res.first()

                    full_name = user.display_name or user.user_login

                    # Common context for all templates
                    context = {
                        "username": full_name,
                        "user_email": user.user_email,
                        "login_id": prop.login_id if prop else (am.account_id if am else "N/A"),
                        "platform": prop.trading_platform if prop else "Metatrader 5",
                        "account_id": am.account_id if am else (prop.login_id if prop else "N/A"),
                        "status": prop.status if prop else (am.status if am else "active"),
                        "dashboard_url": f"{settings.FRONTEND_URL}/dashboard",
                        "current_year": datetime.now().year,
                        "app_name": settings.APP_NAME,
                    }

                    # Prepare message by replacing user-specific placeholders in the CUSTOM text
                    processed_message = payload.message.replace("{{ username }}", full_name)
                    processed_message = processed_message.replace("{{ user_email }}", user.user_email)
                    processed_message = processed_message.replace("{{ login_id }}", str(context["login_id"]))
                    processed_message = processed_message.replace("{{ platform }}", str(context["platform"]))

                    # Add processed message to context for the template wrapper
                    context["message"] = processed_message

                    # Render with the selected template
                    template_path = f"email/{payload.templateId}"
                    html_body = render_template(template_path, **context)

                    # Send email using existing service
                    await send_email(
                        to_email=user.user_email,
                        subject=payload.subject,
                        html_content=html_body
                    )
    except Exception as e:
        print(f"Error in background email campaign: {e}")

@router.post("/send-email")
async def send_email_campaign(
    payload: SendEmailPayload,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user)
):
    """Initiate an email campaign as a background task."""
    background_tasks.add_task(process_email_campaign, payload)
    return {"status": "success", "message": "Email campaign successfully initiated in the background"}
