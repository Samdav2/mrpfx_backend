from fastapi import APIRouter
from .learnpress import router as learnpress_router
from .comments import router as comments_router
from .forms import router as forms_router

router = APIRouter()

router.include_router(learnpress_router, prefix="/admin/learnpress", tags=["Admin LearnPress"])
router.include_router(comments_router, prefix="/admin/comments", tags=["Admin Comments"])
router.include_router(forms_router, prefix="/admin/forms", tags=["Admin Forms"])
