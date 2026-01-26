from .posts import router as posts_router
from .category import router as category_router
from .user import router as user_router
from .tag import router as tags_router

__all__ = ["posts_router", "category_router", "user_router", "tags_router"]
