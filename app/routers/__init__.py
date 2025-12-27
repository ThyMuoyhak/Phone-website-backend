from .phones import router as phones_router
from .auth import router as auth_router
from .orders import router as orders_router

__all__ = ["phones_router", "auth_router", "orders_router"]