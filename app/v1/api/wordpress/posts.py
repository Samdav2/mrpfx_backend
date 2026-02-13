"""
WordPress Posts, Pages, Comments, Terms, Links, and Featured Images API Endpoints.
Full CRUD operations for WordPress core content types.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlmodel import Session
from pydantic import BaseModel

from app.db.session import get_session
from app.repo.wordpress.posts import WPPostRepository, WPCommentRepository, WPTermRepository
from app.repo.wordpress.links import WPLinkRepository
from app.schema.wordpress.post import (
    WPPostCreate, WPPostUpdate, WPPostRead, WPPostWithTerms,
    WPCommentCreate, WPCommentUpdate, WPCommentRead,
    WPCategory, WPTag
)
from app.dependencies.auth import get_current_user
from app.model.user import User

router = APIRouter()


# ============== Request Schemas ==============

class FeaturedImageRequest(BaseModel):
    attachment_id: int


class LinkCreate(BaseModel):
    url: str
    name: str
    description: Optional[str] = ""
    target: Optional[str] = ""
    rel: Optional[str] = ""
    visible: Optional[str] = "Y"


class LinkUpdate(BaseModel):
    url: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    target: Optional[str] = None
    rel: Optional[str] = None
    visible: Optional[str] = None


# ============== Posts ==============

@router.get("/posts", response_model=List[WPPostRead], tags=["WordPress Posts"])
async def get_posts(
    status: str = Query("publish", description="Post status (e.g., publish, draft, any)"),
    limit: int = Query(10, le=100),
    offset: int = Query(0),
    session: Session = Depends(get_session)
):
    """Get list of posts"""
    repo = WPPostRepository(session)
    return await repo.get_posts(post_type="post", status=status, limit=limit, offset=offset)


@router.get("/posts/{slug}", response_model=WPPostRead, tags=["WordPress Posts"])
async def get_post(
    slug: str,
    session: Session = Depends(get_session)
):
    """Get a single post by slug or numeric ID"""
    repo = WPPostRepository(session)
    # Check if the parameter is a numeric ID
    if slug.isdigit():
        post = await repo.get_post_by_id(int(slug), post_type="post")
    else:
        post = await repo.get_post_by_slug(slug, post_type="post")
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.get("/posts/{slug}/full", response_model=WPPostWithTerms, tags=["WordPress Posts"])
async def get_post_with_terms(
    slug: str,
    session: Session = Depends(get_session)
):
    """Get a post with associated categories and tags by slug or numeric ID"""
    repo = WPPostRepository(session)
    if slug.isdigit():
        # First get post by ID, then fetch terms using its slug
        post_basic = await repo.get_post_by_id(int(slug), post_type="post")
        if post_basic:
            post = await repo.get_post_with_terms_by_slug(post_basic.post_name, post_type="post")
        else:
            post = None
    else:
        post = await repo.get_post_with_terms_by_slug(slug, post_type="post")
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.post("/posts", response_model=WPPostRead, tags=["WordPress Posts"])
async def create_post(
    post_data: WPPostCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new post"""
    repo = WPPostRepository(session)
    return await repo.create_post(user_id=current_user.ID, data=post_data)


