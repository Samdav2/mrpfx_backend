"""
Core WordPress database models.
Maps to tables: 8jH_users, 8jH_usermeta, 8jH_posts, 8jH_postmeta,
8jH_comments, 8jH_commentmeta, 8jH_options, 8jH_terms, 8jH_termmeta,
8jH_term_taxonomy, 8jH_term_relationships, 8jH_links
"""
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class WPUser(SQLModel, table=True):
    """WordPress users table (8jH_users)"""
    __tablename__ = "8jH_users"

    ID: Optional[int] = Field(default=None, primary_key=True)
    user_login: str = Field(max_length=60, default="", index=True)
    user_pass: str = Field(max_length=255, default="")
    user_nicename: str = Field(max_length=50, default="", index=True)
    user_email: str = Field(max_length=100, default="", index=True)
    user_url: str = Field(max_length=100, default="")
    user_registered: datetime = Field(default_factory=datetime.now)
    user_activation_key: str = Field(max_length=255, default="")
    user_status: int = Field(default=0)
    display_name: str = Field(max_length=250, default="")


class WPUserMeta(SQLModel, table=True):
    """WordPress user meta table (8jH_usermeta)"""
    __tablename__ = "8jH_usermeta"

    umeta_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(default=0, foreign_key="8jH_users.ID", index=True)
    meta_key: Optional[str] = Field(default=None, max_length=255, index=True)
    meta_value: Optional[str] = Field(default=None)


class WPPost(SQLModel, table=True):
    """WordPress posts table (8jH_posts)"""
    __tablename__ = "8jH_posts"

    ID: Optional[int] = Field(default=None, primary_key=True)
    post_author: int = Field(default=0, foreign_key="8jH_users.ID")
    post_date: datetime = Field(default_factory=datetime.now)
    post_date_gmt: datetime = Field(default_factory=datetime.now)
    post_content: str = Field(default="")
    post_title: str = Field(default="")
    post_excerpt: str = Field(default="")
    post_status: str = Field(max_length=20, default="publish")
    comment_status: str = Field(max_length=20, default="open")
    ping_status: str = Field(max_length=20, default="open")
    post_password: str = Field(max_length=255, default="")
    post_name: str = Field(max_length=200, default="", index=True)
    to_ping: str = Field(default="")
    pinged: str = Field(default="")
    post_modified: datetime = Field(default_factory=datetime.now)
    post_modified_gmt: datetime = Field(default_factory=datetime.now)
    post_content_filtered: str = Field(default="")
    post_parent: int = Field(default=0, index=True)
    guid: str = Field(max_length=255, default="")
    menu_order: int = Field(default=0)
    post_type: str = Field(max_length=20, default="post", index=True)
    post_mime_type: str = Field(max_length=100, default="")
    comment_count: int = Field(default=0)


class WPPostMeta(SQLModel, table=True):
    """WordPress post meta table (8jH_postmeta)"""
    __tablename__ = "8jH_postmeta"

    meta_id: Optional[int] = Field(default=None, primary_key=True)
    post_id: int = Field(default=0, foreign_key="8jH_posts.ID", index=True)
    meta_key: Optional[str] = Field(default=None, max_length=255, index=True)
    meta_value: Optional[str] = Field(default=None)


class WPComment(SQLModel, table=True):
    """WordPress comments table (8jH_comments)"""
    __tablename__ = "8jH_comments"

    comment_ID: Optional[int] = Field(default=None, primary_key=True)
    comment_post_ID: int = Field(default=0, foreign_key="8jH_posts.ID")
    comment_author: str = Field(default="")
    comment_author_email: str = Field(max_length=100, default="")
    comment_author_url: str = Field(max_length=200, default="")
    comment_author_IP: str = Field(max_length=100, default="")
    comment_date: datetime = Field(default_factory=datetime.now)
    comment_date_gmt: datetime = Field(default_factory=datetime.now)
    comment_content: str = Field(default="")
    comment_karma: int = Field(default=0)
    comment_approved: str = Field(max_length=20, default="1")
    comment_agent: str = Field(max_length=255, default="")
    comment_type: str = Field(max_length=20, default="comment")
    comment_parent: int = Field(default=0)
    user_id: int = Field(default=0)


class WPCommentMeta(SQLModel, table=True):
    """WordPress comment meta table (8jH_commentmeta)"""
    __tablename__ = "8jH_commentmeta"

    meta_id: Optional[int] = Field(default=None, primary_key=True)
    comment_id: int = Field(default=0, foreign_key="8jH_comments.comment_ID")
    meta_key: Optional[str] = Field(default=None, max_length=255)
    meta_value: Optional[str] = Field(default=None)


class WPOption(SQLModel, table=True):
    """WordPress options table (8jH_options)"""
    __tablename__ = "8jH_options"

    option_id: Optional[int] = Field(default=None, primary_key=True)
    option_name: str = Field(max_length=191, default="", unique=True, index=True)
    option_value: str = Field(default="")
    autoload: str = Field(max_length=20, default="yes", index=True)


class WPTerm(SQLModel, table=True):
    """WordPress terms table (8jH_terms)"""
    __tablename__ = "8jH_terms"

    term_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=200, default="")
    slug: str = Field(max_length=200, default="")
    term_group: int = Field(default=0)


class WPTermMeta(SQLModel, table=True):
    """WordPress term meta table (8jH_termmeta)"""
    __tablename__ = "8jH_termmeta"

    meta_id: Optional[int] = Field(default=None, primary_key=True)
    term_id: int = Field(default=0, foreign_key="8jH_terms.term_id")
    meta_key: Optional[str] = Field(default=None, max_length=255)
    meta_value: Optional[str] = Field(default=None)


class WPTermTaxonomy(SQLModel, table=True):
    """WordPress term taxonomy table (8jH_term_taxonomy)"""
    __tablename__ = "8jH_term_taxonomy"

    term_taxonomy_id: Optional[int] = Field(default=None, primary_key=True)
    term_id: int = Field(default=0, foreign_key="8jH_terms.term_id")
    taxonomy: str = Field(max_length=32, default="")
    description: str = Field(default="")
    parent: int = Field(default=0)
    count: int = Field(default=0)


class WPTermRelationship(SQLModel, table=True):
    """WordPress term relationships table (8jH_term_relationships)"""
    __tablename__ = "8jH_term_relationships"

    object_id: int = Field(primary_key=True, default=0)
    term_taxonomy_id: int = Field(primary_key=True, default=0, foreign_key="8jH_term_taxonomy.term_taxonomy_id")
    term_order: int = Field(default=0)


class WPLink(SQLModel, table=True):
    """WordPress links table (8jH_links)"""
    __tablename__ = "8jH_links"

    link_id: Optional[int] = Field(default=None, primary_key=True)
    link_url: str = Field(max_length=255, default="")
    link_name: str = Field(max_length=255, default="")
    link_image: str = Field(max_length=255, default="")
    link_target: str = Field(max_length=25, default="")
    link_description: str = Field(max_length=255, default="")
    link_visible: str = Field(max_length=20, default="Y")
    link_owner: int = Field(default=1)
    link_rating: int = Field(default=0)
    link_updated: datetime = Field(default_factory=datetime.now)
    link_rel: str = Field(max_length=255, default="")
    link_notes: str = Field(default="")
    link_rss: str = Field(max_length=255, default="")
