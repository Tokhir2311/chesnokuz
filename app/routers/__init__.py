from .posts import router as posts_router
from .category import router as category_router
from .user import router as user_router
from .tag import router as tags_router
from .profession import router as prof_router
from .comment import router as comment_router
from .wetaherapi import router as weather_router
from .auth.basic import router as basic_router
from .auth.register import router as register_router
from .auth.session import router as session_router
__all__ = [
            "posts_router", 
           "category_router", 
           "user_router", 
           "tags_router", 
           "prof_router", 
           "comment_router", 
           "weather_router",
           "basic_router",
           "register_router",
           "session_router"
           ]