@router.put("/posts/{post_id}", response_model=WPPostRead, tags=["WordPress Posts"])
async def update_post(
    post_id: int,
    post_data: WPPostUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update an existing post"""
    repo = WPPostRepository(session)
    post = await repo.update_post(post_id, post_data)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.delete("/posts/{post_id}", tags=["WordPress Posts"])
async def delete_post(
    post_id: int,
    force: bool = Query(False, description="Permanently delete instead of trashing"),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete (trash) or permanently delete a post"""
    repo = WPPostRepository(session)
    success = await repo.delete_post(post_id, force=force)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post deleted successfully"}


@router.post("/posts/{post_id}/terms", tags=["WordPress Posts"])
async def assign_terms_to_post(
    post_id: int,
    term_ids: List[int],
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Assign categories/tags to a post"""
    repo = WPTermRepository(session)
    await repo.assign_terms_to_post(post_id, term_ids)
    return {"message": "Terms assigned successfully"}


@router.delete("/posts/{post_id}/terms", tags=["WordPress Posts"])
async def remove_terms_from_post(
    post_id: int,
    term_ids: List[int],
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Remove categories/tags from a post"""
    repo = WPTermRepository(session)
    await repo.remove_terms_from_post(post_id, term_ids)
    return {"message": "Terms removed successfully"}


# ============== Pages ==============

@router.get("/pages", response_model=List[WPPostRead], tags=["WordPress Pages"])
async def get_pages(
    status: str = Query("publish", description="Page status (e.g., publish, draft, any)"),
    limit: int = Query(10, le=100),
    offset: int = Query(0),
    session: Session = Depends(get_session)
):
    """Get list of pages"""
    repo = WPPostRepository(session)
    return await repo.get_posts(post_type="page", status=status, limit=limit, offset=offset)


@router.get("/pages/{slug}", response_model=WPPostRead, tags=["WordPress Pages"])
async def get_page(
    slug: str,
    session: Session = Depends(get_session)
):
    """Get a single page by slug or numeric ID"""
    repo = WPPostRepository(session)
    if slug.isdigit():
        page = await repo.get_post_by_id(int(slug), post_type="page")
    else:
        page = await repo.get_post_by_slug(slug, post_type="page")
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return page


@router.post("/pages", response_model=WPPostRead, tags=["WordPress Pages"])
async def create_page(
    page_data: WPPostCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new page"""
    # Force post_type to page
    page_data.post_type = "page"
    repo = WPPostRepository(session)
    return await repo.create_post(user_id=current_user.ID, data=page_data)


@router.put("/pages/{page_id}", response_model=WPPostRead, tags=["WordPress Pages"])
async def update_page(
    page_id: int,
    page_data: WPPostUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update an existing page"""
    repo = WPPostRepository(session)
    page = await repo.update_post(page_id, page_data)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return page


@router.delete("/pages/{page_id}", tags=["WordPress Pages"])
async def delete_page(
    page_id: int,
    force: bool = Query(False),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a page"""
    repo = WPPostRepository(session)
    success = await repo.delete_post(page_id, force=force)
    if not success:
        raise HTTPException(status_code=404, detail="Page not found")
    return {"message": "Page deleted successfully"}


# ============== Comments ==============

@router.get("/posts/{post_id}/comments", response_model=List[WPCommentRead], tags=["WordPress Comments"])
async def get_post_comments(
    post_id: int,
    status: str = Query("approve", description="Comment status"),
    limit: int = Query(50, le=200),
    offset: int = Query(0),
    session: Session = Depends(get_session)
):
    """Get comments for a specific post"""
    repo = WPCommentRepository(session)
    return await repo.get_comments(post_id=post_id, status=status, limit=limit, offset=offset)


@router.get("/comments", response_model=List[WPCommentRead], tags=["WordPress Comments"])
async def get_all_comments(
    status: str = Query("approve", description="Comment status"),
    limit: int = Query(50, le=200),
    offset: int = Query(0),
    session: Session = Depends(get_session)
):
    """Get all comments (admin)"""
    repo = WPCommentRepository(session)
    return await repo.get_comments(status=status, limit=limit, offset=offset)


@router.get("/comments/{comment_id}", response_model=WPCommentRead, tags=["WordPress Comments"])
async def get_comment(
    comment_id: int,
    session: Session = Depends(get_session)
):
    """Get a single comment by ID"""
    repo = WPCommentRepository(session)
    comment = await repo.get_comment(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


@router.post("/posts/{post_id}/comments", response_model=WPCommentRead, tags=["WordPress Comments"])
async def create_comment(
    post_id: int,
    comment_data: WPCommentCreate,
    request: Request,
    session: Session = Depends(get_session)
):
    """Add a comment to a post"""
    comment_data.comment_post_ID = post_id
    repo = WPCommentRepository(session)

    # Get client IP and user agent
    ip = request.client.host if request.client else ""
    user_agent = request.headers.get("user-agent", "")

    return await repo.create_comment(comment_data, ip=ip, user_agent=user_agent)


@router.put("/comments/{comment_id}", response_model=WPCommentRead, tags=["WordPress Comments"])
async def update_comment(
    comment_id: int,
    comment_data: WPCommentUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a comment"""
    repo = WPCommentRepository(session)
    comment = await repo.update_comment(comment_id, comment_data)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


@router.delete("/comments/{comment_id}", tags=["WordPress Comments"])
async def delete_comment(
    comment_id: int,
    force: bool = Query(False),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a comment"""
    repo = WPCommentRepository(session)
    success = await repo.delete_comment(comment_id, force=force)
    if not success:
        raise HTTPException(status_code=404, detail="Comment not found")
    return {"message": "Comment deleted successfully"}


# ============== Categories ==============

@router.get("/categories", response_model=List[dict], tags=["WordPress Terms"])
async def get_categories(
    limit: int = Query(100, le=500),
    offset: int = Query(0),
    session: Session = Depends(get_session)
):
    """Get list of categories"""
    repo = WPTermRepository(session)
    return await repo.get_terms(taxonomy="category", limit=limit, offset=offset)


@router.get("/categories/{category_id}", response_model=dict, tags=["WordPress Terms"])
async def get_category(
    category_id: int,
    session: Session = Depends(get_session)
):
    """Get a single category"""
    repo = WPTermRepository(session)
    term = await repo.get_term(category_id)
    if not term or term.get("taxonomy") != "category":
        raise HTTPException(status_code=404, detail="Category not found")
    return term


@router.post("/categories", response_model=dict, tags=["WordPress Terms"])
async def create_category(
    name: str,
    slug: Optional[str] = None,
    description: str = "",
    parent: int = 0,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new category"""
    repo = WPTermRepository(session)
    return await repo.create_term(
        name=name,
        taxonomy="category",
        slug=slug,
        description=description,
        parent=parent
    )


@router.put("/categories/{category_id}", response_model=dict, tags=["WordPress Terms"])
async def update_category(
    category_id: int,
    name: Optional[str] = None,
    slug: Optional[str] = None,
    description: Optional[str] = None,
    parent: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a category"""
    repo = WPTermRepository(session)
    term = await repo.update_term(category_id, name=name, slug=slug, description=description, parent=parent)
    if not term:
        raise HTTPException(status_code=404, detail="Category not found")
    return term


@router.delete("/categories/{category_id}", tags=["WordPress Terms"])
async def delete_category(
    category_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a category"""
    repo = WPTermRepository(session)
    success = await repo.delete_term(category_id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted successfully"}


# ============== Tags ==============

@router.get("/tags", response_model=List[dict], tags=["WordPress Terms"])
async def get_tags(
    limit: int = Query(100, le=500),
    offset: int = Query(0),
    session: Session = Depends(get_session)
):
    """Get list of tags"""
    repo = WPTermRepository(session)
    return await repo.get_terms(taxonomy="post_tag", limit=limit, offset=offset)


@router.get("/tags/{tag_id}", response_model=dict, tags=["WordPress Terms"])
async def get_tag(
    tag_id: int,
    session: Session = Depends(get_session)
):
    """Get a single tag"""
    repo = WPTermRepository(session)
    term = await repo.get_term(tag_id)
    if not term or term.get("taxonomy") != "post_tag":
        raise HTTPException(status_code=404, detail="Tag not found")
    return term


@router.post("/tags", response_model=dict, tags=["WordPress Terms"])
async def create_tag(
    name: str,
    slug: Optional[str] = None,
    description: str = "",
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new tag"""
    repo = WPTermRepository(session)
    return await repo.create_term(
        name=name,
        taxonomy="post_tag",
        slug=slug,
        description=description
    )


@router.put("/tags/{tag_id}", response_model=dict, tags=["WordPress Terms"])
async def update_tag(
    tag_id: int,
    name: Optional[str] = None,
    slug: Optional[str] = None,
    description: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a tag"""
    repo = WPTermRepository(session)
    term = await repo.update_term(tag_id, name=name, slug=slug, description=description)
    if not term:
        raise HTTPException(status_code=404, detail="Tag not found")
    return term


@router.delete("/tags/{tag_id}", tags=["WordPress Terms"])
async def delete_tag(
    tag_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a tag"""
    repo = WPTermRepository(session)
    success = await repo.delete_term(tag_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tag not found")
    return {"message": "Tag deleted successfully"}


# ============== Featured Images ==============

@router.get("/posts/{post_id}/featured-image", tags=["WordPress Posts"])
async def get_post_featured_image(
    post_id: int,
    session: Session = Depends(get_session)
):
    """Get the featured image for a post"""
    repo = WPPostRepository(session)
    image = await repo.get_featured_image(post_id)
    if not image:
        raise HTTPException(status_code=404, detail="No featured image set")
    return image


@router.put("/posts/{post_id}/featured-image", tags=["WordPress Posts"])
async def set_post_featured_image(
    post_id: int,
    image_data: FeaturedImageRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Set the featured image for a post"""
    repo = WPPostRepository(session)
    success = await repo.set_featured_image(post_id, image_data.attachment_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to set featured image. Check post and attachment IDs.")
    return {"message": "Featured image set successfully"}


@router.delete("/posts/{post_id}/featured-image", tags=["WordPress Posts"])
async def remove_post_featured_image(
    post_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Remove the featured image from a post"""
    repo = WPPostRepository(session)
    success = await repo.remove_featured_image(post_id)
    if not success:
        raise HTTPException(status_code=404, detail="No featured image to remove")
    return {"message": "Featured image removed successfully"}


@router.get("/pages/{page_id}/featured-image", tags=["WordPress Pages"])
async def get_page_featured_image(
    page_id: int,
    session: Session = Depends(get_session)
):
    """Get the featured image for a page"""
    repo = WPPostRepository(session)
    image = await repo.get_featured_image(page_id)
    if not image:
        raise HTTPException(status_code=404, detail="No featured image set")
    return image


@router.put("/pages/{page_id}/featured-image", tags=["WordPress Pages"])
async def set_page_featured_image(
    page_id: int,
    image_data: FeaturedImageRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Set the featured image for a page"""
    repo = WPPostRepository(session)
    success = await repo.set_featured_image(page_id, image_data.attachment_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to set featured image")
    return {"message": "Featured image set successfully"}


@router.delete("/pages/{page_id}/featured-image", tags=["WordPress Pages"])
async def remove_page_featured_image(
    page_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Remove the featured image from a page"""
    repo = WPPostRepository(session)
    success = await repo.remove_featured_image(page_id)
    if not success:
        raise HTTPException(status_code=404, detail="No featured image to remove")
    return {"message": "Featured image removed successfully"}


# ============== Links ==============

@router.get("/links", tags=["WordPress Links"])
async def get_links(
    visible_only: bool = Query(True, description="Only return visible links"),
    limit: int = Query(100, le=500),
    offset: int = Query(0),
    session: Session = Depends(get_session)
):
    """Get all WordPress links"""
    repo = WPLinkRepository(session)
    return await repo.get_links(visible_only=visible_only, limit=limit, offset=offset)


@router.get("/links/{link_id}", tags=["WordPress Links"])
async def get_link(
    link_id: int,
    session: Session = Depends(get_session)
):
    """Get a single link by ID"""
    repo = WPLinkRepository(session)
    link = await repo.get_link(link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return link


@router.post("/links", tags=["WordPress Links"])
async def create_link(
    link_data: LinkCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new link"""
    repo = WPLinkRepository(session)
    return await repo.create_link(
        url=link_data.url,
        name=link_data.name,
        owner_id=current_user.ID,
        description=link_data.description or "",
        target=link_data.target or "",
        rel=link_data.rel or "",
        visible=link_data.visible or "Y"
    )


@router.put("/links/{link_id}", tags=["WordPress Links"])
async def update_link(
    link_id: int,
    link_data: LinkUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update an existing link"""
    repo = WPLinkRepository(session)
    link = await repo.update_link(
        link_id=link_id,
        url=link_data.url,
        name=link_data.name,
        description=link_data.description,
        target=link_data.target,
        rel=link_data.rel,
        visible=link_data.visible
    )
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return link


@router.delete("/links/{link_id}", tags=["WordPress Links"])
async def delete_link(
    link_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a link"""
    repo = WPLinkRepository(session)
    success = await repo.delete_link(link_id)
    if not success:
        raise HTTPException(status_code=404, detail="Link not found")
    return {"message": "Link deleted successfully"}
