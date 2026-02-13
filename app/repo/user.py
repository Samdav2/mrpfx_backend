from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from typing import Optional

from app.model.user import User
from app.schema.user import UserCreate, UserUpdate


class UserRepository:
    """Repository for user database operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        result = await self.session.execute(
            select(User).where(User.ID == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email address."""
        result = await self.session.execute(
            select(User).where(User.user_email == email)
        )
        return result.scalars().first()

    async def get_by_login(self, login: str) -> Optional[User]:
        """Get user by username (user_login)."""
        result = await self.session.execute(
            select(User).where(User.user_login == login)
        )
        return result.scalars().first()

    async def get_by_email_or_login(self, identifier: str) -> Optional[User]:
        """Get user by email or username."""
        result = await self.session.execute(
            select(User).where(
                (User.user_email == identifier) | (User.user_login == identifier)
            )
        )
        return result.scalars().first()

    async def create(self, user_data: UserCreate) -> User:
        """Create a new user."""
        user = User(
            user_login=user_data.user_login,
            user_pass=user_data.user_pass,
            user_email=user_data.user_email,
            user_nicename=user_data.user_nicename,
            user_url=user_data.user_url,
            user_activation_key=user_data.user_activation_key,
            user_status=user_data.user_status,
            display_name=user_data.display_name or user_data.user_nicename,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update(self, user: User, update_data: UserUpdate) -> User:
        """Update user profile data."""
        update_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(user, key, value)

        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update_password(self, user: User, hashed_password: str) -> User:
        """Update user password."""
        user.user_pass = hashed_password
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def set_activation_key(self, user: User, activation_key: Optional[str]) -> User:
        """Set or clear the activation key for email verification or password reset."""
        user.user_activation_key = activation_key
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def set_status(self, user: User, status: int) -> User:
        """Update user status (0=unverified, 1=active)."""
        user.user_status = status
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def exists_by_email(self, email: str) -> bool:
        """Check if a user with the given email exists."""
        result = await self.session.execute(
            select(User.ID).where(User.user_email == email)
        )
        return result.scalars().first() is not None

    async def exists_by_login(self, login: str) -> bool:
        """Check if a user with the given username exists."""
        result = await self.session.execute(
            select(User.ID).where(User.user_login == login)
        )
        return result.scalars().first() is not None
