"""
Caching plugin database models.
Includes LiteSpeed Cache.
Maps to tables with prefix 8jH_litespeed_*
"""
from typing import Optional
from sqlmodel import SQLModel, Field


class LiteSpeedUrl(SQLModel, table=True):
    """LiteSpeed Cache URLs (8jH_litespeed_url)"""
    __tablename__ = "8jH_litespeed_url"

    id: Optional[int] = Field(default=None, primary_key=True)
    url: str = Field(max_length=500, default="")
    cache_tags: str = Field(max_length=1000, default="")


class LiteSpeedUrlFile(SQLModel, table=True):
    """LiteSpeed Cache URL files (8jH_litespeed_url_file)"""
    __tablename__ = "8jH_litespeed_url_file"

    id: Optional[int] = Field(default=None, primary_key=True)
    url_id: int = Field(default=0, foreign_key="8jH_litespeed_url.id")
    vary: str = Field(max_length=32, default="")
    filename: str = Field(max_length=32, default="")
    type: int = Field(default=0)  # css=1, js=2, ccss=3, ucss=4
    expired: int = Field(default=0)
