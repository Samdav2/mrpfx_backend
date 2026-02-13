"""
WordPress Core Post/Page Pydantic Schemas for API responses and requests.
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


# ============== Post Schemas ==============

class WPPostBase(BaseModel):
    """Base post schema for WordPress posts/pages"""
    post_title: str = Field(..., description="Post title")
    post_content: Optional[str] = Field("", description="Post content")
    post_excerpt: Optional[str] = Field("", description="Post excerpt")
    post_status: Optional[str] = Field("draft", description="Post status (publish, draft, pending, etc)")
    post_type: Optional[str] = Field("post", description="Post type (post, page, product, lp_course, etc)")
    post_parent: Optional[int] = Field(0, description="Parent post ID")
    menu_order: Optional[int] = Field(0, description="Menu order")
    comment_status: Optional[str] = Field("open", description="Comment status")
    ping_status: Optional[str] = Field("open", description="Ping status")


class WPPostCreate(WPPostBase):
    """Schema for creating a new post/page"""
    post_name: Optional[str] = Field(None, description="Post slug (auto-generated if not provided)")


class WPPostUpdate(BaseModel):
    """Schema for updating a post/page"""
    post_title: Optional[str] = None
    post_content: Optional[str] = None
    post_excerpt: Optional[str] = None
    post_status: Optional[str] = None
    post_name: Optional[str] = None
    post_parent: Optional[int] = None
    menu_order: Optional[int] = None
    comment_status: Optional[str] = None
    ping_status: Optional[str] = None


class WPImageRead(BaseModel):
    """Schema for reading an image/attachment"""
    id: int
    url: str
    title: Optional[str] = None
    alt_text: Optional[str] = None
    caption: Optional[str] = None

    class Config:
        from_attributes = True


class WPPostRead(WPPostBase):
    """Schema for reading a post/page"""
    ID: int
    post_author: int
    post_date: datetime
    post_date_gmt: datetime
    post_modified: datetime
    post_modified_gmt: datetime
    post_name: str
    guid: Optional[str] = None
    comment_count: int = 0
    featured_image: Optional[WPImageRead] = None

    class Config:
        from_attributes = True


class WPPostMetaBase(BaseModel):
    """Base post meta schema"""
    meta_key: str
    meta_value: Optional[str] = None


class WPPostMetaCreate(WPPostMetaBase):
    """Schema for creating post meta"""
    post_id: int


class WPPostMetaRead(WPPostMetaBase):
    """Schema for reading post meta"""
    meta_id: int
    post_id: int

    class Config:
        from_attributes = True


# ============== Comment Schemas ==============

class WPCommentBase(BaseModel):
    """Base comment schema"""
    comment_content: str = Field(..., description="Comment content")
    comment_author: Optional[str] = Field("", description="Comment author name")
    comment_author_email: Optional[str] = Field("", description="Comment author email")
    comment_author_url: Optional[str] = Field("", description="Comment author URL")


class WPCommentCreate(WPCommentBase):
    """Schema for creating a comment"""
    comment_post_ID: int = Field(..., description="Post ID")
    comment_parent: Optional[int] = Field(0, description="Parent comment ID")
    user_id: Optional[int] = Field(0, description="User ID if logged in")


class WPCommentUpdate(BaseModel):
    """Schema for updating a comment"""
    comment_content: Optional[str] = None
    comment_approved: Optional[str] = None


class WPCommentRead(WPCommentBase):
    """Schema for reading a comment"""
    comment_ID: int
    comment_post_ID: int
    comment_date: datetime
    comment_date_gmt: datetime
    comment_approved: str = "1"
    comment_parent: int = 0
    user_id: int = 0
    comment_karma: int = 0

    class Config:
        from_attributes = True


# ============== Term/Category Schemas ==============

class WPTermBase(BaseModel):
    """Base term schema"""
    name: str = Field(..., description="Term name")
    slug: Optional[str] = Field(None, description="Term slug")


class WPTermCreate(WPTermBase):
    """Schema for creating a term"""
    pass


class WPTermRead(WPTermBase):
    """Schema for reading a term"""
    term_id: int
    term_group: int = 0

    class Config:
        from_attributes = True


class WPTermTaxonomyBase(BaseModel):
    """Base term taxonomy schema"""
    taxonomy: str = Field(..., description="Taxonomy name")
    description: Optional[str] = Field("", description="Term description")
    parent: Optional[int] = Field(0, description="Parent term ID")


class WPTermTaxonomyCreate(WPTermTaxonomyBase):
    """Schema for creating term taxonomy"""
    term_id: int


class WPTermTaxonomyRead(WPTermTaxonomyBase):
    """Schema for reading term taxonomy"""
    term_taxonomy_id: int
    term_id: int
    count: int = 0

    class Config:
        from_attributes = True


class WPCategory(BaseModel):
    """Combined category schema with term and taxonomy info"""
    term_id: int
    name: str
    slug: str
    taxonomy: str = "category"
    description: Optional[str] = ""
    parent: int = 0
    count: int = 0

    class Config:
        from_attributes = True


class WPTag(BaseModel):
    """Tag schema"""
    term_id: int
    name: str
    slug: str
    taxonomy: str = "post_tag"
    description: Optional[str] = ""
    count: int = 0

    class Config:
        from_attributes = True


# ============== Option Schemas ==============

class WPOptionBase(BaseModel):
    """Base option schema"""
    option_name: str = Field(..., max_length=191)
    option_value: Optional[str] = Field("")


class WPOptionCreate(WPOptionBase):
    """Schema for creating an option"""
    autoload: Optional[str] = Field("yes")


class WPOptionRead(WPOptionBase):
    """Schema for reading an option"""
    option_id: int
    autoload: str = "yes"

    class Config:
        from_attributes = True


# ============== Link Schemas ==============

class WPLinkBase(BaseModel):
    """Base link schema"""
    link_url: str = Field(..., description="Link URL")
    link_name: str = Field(..., description="Link name")
    link_description: Optional[str] = Field("", description="Link description")
    link_visible: Optional[str] = Field("Y", description="Visibility")
    link_target: Optional[str] = Field("", description="Target attribute")
    link_rel: Optional[str] = Field("", description="Rel attribute")


class WPLinkCreate(WPLinkBase):
    """Schema for creating a link"""
    link_owner: int = Field(..., description="Link owner user ID")


class WPLinkRead(WPLinkBase):
    """Schema for reading a link"""
    link_id: int
    link_owner: int
    link_rating: int = 0
    link_updated: datetime
    link_notes: Optional[str] = ""

    class Config:
        from_attributes = True


# ============== Post with Terms ==============

class WPPostWithTerms(WPPostRead):
    """Post with associated terms/categories/tags"""
    categories: List[WPCategory] = []
    tags: List[WPTag] = []
    meta: List[WPPostMetaRead] = []
