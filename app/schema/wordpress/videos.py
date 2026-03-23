from pydantic import BaseModel, Field

class YouTubeVideoRead(BaseModel):
    id: str = Field(..., description="YouTube Video ID")
    title: str = Field(..., description="Video Title")
    thumbnail: str = Field(..., description="Thumbnail URL")

    class Config:
        from_attributes = True
