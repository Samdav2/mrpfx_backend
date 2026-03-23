from typing import Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.model.wordpress.core import WPOption

class WPOptionRepository:
    """Repository for WordPress options table (8jH_options)"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_option(self, option_name: str, default: Optional[str] = None) -> Optional[str]:
        """Get an option value by name."""
        statement = select(WPOption).where(WPOption.option_name == option_name)
        result = await self.session.exec(statement)
        option = result.first()
        return option.option_value if option else default

    async def update_option(self, option_name: str, option_value: str) -> WPOption:
        """Update or create an option."""
        statement = select(WPOption).where(WPOption.option_name == option_name)
        result = await self.session.exec(statement)
        option = result.first()

        if option:
            option.option_value = option_value
            self.session.add(option)
        else:
            option = WPOption(option_name=option_name, option_value=option_value, autoload="yes")
            self.session.add(option)

        await self.session.commit()
        await self.session.refresh(option)
        return option

    async def delete_option(self, option_name: str) -> bool:
        """Delete an option by name."""
        statement = select(WPOption).where(WPOption.option_name == option_name)
        result = await self.session.exec(statement)
        option = result.first()

        if option:
            await self.session.delete(option)
            await self.session.commit()
            return True
        return False
