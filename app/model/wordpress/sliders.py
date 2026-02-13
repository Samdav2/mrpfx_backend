"""
Slider plugin database models.
Includes Smart Slider 3 (Nextend).
Maps to tables with prefix 8jH_nextend2_*
"""
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class SmartSliderImageStorage(SQLModel, table=True):
    """Smart Slider image storage (8jH_nextend2_image_storage)"""
    __tablename__ = "8jH_nextend2_image_storage"

    id: Optional[int] = Field(default=None, primary_key=True)
    hash: str = Field(max_length=32, default="")
    image: str = Field(default="")
    value: str = Field(default="")


class SmartSliderSectionStorage(SQLModel, table=True):
    """Smart Slider section storage (8jH_nextend2_section_storage)"""
    __tablename__ = "8jH_nextend2_section_storage"

    id: Optional[int] = Field(default=None, primary_key=True)
    application: str = Field(max_length=20, default="")
    section: str = Field(max_length=128, default="")
    referencekey: str = Field(max_length=128, default="")
    value: str = Field(default="")
    isSystem: int = Field(default=0)
    editable: int = Field(default=1)


class SmartSlider(SQLModel, table=True):
    """Smart Slider sliders (8jH_nextend2_smartslider3_sliders)"""
    __tablename__ = "8jH_nextend2_smartslider3_sliders"

    id: Optional[int] = Field(default=None, primary_key=True)
    alias: Optional[str] = Field(default=None)
    title: str = Field(default="")
    type: str = Field(max_length=30, default="")
    params: str = Field(default="")
    slider_status: str = Field(max_length=50, default="published")
    time: datetime = Field(default_factory=datetime.now)
    thumbnail: str = Field(default="")
    ordering: int = Field(default=0)


class SmartSliderXref(SQLModel, table=True):
    """Smart Slider cross-references (8jH_nextend2_smartslider3_sliders_xref)"""
    __tablename__ = "8jH_nextend2_smartslider3_sliders_xref"

    group_id: int = Field(primary_key=True)
    slider_id: int = Field(primary_key=True, foreign_key="8jH_nextend2_smartslider3_sliders.id")
    ordering: int = Field(default=0)


class SmartSlide(SQLModel, table=True):
    """Smart Slider slides (8jH_nextend2_smartslider3_slides)"""
    __tablename__ = "8jH_nextend2_smartslider3_slides"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: Optional[str] = Field(default=None)
    slider: int = Field(default=0, foreign_key="8jH_nextend2_smartslider3_sliders.id")
    publish_up: Optional[datetime] = Field(default=None)
    publish_down: Optional[datetime] = Field(default=None)
    published: int = Field(default=0)
    first: int = Field(default=0)
    slide: Optional[str] = Field(default=None)
    description: str = Field(default="")
    thumbnail: Optional[str] = Field(default=None)
    params: str = Field(default="")
    ordering: int = Field(default=0)
    generator_id: int = Field(default=0)


class SmartSliderGenerator(SQLModel, table=True):
    """Smart Slider generators (8jH_nextend2_smartslider3_generators)"""
    __tablename__ = "8jH_nextend2_smartslider3_generators"

    id: Optional[int] = Field(default=None, primary_key=True)
    group: str = Field(max_length=254, default="")
    type: str = Field(max_length=254, default="")
    params: str = Field(default="")
