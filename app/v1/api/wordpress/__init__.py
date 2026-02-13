from fastapi import APIRouter

from .users import router as users_router
from .members import router as members_router
from .learnpress import router as learnpress_router

router = APIRouter()

router.include_router(users_router, prefix="/wordpress/users", tags=["WordPress Users"])
router.include_router(members_router, prefix="/wordpress/members", tags=["SWPM Members"])
router.include_router(learnpress_router, prefix="/wordpress/learnpress", tags=["LearnPress"])

from .woocommerce import router as woocommerce_router
router.include_router(woocommerce_router, prefix="/wordpress/wc", tags=["WooCommerce"])

from .posts import router as posts_router
router.include_router(posts_router, prefix="/wordpress", tags=["WordPress Content"])

# Plugin API endpoints
from .security import router as security_router
router.include_router(security_router, prefix="/wordpress/security", tags=["Security"])

from .seo import router as seo_router
router.include_router(seo_router, prefix="/wordpress/seo", tags=["SEO"])

from .marketing import router as marketing_router
router.include_router(marketing_router, prefix="/wordpress/marketing", tags=["Marketing"])

from .forms import router as forms_router
router.include_router(forms_router, prefix="/wordpress/forms", tags=["Forms"])

from .media import router as media_router
router.include_router(media_router, prefix="/wordpress/media", tags=["Media"])
