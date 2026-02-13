"""
Forms plugin repository.
Handles WPForms and Elementor form submissions.
"""
from datetime import datetime
from typing import Optional, List
from sqlmodel import Session, select, func, desc

from app.model.wordpress.forms import (
    WPFormsLog, WPFormsPayment, WPFormsPaymentMeta, WPFormsTaskMeta
)
from app.model.wordpress.elementor import (
    ElementorSubmission, ElementorSubmissionActionLog, ElementorSubmissionValue
)
from app.model.wordpress.core import WPPost
from app.schema.wordpress.plugins import WPFormCreate, WPFormRead, NewsletterSubscribe


from sqlmodel.ext.asyncio.session import AsyncSession

class FormsRepository:
    """Repository for form plugin data access."""

    def __init__(self, session: AsyncSession):
        self.session = session

    # =========================================================================
    # WPForms Submissions
    # =========================================================================

    async def get_wpforms_logs(
        self,
        form_id: Optional[int] = None,
        log_type: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[dict]:
        """Get WPForms activity logs."""
        query = select(WPFormsLog)

        if form_id:
            query = query.where(WPFormsLog.form_id == form_id)
        if log_type:
            query = query.where(WPFormsLog.types.contains(log_type))

        query = query.order_by(desc(WPFormsLog.create_at)).offset(offset).limit(limit)
        result = (await self.session.exec(query)).all()

        return [
            {
                "id": log.id,
                "form_id": log.form_id,
                "entry_id": log.entry_id,
                "user_id": log.user_id,
                "title": log.title,
                "message": log.message,
                "types": log.types,
                "created_at": log.create_at
            }
            for log in result
        ]

    async def get_wpforms_log(self, log_id: int) -> Optional[dict]:
        """Get a single WPForms activity log."""
        log = await self.session.get(WPFormsLog, log_id)
        if not log:
            return None

        return {
            "id": log.id,
            "form_id": log.form_id,
            "entry_id": log.entry_id,
            "user_id": log.user_id,
            "title": log.title,
            "message": log.message,
            "types": log.types,
            "created_at": log.create_at
        }

    # =========================================================================
    # WPForms Payments
    # =========================================================================

    async def get_wpforms_payments(
        self,
        form_id: Optional[int] = None,
        status: Optional[str] = None,  # "completed", "pending", "failed"
        gateway: Optional[str] = None,  # "stripe", "paypal"
        limit: int = 100,
        offset: int = 0
    ) -> List[dict]:
        """Get WPForms payment submissions."""
        query = select(WPFormsPayment)

        if form_id:
            query = query.where(WPFormsPayment.form_id == form_id)
        if status:
            query = query.where(WPFormsPayment.status == status)
        if gateway:
            query = query.where(WPFormsPayment.gateway == gateway)

        query = query.order_by(desc(WPFormsPayment.date_created_gmt)).offset(offset).limit(limit)
        result = (await self.session.exec(query)).all()

        payments = []
        for payment in result:
            meta = await self._get_payment_meta(payment.id)
            payments.append({
                "id": payment.id,
                "form_id": payment.form_id,
                "entry_id": payment.entry_id,
                "status": payment.status,
                "subtotal": float(payment.subtotal_amount),
                "discount": float(payment.discount_amount),
                "total": float(payment.total_amount),
                "currency": payment.currency,
                "gateway": payment.gateway,
                "type": payment.type,
                "mode": payment.mode,
                "transaction_id": payment.transaction_id,
                "customer_id": payment.customer_id,
                "subscription_id": payment.subscription_id,
                "subscription_status": payment.subscription_status,
                "title": payment.title,
                "created_at": payment.date_created_gmt,
                "updated_at": payment.date_updated_gmt,
                "meta": meta
            })

        return payments

    async def get_wpforms_payment(self, payment_id: int) -> Optional[dict]:
        """Get a single WPForms payment."""
        payment = await self.session.get(WPFormsPayment, payment_id)
        if not payment:
            return None

        meta = await self._get_payment_meta(payment_id)

        return {
            "id": payment.id,
            "form_id": payment.form_id,
            "entry_id": payment.entry_id,
            "status": payment.status,
            "subtotal": float(payment.subtotal_amount),
            "discount": float(payment.discount_amount),
            "total": float(payment.total_amount),
            "currency": payment.currency,
            "gateway": payment.gateway,
            "type": payment.type,
            "mode": payment.mode,
            "transaction_id": payment.transaction_id,
            "customer_id": payment.customer_id,
            "subscription_id": payment.subscription_id,
            "subscription_status": payment.subscription_status,
            "title": payment.title,
            "created_at": payment.date_created_gmt,
            "updated_at": payment.date_updated_gmt,
            "meta": meta
        }

    async def get_payment_stats(
        self,
        form_id: Optional[int] = None
    ) -> dict:
        """Get WPForms payment statistics."""
        query = select(
            WPFormsPayment.status,
            func.count().label("count"),
            func.sum(WPFormsPayment.total_amount).label("total")
        ).group_by(WPFormsPayment.status)

        if form_id:
            query = query.where(WPFormsPayment.form_id == form_id)

        result = (await self.session.exec(query)).all()

        stats = {"completed": 0, "pending": 0, "failed": 0, "total_revenue": 0}
        for row in result:
            if row.status in stats:
                stats[row.status] = row.count
            if row.status == "completed":
                stats["total_revenue"] = float(row.total) if row.total else 0

        return stats

    # =========================================================================
    # Elementor Form Submissions
    # =========================================================================

    async def get_elementor_submissions(
        self,
        form_name: Optional[str] = None,
        post_id: Optional[int] = None,
        status: Optional[str] = None,
        is_read: Optional[bool] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[dict]:
        """Get Elementor form submissions."""
        query = select(ElementorSubmission)

        if form_name:
            query = query.where(ElementorSubmission.form_name == form_name)
        if post_id:
            query = query.where(ElementorSubmission.post_id == post_id)
        if status:
            query = query.where(ElementorSubmission.status == status)
        if is_read is not None:
            query = query.where(ElementorSubmission.is_read == (1 if is_read else 0))

        query = query.order_by(desc(ElementorSubmission.created_at)).offset(offset).limit(limit)
        result = (await self.session.exec(query)).all()

        submissions = []
        for sub in result:
            values = await self._get_submission_values(sub.id)
            actions = await self._get_submission_actions(sub.id)

            submissions.append({
                "id": sub.id,
                "hash_id": sub.hash_id,
                "form_name": sub.form_name,
                "type": sub.type,
                "post_id": sub.post_id,
                "element_id": sub.element_id,
                "referer": sub.referer,
                "referer_title": sub.referer_title,
                "user_id": sub.user_id,
                "user_ip": sub.user_ip,
                "user_agent": sub.user_agent,
                "status": sub.status,
                "is_read": sub.is_read == 1,
                "actions_count": sub.actions_count,
                "actions_succeeded": sub.actions_succeeded_count,
                "created_at": sub.created_at,
                "updated_at": sub.updated_at,
                "values": values,
                "action_logs": actions
            })

        return submissions

    async def get_elementor_submission(self, submission_id: int) -> Optional[dict]:
        """Get a single Elementor form submission."""
        sub = await self.session.get(ElementorSubmission, submission_id)
        if not sub:
            return None

        values = await self._get_submission_values(submission_id)
        actions = await self._get_submission_actions(submission_id)

        return {
            "id": sub.id,
            "hash_id": sub.hash_id,
            "form_name": sub.form_name,
            "type": sub.type,
            "post_id": sub.post_id,
            "element_id": sub.element_id,
            "referer": sub.referer,
            "referer_title": sub.referer_title,
            "user_id": sub.user_id,
            "user_ip": sub.user_ip,
            "user_agent": sub.user_agent,
            "status": sub.status,
            "is_read": sub.is_read == 1,
            "actions_count": sub.actions_count,
            "actions_succeeded": sub.actions_succeeded_count,
            "created_at": sub.created_at,
            "updated_at": sub.updated_at,
            "values": values,
            "action_logs": actions
        }

    async def mark_submission_read(
        self,
        submission_id: int,
        is_read: bool = True
    ) -> bool:
        """Mark Elementor submission as read/unread."""
        sub = await self.session.get(ElementorSubmission, submission_id)
        if not sub:
            return False

        sub.is_read = 1 if is_read else 0
        sub.updated_at = datetime.now()
        self.session.add(sub)
        await self.session.commit()
        return True

    async def get_elementor_form_names(self) -> List[dict]:
        """Get list of unique Elementor form names."""
        query = select(
            ElementorSubmission.form_name,
            func.count().label("count")
        ).group_by(
            ElementorSubmission.form_name
        ).order_by(
            desc(func.count())
        )

        result = (await self.session.exec(query)).all()

        return [
            {"form_name": row.form_name, "submissions": row.count}
            for row in result
        ]

    # =========================================================================
    # Forms Statistics
    # =========================================================================

    async def get_forms_stats(self) -> dict:
        """Get overall forms statistics."""
        # Elementor submissions
        elementor_total = (await self.session.exec(
            select(func.count()).select_from(ElementorSubmission)
        )).one() or 0

        elementor_unread = (await self.session.exec(
            select(func.count()).select_from(ElementorSubmission)
            .where(ElementorSubmission.is_read == 0)
        )).one() or 0

        # WPForms payments
        wpforms_payments = (await self.session.exec(
            select(func.count()).select_from(WPFormsPayment)
        )).one() or 0

        wpforms_revenue = (await self.session.exec(
            select(func.sum(WPFormsPayment.total_amount))
            .where(WPFormsPayment.status == "completed")
        )).one() or 0

        return {
            "elementor": {
                "total_submissions": elementor_total,
                "unread": elementor_unread
            },
            "wpforms": {
                "total_payments": wpforms_payments,
                "total_revenue": float(wpforms_revenue) if wpforms_revenue else 0
            },
            "last_updated": datetime.now().isoformat()
        }

    # =========================================================================
    # Helper Methods
    # =========================================================================

    async def _get_payment_meta(self, payment_id: int) -> dict:
        """Get WPForms payment metadata."""
        query = select(WPFormsPaymentMeta).where(WPFormsPaymentMeta.payment_id == payment_id)
        result = (await self.session.exec(query)).all()

        return {meta.meta_key: meta.meta_value for meta in result if meta.meta_key}

    async def _get_submission_values(self, submission_id: int) -> dict:
        """Get Elementor submission field values."""
        query = select(ElementorSubmissionValue).where(
            ElementorSubmissionValue.submission_id == submission_id
        )
        result = (await self.session.exec(query)).all()

        return {val.key: val.value for val in result if val.key}

    async def _get_submission_actions(self, submission_id: int) -> List[dict]:
        """Get Elementor submission action logs."""
        query = select(ElementorSubmissionActionLog).where(
            ElementorSubmissionActionLog.submission_id == submission_id
        ).order_by(ElementorSubmissionActionLog.created_at)

        result = (await self.session.exec(query)).all()

        return [
            {
                "id": action.id,
                "action_name": action.action_name,
                "action_label": action.action_label,
                "status": action.status,
                "log": action.log,
                "created_at": action.created_at
            }
            for action in result
        ]

    # =========================================================================
    # WPForms Management (Admin)
    # =========================================================================

    async def create_form(self, data: WPFormCreate, user_id: int = 0) -> WPFormRead:
        """Create a new form (WPForms style)"""
        new_post = WPPost(
            post_author=user_id,
            post_title=data.title,
            post_content=data.content,
            post_status="publish",
            post_type="wpforms",
            post_date=datetime.now(),
            post_date_gmt=datetime.now(),
            post_modified=datetime.now(),
            post_modified_gmt=datetime.now()
        )
        self.session.add(new_post)
        await self.session.commit()
        await self.session.refresh(new_post)

        return WPFormRead(
            id=new_post.ID,
            title=new_post.post_title,
            date=new_post.post_date
        )

    async def get_forms(self, limit: int = 100, offset: int = 0) -> List[WPFormRead]:
        """List all forms (wpforms post type)"""
        query = select(WPPost).where(WPPost.post_type == "wpforms")
        query = query.order_by(desc(WPPost.post_date)).offset(offset).limit(limit)
        result = (await self.session.exec(query)).all()

        return [
            WPFormRead(
                id=p.ID,
                title=p.post_title,
                date=p.post_date
            )
            for p in result
        ]

    # =========================================================================
    # Newsletter Subscription (Public)
    # =========================================================================

    async def create_newsletter_log(self, data: NewsletterSubscribe) -> dict:
        """Create a log entry for newsletter subscription"""
        message = f"Newsletter signup: {data.name or 'Unknown'} ({data.email})"
        new_log = WPFormsLog(
            title="Newsletter Signup",
            message=message,
            types="subscription,optin",
            create_at=datetime.now(),
            form_id=data.form_id
        )
        self.session.add(new_log)
        await self.session.commit()
        await self.session.refresh(new_log)

        return {
            "success": True,
            "message": "Subscription successful",
            "log_id": new_log.id
        }
