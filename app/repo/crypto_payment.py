from typing import Optional, List
from uuid import UUID
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.model.crypto_payment import CryptoPayment
from app.schema.crypto_payment import CryptoPaymentCreate, CryptoPaymentUpdate

class CryptoPaymentRepository:
    """Repository for managing crypto payment records in the database."""

    def __init__(self, model_class: type[CryptoPayment], session: AsyncSession):
        self.model_class = model_class
        self.session = session

    async def get(self, id: UUID) -> Optional[CryptoPayment]:
        """Get a crypto payment by its internal database ID."""
        return await self.session.get(self.model_class, id)

    async def get_by_payment_id(self, payment_id: str) -> Optional[CryptoPayment]:
        """Get a crypto payment by its external provider payment ID."""
        statement = select(self.model_class).where(self.model_class.payment_id == payment_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_invoice_id(self, invoice_id: str) -> Optional[CryptoPayment]:
        """Get a crypto payment by its external provider invoice ID."""
        statement = select(self.model_class).where(self.model_class.invoice_id == invoice_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_user(self, user_id: int) -> List[CryptoPayment]:
        """Get all crypto payments for a specific user."""
        statement = select(self.model_class).where(self.model_class.user_id == user_id)
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def create(self, obj_in: dict) -> CryptoPayment:
        """Create a new crypto payment record."""
        db_obj = self.model_class(**obj_in)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def update(self, db_obj: CryptoPayment, obj_in: CryptoPaymentUpdate) -> CryptoPayment:
        """Update an existing crypto payment record."""
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        from datetime import datetime, timezone
        db_obj.updated_at = datetime.now(timezone.utc)

        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj
