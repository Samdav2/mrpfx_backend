"""
Marketing plugin repository.
Handles Hustle popups and OptinPanda lead generation data.
"""
from datetime import datetime
from typing import Optional, List
from sqlmodel import Session, select, func, desc

from app.model.wordpress.marketing import (
    HustleModule, HustleModuleMeta, HustleEntry, HustleEntryMeta, HustleTracking,
    OpandaLead, OpandaLeadField, OpandaStat
)


class MarketingRepository:
    """Repository for marketing plugin data access."""

    def __init__(self, session: Session):
        self.session = session

    # =========================================================================
    # Hustle Modules (Popups, Slide-ins, Embeds)
    # =========================================================================

    async def get_modules(
        self,
        module_type: Optional[str] = None,  # "popup", "slidein", "embedded", "social_sharing"
        active_only: bool = True,
        limit: int = 100
    ) -> List[dict]:
        """Get Hustle marketing modules."""
        query = select(HustleModule)

        if module_type:
            query = query.where(HustleModule.module_type == module_type)
        if active_only:
            query = query.where(HustleModule.active == 1)

        query = query.limit(limit)
        result = self.session.exec(query).all()

        modules = []
        for module in result:
            # Get module meta
            meta = await self._get_module_meta(module.module_id)
            modules.append({
                "id": module.module_id,
                "name": module.module_name,
                "type": module.module_type,
                "mode": module.module_mode,
                "active": module.active == 1,
                "settings": meta
            })

        return modules

    async def get_module(self, module_id: int) -> Optional[dict]:
        """Get a single Hustle module with details."""
        module = self.session.get(HustleModule, module_id)
        if not module:
            return None

        meta = await self._get_module_meta(module_id)
        stats = await self.get_module_stats(module_id)

        return {
            "id": module.module_id,
            "name": module.module_name,
            "type": module.module_type,
            "mode": module.module_mode,
            "active": module.active == 1,
            "settings": meta,
            "stats": stats
        }

    async def get_module_stats(self, module_id: int) -> dict:
        """Get statistics for a Hustle module."""
        # Views
        views = self.session.exec(
            select(func.sum(HustleTracking.counter))
            .where(HustleTracking.module_id == module_id)
            .where(HustleTracking.action == "view")
        ).one() or 0

        # Conversions
        conversions = self.session.exec(
            select(func.sum(HustleTracking.counter))
            .where(HustleTracking.module_id == module_id)
            .where(HustleTracking.action == "conversion")
        ).one() or 0

        # Submissions
        submissions = self.session.exec(
            select(func.count())
            .select_from(HustleEntry)
            .where(HustleEntry.module_id == module_id)
        ).one() or 0

        conversion_rate = (conversions / views * 100) if views > 0 else 0

        return {
            "views": views,
            "conversions": conversions,
            "submissions": submissions,
            "conversion_rate": round(conversion_rate, 2)
        }

    # =========================================================================
    # Hustle Entries (Form Submissions)
    # =========================================================================

    async def get_entries(
        self,
        module_id: Optional[int] = None,
        entry_type: Optional[str] = None,  # "optin", "conversion"
        limit: int = 100,
        offset: int = 0
    ) -> List[dict]:
        """Get Hustle form entries/submissions."""
        query = select(HustleEntry)

        if module_id:
            query = query.where(HustleEntry.module_id == module_id)
        if entry_type:
            query = query.where(HustleEntry.entry_type == entry_type)

        query = query.order_by(desc(HustleEntry.date_created)).offset(offset).limit(limit)
        result = self.session.exec(query).all()

        entries = []
        for entry in result:
            meta = await self._get_entry_meta(entry.entry_id)
            entries.append({
                "id": entry.entry_id,
                "module_id": entry.module_id,
                "type": entry.entry_type,
                "date": entry.date_created,
                "data": meta
            })

        return entries

    async def get_entry(self, entry_id: int) -> Optional[dict]:
        """Get a single entry with full details."""
        entry = self.session.get(HustleEntry, entry_id)
        if not entry:
            return None

        meta = await self._get_entry_meta(entry_id)
        module = self.session.get(HustleModule, entry.module_id)

        return {
            "id": entry.entry_id,
            "module_id": entry.module_id,
            "module_name": module.module_name if module else None,
            "type": entry.entry_type,
            "date": entry.date_created,
            "data": meta
        }

    # =========================================================================
    # OptinPanda Leads
    # =========================================================================

    async def get_leads(
        self,
        confirmed_only: bool = False,
        limit: int = 100,
        offset: int = 0
    ) -> List[dict]:
        """Get OptinPanda leads."""
        query = select(OpandaLead)

        if confirmed_only:
            query = query.where(OpandaLead.lead_email_confirmed == 1)

        query = query.order_by(desc(OpandaLead.lead_date)).offset(offset).limit(limit)
        result = self.session.exec(query).all()

        leads = []
        for lead in result:
            fields = await self._get_lead_fields(lead.ID)
            leads.append({
                "id": lead.ID,
                "email": lead.lead_email,
                "name": lead.lead_name,
                "family": lead.lead_family,
                "display_name": lead.lead_display_name,
                "ip": lead.lead_ip,
                "confirmed": lead.lead_email_confirmed == 1,
                "subscribed": lead.lead_subscription_confirmed == 1,
                "post_id": lead.lead_post_id,
                "post_title": lead.lead_post_title,
                "item_id": lead.lead_item_id,
                "item_title": lead.lead_item_title,
                "referer": lead.lead_referer,
                "date": datetime.fromtimestamp(lead.lead_date) if lead.lead_date else None,
                "fields": fields
            })

        return leads

    async def get_lead(self, lead_id: int) -> Optional[dict]:
        """Get a single lead with full details."""
        lead = self.session.get(OpandaLead, lead_id)
        if not lead:
            return None

        fields = await self._get_lead_fields(lead_id)

        return {
            "id": lead.ID,
            "email": lead.lead_email,
            "name": lead.lead_name,
            "family": lead.lead_family,
            "display_name": lead.lead_display_name,
            "ip": lead.lead_ip,
            "confirmed": lead.lead_email_confirmed == 1,
            "subscribed": lead.lead_subscription_confirmed == 1,
            "post_id": lead.lead_post_id,
            "post_title": lead.lead_post_title,
            "item_id": lead.lead_item_id,
            "item_title": lead.lead_item_title,
            "referer": lead.lead_referer,
            "date": datetime.fromtimestamp(lead.lead_date) if lead.lead_date else None,
            "fields": fields
        }

    async def export_leads(
        self,
        confirmed_only: bool = False,
        format: str = "json"  # "json" or "csv"
    ) -> dict:
        """Export all leads."""
        leads = await self.get_leads(confirmed_only=confirmed_only, limit=10000)

        if format == "csv":
            # Generate CSV-friendly format
            csv_data = []
            for lead in leads:
                row = {
                    "email": lead["email"],
                    "name": lead["name"],
                    "family": lead["family"],
                    "confirmed": "Yes" if lead["confirmed"] else "No",
                    "date": str(lead["date"]) if lead["date"] else ""
                }
                # Add custom fields
                for field_name, field_value in lead.get("fields", {}).items():
                    row[field_name] = field_value
                csv_data.append(row)

            return {"format": "csv", "data": csv_data, "count": len(csv_data)}

        return {"format": "json", "data": leads, "count": len(leads)}

    # =========================================================================
    # Marketing Statistics
    # =========================================================================

    async def get_marketing_stats(self) -> dict:
        """Get overall marketing statistics."""
        # Total leads
        total_leads = self.session.exec(
            select(func.count()).select_from(OpandaLead)
        ).one() or 0

        # Confirmed leads
        confirmed_leads = self.session.exec(
            select(func.count()).select_from(OpandaLead)
            .where(OpandaLead.lead_email_confirmed == 1)
        ).one() or 0

        # Active modules
        active_modules = self.session.exec(
            select(func.count()).select_from(HustleModule)
            .where(HustleModule.active == 1)
        ).one() or 0

        # Total submissions
        total_submissions = self.session.exec(
            select(func.count()).select_from(HustleEntry)
        ).one() or 0

        # Total views
        total_views = self.session.exec(
            select(func.sum(HustleTracking.counter))
            .where(HustleTracking.action == "view")
        ).one() or 0

        # Total conversions
        total_conversions = self.session.exec(
            select(func.sum(HustleTracking.counter))
            .where(HustleTracking.action == "conversion")
        ).one() or 0

        conversion_rate = (total_conversions / total_views * 100) if total_views > 0 else 0

        return {
            "leads": {
                "total": total_leads,
                "confirmed": confirmed_leads,
                "conversion_rate": round(confirmed_leads / total_leads * 100, 2) if total_leads > 0 else 0
            },
            "modules": {
                "active": active_modules
            },
            "hustle": {
                "views": total_views,
                "conversions": total_conversions,
                "submissions": total_submissions,
                "conversion_rate": round(conversion_rate, 2)
            },
            "last_updated": datetime.now().isoformat()
        }

    async def get_conversion_stats(
        self,
        module_id: Optional[int] = None,
        days: int = 30
    ) -> List[dict]:
        """Get daily conversion statistics."""
        from datetime import timedelta

        start_date = datetime.now() - timedelta(days=days)

        query = select(
            HustleTracking.date_created,
            HustleTracking.action,
            func.sum(HustleTracking.counter).label("count")
        ).where(
            HustleTracking.date_created >= start_date
        ).group_by(
            HustleTracking.date_created,
            HustleTracking.action
        )

        if module_id:
            query = query.where(HustleTracking.module_id == module_id)

        result = self.session.exec(query).all()

        # Organize by date
        stats_by_date = {}
        for row in result:
            date_str = row.date_created.strftime("%Y-%m-%d") if row.date_created else "unknown"
            if date_str not in stats_by_date:
                stats_by_date[date_str] = {"date": date_str, "views": 0, "conversions": 0}

            if row.action == "view":
                stats_by_date[date_str]["views"] = row.count or 0
            elif row.action == "conversion":
                stats_by_date[date_str]["conversions"] = row.count or 0

        return sorted(stats_by_date.values(), key=lambda x: x["date"])

    # =========================================================================
    # Helper Methods
    # =========================================================================

    async def _get_module_meta(self, module_id: int) -> dict:
        """Get module metadata."""
        query = select(HustleModuleMeta).where(HustleModuleMeta.module_id == module_id)
        result = self.session.exec(query).all()

        return {meta.meta_key: meta.meta_value for meta in result if meta.meta_key}

    async def _get_entry_meta(self, entry_id: int) -> dict:
        """Get entry metadata."""
        query = select(HustleEntryMeta).where(HustleEntryMeta.entry_id == entry_id)
        result = self.session.exec(query).all()

        return {meta.meta_key: meta.meta_value for meta in result if meta.meta_key}

    async def _get_lead_fields(self, lead_id: int) -> dict:
        """Get lead custom fields."""
        query = select(OpandaLeadField).where(OpandaLeadField.lead_id == lead_id)
        result = self.session.exec(query).all()

        return {field.field_name: field.field_value for field in result}
