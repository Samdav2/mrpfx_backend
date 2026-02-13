from typing import Optional, List
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.model.wordpress.core import WPUser
from app.schema.wordpress.user import WPUserCreate, WPUserUpdate

class WPUserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> Optional[WPUser]:
        result = await self.session.exec(select(WPUser).where(WPUser.ID == user_id))
        return result.first()

    async def get_by_email(self, email: str) -> Optional[WPUser]:
        result = await self.session.exec(select(WPUser).where(WPUser.user_email == email))
        return result.first()

    async def get_by_login(self, login: str) -> Optional[WPUser]:
        result = await self.session.exec(select(WPUser).where(WPUser.user_login == login))
        return result.first()

    async def create(self, user_data: WPUserCreate) -> WPUser:
        db_user = WPUser.model_validate(user_data)
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user

    async def update(self, user: WPUser, user_data: WPUserUpdate) -> WPUser:
        update_data = user_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_all(self, skip: int = 0, limit: int = 10) -> List[WPUser]:
        result = await self.session.exec(select(WPUser).offset(skip).limit(limit))
        return result.all()

    async def delete(self, user_id: int) -> bool:
        """Delete a user"""
        user = await self.get_by_id(user_id)
        if not user:
            return False

        # In a real WP environment, we should reassign posts, etc.
        # For now, we'll just delete the user record and let cascading handle (or not)
        await self.session.delete(user)
        await self.session.commit()
        return True

    async def get_roles(self, user_id: int) -> List[str]:
        """Get user roles from usermeta"""
        from app.model.wordpress.core import WPUserMeta
        import phpserialize

        stmt = select(WPUserMeta).where(
            WPUserMeta.user_id == user_id,
            WPUserMeta.meta_key == "wp_capabilities"  # Prefix might vary if table prefix isn't standard, but typically wp_capabilities
            # database prefix is 8jH_, so keys usually stick to wp_ unless explicitly changed in config
            # However, WP typically stores it as {prefix}_capabilities.
            # Given table is 8jH_usermeta, let's try to find the capability key dynamically or assume standard
        )
        # Actually, let's search for the capability key
        stmt = select(WPUserMeta).where(
             WPUserMeta.user_id == user_id,
             WPUserMeta.meta_key.like("%capabilities")
        )
        result = await self.session.exec(stmt)
        meta = result.first()

        if not meta or not meta.meta_value:
            return []

        try:
            # Deserialization using phpserialize for accuracy
            data = phpserialize.loads(meta.meta_value.encode('utf-8'))
            if isinstance(data, dict):
                # WP format is {rolename: True, ...}
                # phpserialize returns bytes for keys
                return [k.decode('utf-8') for k, v in data.items() if v]
            return []
        except Exception as e:
            print(f"Error deserializing roles: {e}")
            # Fallback to regex if serialization fails
            import re
            roles = re.findall(r's:\d+:"([^"]+)";b:1', meta.meta_value)
            return roles

    async def set_roles(self, user_id: int, roles: List[str]) -> bool:
        """Set user roles"""
        # We need to construct the serialized string.
        # a:N:{s:len:"role";b:1;...}
        from app.model.wordpress.core import WPUserMeta

        # Find the capability key first
        stmt = select(WPUserMeta).where(
             WPUserMeta.user_id == user_id,
             WPUserMeta.meta_key.like("%capabilities")
        )
        result = await self.session.exec(stmt)
        meta = result.first()

        # Use phpserialize for robust serialization
        import phpserialize
        role_dict = {role: True for role in roles}
        serialized_str = phpserialize.dumps(role_dict).decode('utf-8')

        meta_key = meta.meta_key if meta else "8jH_capabilities" # Default to prefix + capabilities

        if meta:
            meta.meta_value = serialized_str
            self.session.add(meta)
        else:
            new_meta = WPUserMeta(
                user_id=user_id,
                meta_key=meta_key,
                meta_value=serialized_str
            )
            self.session.add(new_meta)

        await self.session.commit()
        return True
