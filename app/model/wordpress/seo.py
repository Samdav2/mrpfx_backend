"""
SEO plugin database models.
Includes Yoast SEO and Redirection.
Maps to tables with prefixes 8jH_yoast_*, 8jH_redirection_*
"""
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


# =============================================================================
# Yoast SEO Models
# =============================================================================

class YoastIndexable(SQLModel, table=True):
    """Yoast SEO indexables (8jH_yoast_indexable)"""
    __tablename__ = "8jH_yoast_indexable"

    id: Optional[int] = Field(default=None, primary_key=True)
    permalink: Optional[str] = Field(default=None)
    permalink_hash: Optional[str] = Field(default=None, max_length=40)
    object_id: Optional[int] = Field(default=None)
    object_type: str = Field(max_length=32, default="")
    object_sub_type: Optional[str] = Field(default=None, max_length=32)
    author_id: Optional[int] = Field(default=None)
    post_parent: Optional[int] = Field(default=None)
    title: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    breadcrumb_title: Optional[str] = Field(default=None)
    post_status: Optional[str] = Field(default=None, max_length=20)
    is_public: Optional[int] = Field(default=None)
    is_protected: Optional[int] = Field(default=0)
    has_public_posts: Optional[int] = Field(default=None)
    number_of_pages: Optional[int] = Field(default=None)
    canonical: Optional[str] = Field(default=None)
    primary_focus_keyword: Optional[str] = Field(default=None, max_length=191)
    primary_focus_keyword_score: Optional[int] = Field(default=None)
    readability_score: Optional[int] = Field(default=None)
    is_cornerstone: Optional[int] = Field(default=0)
    is_robots_noindex: Optional[int] = Field(default=0)
    is_robots_nofollow: Optional[int] = Field(default=0)
    is_robots_noarchive: Optional[int] = Field(default=0)
    is_robots_noimageindex: Optional[int] = Field(default=0)
    is_robots_nosnippet: Optional[int] = Field(default=0)
    twitter_title: Optional[str] = Field(default=None)
    twitter_image: Optional[str] = Field(default=None)
    twitter_description: Optional[str] = Field(default=None)
    twitter_image_id: Optional[str] = Field(default=None, max_length=191)
    twitter_image_source: Optional[str] = Field(default=None)
    open_graph_title: Optional[str] = Field(default=None)
    open_graph_description: Optional[str] = Field(default=None)
    open_graph_image: Optional[str] = Field(default=None)
    open_graph_image_id: Optional[str] = Field(default=None, max_length=191)
    open_graph_image_source: Optional[str] = Field(default=None)
    open_graph_image_meta: Optional[str] = Field(default=None)
    link_count: Optional[int] = Field(default=None)
    incoming_link_count: Optional[int] = Field(default=None)
    prominent_words_version: Optional[int] = Field(default=None)
    created_at: Optional[datetime] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=None)
    blog_id: int = Field(default=1)
    language: Optional[str] = Field(default=None, max_length=32)
    region: Optional[str] = Field(default=None, max_length=32)
    schema_page_type: Optional[str] = Field(default=None, max_length=64)
    schema_article_type: Optional[str] = Field(default=None, max_length=64)
    has_ancestors: Optional[int] = Field(default=0)
    estimated_reading_time_minutes: Optional[int] = Field(default=None)
    version: Optional[int] = Field(default=1)
    object_last_modified: Optional[datetime] = Field(default=None)
    object_published_at: Optional[datetime] = Field(default=None)


class YoastIndexableHierarchy(SQLModel, table=True):
    """Yoast SEO indexable hierarchy (8jH_yoast_indexable_hierarchy)"""
    __tablename__ = "8jH_yoast_indexable_hierarchy"

    indexable_id: int = Field(primary_key=True, default=0)
    ancestor_id: int = Field(primary_key=True, default=0)
    depth: Optional[int] = Field(default=None)
    blog_id: int = Field(default=1)


class YoastMigration(SQLModel, table=True):
    """Yoast SEO migrations (8jH_yoast_migrations)"""
    __tablename__ = "8jH_yoast_migrations"

    id: Optional[int] = Field(default=None, primary_key=True)
    version: Optional[str] = Field(default=None, max_length=191)


