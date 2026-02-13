"""
WordPress Media/Attachments Repository.
Provides CRUD operations for WordPress media attachments.
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
import os
import re
from PIL import Image
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.model.wordpress.core import WPPost, WPPostMeta


class WPMediaRepository:
    """Repository for WordPress media attachments"""

    def __init__(self, session: AsyncSession):
        self.session = session

    # Get list of media attachments
    async def get_attachments(
        self,
        mime_type: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
        search: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get list of media attachments with optional filters"""
        query = select(WPPost).where(WPPost.post_type == "attachment")

        if mime_type:
            query = query.where(WPPost.post_mime_type.like(f"{mime_type}%"))

        if search:
            query = query.where(
                WPPost.post_title.ilike(f"%{search}%") |
                WPPost.post_name.ilike(f"%{search}%")
            )

        query = query.order_by(WPPost.post_date.desc()).offset(offset).limit(limit)
        result = await self.session.exec(query)
        attachments = result.all()

        media_list = []
        for attachment in attachments:
            media_data = await self._build_media_response(attachment)
            media_list.append(media_data)

        return media_list

    # Get a single attachment by ID
    async def get_attachment(self, attachment_id: int) -> Optional[Dict[str, Any]]:
        """Get a single media attachment by ID"""
        query = select(WPPost).where(
            WPPost.ID == attachment_id,
            WPPost.post_type == "attachment"
        )
        result = await self.session.exec(query)
        attachment = result.first()

        if not attachment:
            return None

        return await self._build_media_response(attachment)

    # Create a new attachment record
    async def create_attachment(
        self,
        user_id: int,
        filename: str,
        mime_type: str,
        guid: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        alt_text: Optional[str] = None,
        caption: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new media attachment record"""
        now = datetime.now()

        attachment = WPPost(
            post_author=user_id,
            post_date=now,
            post_date_gmt=now,
            post_content=description or "",
            post_title=title or filename,
            post_excerpt=caption or "",
            post_status="inherit",
            post_type="attachment",
            post_name=filename.replace(" ", "-").lower(),
            post_modified=now,
            post_modified_gmt=now,
            post_parent=0,
            guid=guid,
            post_mime_type=mime_type,
            comment_status="open",
            ping_status="closed"
        )

        self.session.add(attachment)
        await self.session.commit()
        await self.session.refresh(attachment)

        attachment_id = attachment.ID

        # Add alt text as meta
        if alt_text:
            await self._set_attachment_meta(attachment_id, "_wp_attachment_alt_text", alt_text)

        # Add attached file path
        # WP stores relative to uploads dir: 2024/02/filename.ext
        relative_path = guid.split("/wp-content/uploads/")[-1] if "/wp-content/uploads/" in guid else filename
        await self._set_attachment_meta(attachment_id, "_wp_attached_file", relative_path)

        # Generate thumbnails and metadata
        if mime_type.startswith("image/"):
            try:
                # Need absolute path to process the file
                abs_path = os.path.join(os.getcwd(), guid.split("/")[-4], guid.split("/")[-3], guid.split("/")[-2], guid.split("/")[-1])
                # Simpler: just use relative path from cwd
                abs_path = guid.split(str(self.session.bind.url).rsplit("/", 1)[0])[-1].lstrip("/")
                # Actually, the file was just saved in app/v1/api/wordpress/media.py to wp-content/uploads/...
                abs_path = os.path.join("wp-content/uploads", relative_path)

                metadata = await self._generate_image_metadata(abs_path, relative_path)
                if metadata:
                    await self._set_attachment_meta(attachment_id, "_wp_attachment_metadata", metadata)
            except Exception as e:
                # Log error but don't fail the whole upload
                print(f"Error generating image metadata: {e}")

        return await self._build_media_response(attachment)

    # Update an attachment
    async def update_attachment(
        self,
        attachment_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        alt_text: Optional[str] = None,
        caption: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Update a media attachment"""
        query = select(WPPost).where(
            WPPost.ID == attachment_id,
            WPPost.post_type == "attachment"
        )
        result = await self.session.exec(query)
        attachment = result.first()

        if not attachment:
            return None

        if title is not None:
            attachment.post_title = title
        if description is not None:
            attachment.post_content = description
        if caption is not None:
            attachment.post_excerpt = caption

        attachment.post_modified = datetime.now()
        attachment.post_modified_gmt = datetime.now()

        self.session.add(attachment)

        if alt_text is not None:
            await self._set_attachment_meta(attachment_id, "_wp_attachment_alt_text", alt_text)

        attachment_id = attachment.ID
        await self.session.commit()

        return await self.get_attachment(attachment_id)

    # Delete an attachment
    async def delete_attachment(self, attachment_id: int, force: bool = False) -> bool:
        """Delete a media attachment"""
        query = select(WPPost).where(
            WPPost.ID == attachment_id,
            WPPost.post_type == "attachment"
        )
        result = await self.session.exec(query)
        attachment = result.first()

        if not attachment:
            return False

        if force:
            # Delete meta first
            meta_query = select(WPPostMeta).where(WPPostMeta.post_id == attachment_id)
            meta_result = await self.session.exec(meta_query)
            for meta in meta_result.all():
                await self.session.delete(meta)

            await self.session.delete(attachment)
        else:
            attachment.post_status = "trash"
            self.session.add(attachment)

        await self.session.commit()
        return True

    # Get attachment URL with different sizes
    async def get_attachment_urls(self, attachment_id: int) -> Dict[str, str]:
        """Get all available URLs for an attachment (different sizes)"""
        query = select(WPPost).where(
            WPPost.ID == attachment_id,
            WPPost.post_type == "attachment"
        )
        result = await self.session.exec(query)
        attachment = result.first()

        if not attachment:
            return {}

        base_url = attachment.guid

        # Get attachment metadata for sizes
        meta_query = select(WPPostMeta).where(
            WPPostMeta.post_id == attachment_id,
            WPPostMeta.meta_key == "_wp_attachment_metadata"
        )
        meta_result = await self.session.exec(meta_query)
        meta = meta_result.first()

        urls = {"full": base_url}

        if meta and meta.meta_value:
            # Extract sizes from serialized PHP data
            # Format: s:5:"sizes";a:N:{s:9:"thumbnail";a:4:{s:4:"file";s:nn:"file-150x150.jpg";...}}
            base_dir_url = base_url.rsplit("/", 1)[0]

            # Simple regex parser for our generated metadata
            sizes = ["thumbnail", "medium", "large"]
            for size in sizes:
                # Match: s:9:"thumbnail";a:4:{s:4:"file";s:23:"image-150x150.jpg";
                pattern = rf's:{len(size)}:"{size}";a:4:{{s:4:"file";s:\d+:"([^"]+)"'
                match = re.search(pattern, meta.meta_value)
                if match:
                    urls[size] = f"{base_dir_url}/{match.group(1)}"

        return urls

    # Helper: Generate image metadata and resized versions
    async def _generate_image_metadata(self, file_path: str, relative_path: str) -> Optional[str]:
        """Generate multiple image sizes and return serialized WP metadata"""
        if not os.path.exists(file_path):
            return None

        try:
            with Image.open(file_path) as img:
                width, height = img.size
                mime_type = f"image/{img.format.lower()}"

                # Sizes to generate
                target_sizes = {
                    "thumbnail": (150, 150, True),  # Crop
                    "medium": (300, 300, False),    # Scale
                    "large": (1024, 1024, False)    # Scale
                }

                file_dir = os.path.dirname(file_path)
                file_base, file_ext = os.path.splitext(os.path.basename(file_path))

                sizes_meta = {}

                for size_name, (tw, th, crop) in target_sizes.items():
                    # Only resize if original is larger
                    if width > tw or height > th:
                        resized_img = img.copy()
                        if crop:
                            # Center crop to aspect ratio
                            w_ratio = tw / width
                            h_ratio = th / height
                            ratio = max(w_ratio, h_ratio)
                            new_size = (int(width * ratio), int(height * ratio))
                            resized_img = resized_img.resize(new_size, Image.LANCZOS)

                            # Calculate crop box
                            left = (resized_img.width - tw) / 2
                            top = (resized_img.height - th) / 2
                            resized_img = resized_img.crop((left, top, left + tw, top + th))
                            rw, rh = tw, th
                        else:
                            # Thumbnail scale
                            resized_img.thumbnail((tw, th), Image.LANCZOS)
                            rw, rh = resized_img.size

                        resized_filename = f"{file_base}-{rw}x{rh}{file_ext}"
                        resized_path = os.path.join(file_dir, resized_filename)
                        resized_img.save(resized_path)

                        sizes_meta[size_name] = {
                            "file": resized_filename,
                            "width": rw,
                            "height": rh,
                            "mime-type": mime_type
                        }

                # Serialize to WP Format (at least enough for our read logic)
                # a:4:{s:5:"width";i:W;s:6:"height";i:H;s:4:"file";s:N:"REL_PATH";s:5:"sizes";a:M:{...}}
                def serialize_size(name, data):
                    return (f's:{len(name)}:"{name}";a:4:{{'
                            f's:4:"file";s:{len(data["file"])}:"{data["file"]}";'
                            f's:5:"width";i:{data["width"]};'
                            f's:6:"height";i:{data["height"]};'
                            f's:9:"mime-type";s:{len(data["mime-type"])}:"{data["mime-type"]}";}}')

                sizes_str = "".join([serialize_size(k, v) for k, v in sizes_meta.items()])

                metadata = (f'a:5:{{s:5:"width";i:{width};s:6:"height";i:{height};'
                           f's:4:"file";s:{len(relative_path)}:"{relative_path}";'
                           f's:5:"sizes";a:{len(sizes_meta)}:{{{sizes_str}}}'
                           f's:10:"image_meta";a:0:{{}}}}')

                return metadata
        except Exception as e:
            print(f"Error in _generate_image_metadata: {e}")
            return None

    # Helper: Build media response
    async def _build_media_response(self, attachment: WPPost) -> Dict[str, Any]:
        """Build a complete media response with all metadata"""
        # Get alt text
        alt_meta = await self._get_attachment_meta(attachment.ID, "_wp_attachment_alt_text")

        # Get URLs
        urls = await self.get_attachment_urls(attachment.ID)

        return {
            "id": attachment.ID,
            "title": attachment.post_title,
            "description": attachment.post_content,
            "caption": attachment.post_excerpt,
            "alt_text": alt_meta or "",
            "url": attachment.guid,
            "mime_type": attachment.post_mime_type,
            "date_created": attachment.post_date,
            "date_modified": attachment.post_modified,
            "author": attachment.post_author,
            "sizes": urls,
            "slug": attachment.post_name
        }

    # Helper: Get attachment meta
    async def _get_attachment_meta(self, attachment_id: int, meta_key: str) -> Optional[str]:
        """Get a single meta value for an attachment"""
        query = select(WPPostMeta).where(
            WPPostMeta.post_id == attachment_id,
            WPPostMeta.meta_key == meta_key
        )
        result = await self.session.exec(query)
        meta = result.first()
        return meta.meta_value if meta else None

    # Helper: Set attachment meta
    async def _set_attachment_meta(self, attachment_id: int, meta_key: str, meta_value: str) -> None:
        """Set or update a meta value for an attachment"""
        query = select(WPPostMeta).where(
            WPPostMeta.post_id == attachment_id,
            WPPostMeta.meta_key == meta_key
        )
        result = await self.session.exec(query)
        meta = result.first()

        if meta:
            meta.meta_value = meta_value
            self.session.add(meta)
        else:
            new_meta = WPPostMeta(
                post_id=attachment_id,
                meta_key=meta_key,
                meta_value=meta_value
            )
            self.session.add(new_meta)