class YoastPrimaryTerm(SQLModel, table=True):
    """Yoast SEO primary terms (8jH_yoast_primary_term)"""
    __tablename__ = "8jH_yoast_primary_term"

    id: Optional[int] = Field(default=None, primary_key=True)
    post_id: Optional[int] = Field(default=None)
    term_id: Optional[int] = Field(default=None)
    taxonomy: str = Field(max_length=32, default="")
    created_at: Optional[datetime] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=None)
    blog_id: int = Field(default=1)


class YoastSEOLink(SQLModel, table=True):
    """Yoast SEO links (8jH_yoast_seo_links)"""
    __tablename__ = "8jH_yoast_seo_links"

    id: Optional[int] = Field(default=None, primary_key=True)
    url: Optional[str] = Field(default=None, max_length=255)
    post_id: Optional[int] = Field(default=None)
    target_post_id: Optional[int] = Field(default=None)
    type: Optional[str] = Field(default=None, max_length=8)
    indexable_id: Optional[int] = Field(default=None)
    target_indexable_id: Optional[int] = Field(default=None)
    height: Optional[int] = Field(default=None)
    width: Optional[int] = Field(default=None)
    size: Optional[int] = Field(default=None)
    language: Optional[str] = Field(default=None, max_length=32)
    region: Optional[str] = Field(default=None, max_length=32)


# =============================================================================
# Redirection Plugin Models
# =============================================================================

class RedirectionGroup(SQLModel, table=True):
    """Redirection groups (8jH_redirection_groups)"""
    __tablename__ = "8jH_redirection_groups"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50, default="")
    tracking: int = Field(default=1)
    module_id: int = Field(default=0)
    status: str = Field(max_length=10, default="enabled")
    position: int = Field(default=0)


class RedirectionItem(SQLModel, table=True):
    """Redirection items (8jH_redirection_items)"""
    __tablename__ = "8jH_redirection_items"

    id: Optional[int] = Field(default=None, primary_key=True)
    url: str = Field(default="")
    match_url: Optional[str] = Field(default=None, max_length=2000)
    match_data: Optional[str] = Field(default=None)
    regex: int = Field(default=0)
    position: int = Field(default=0)
    last_count: int = Field(default=0)
    last_access: Optional[datetime] = Field(default=None)
    group_id: int = Field(default=0, foreign_key="8jH_redirection_groups.id")
    status: str = Field(max_length=10, default="enabled")
    action_type: str = Field(max_length=20, default="")
    action_code: int = Field(default=0)
    action_data: Optional[str] = Field(default=None)
    match_type: str = Field(max_length=20, default="")
    title: Optional[str] = Field(default=None)


class RedirectionLog(SQLModel, table=True):
    """Redirection logs (8jH_redirection_logs)"""
    __tablename__ = "8jH_redirection_logs"

    id: Optional[int] = Field(default=None, primary_key=True)
    created: datetime = Field(default_factory=datetime.now)
    url: str = Field(default="")
    domain: Optional[str] = Field(default=None, max_length=255)
    sent_to: Optional[str] = Field(default=None)
    agent: Optional[str] = Field(default=None)
    referrer: Optional[str] = Field(default=None)
    http_code: int = Field(default=0)
    request_method: Optional[str] = Field(default=None, max_length=10)
    request_data: Optional[str] = Field(default=None)
    redirect_by: Optional[str] = Field(default=None, max_length=50)
    redirection_id: Optional[int] = Field(default=None, foreign_key="8jH_redirection_items.id")
    ip: Optional[str] = Field(default=None, max_length=45)


class Redirection404(SQLModel, table=True):
    """Redirection 404 errors (8jH_redirection_404)"""
    __tablename__ = "8jH_redirection_404"

    id: Optional[int] = Field(default=None, primary_key=True)
    created: datetime = Field(default_factory=datetime.now)
    url: str = Field(default="")
    domain: Optional[str] = Field(default=None, max_length=255)
    agent: Optional[str] = Field(default=None, max_length=255)
    referrer: Optional[str] = Field(default=None, max_length=255)
    http_code: int = Field(default=0)
    request_method: Optional[str] = Field(default=None, max_length=10)
    request_data: Optional[str] = Field(default=None)
    ip: Optional[str] = Field(default=None, max_length=45)
