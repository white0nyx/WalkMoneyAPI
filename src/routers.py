from src.auth.router import router as auth_router
from src.category.main.router import router as category_router
from src.transaction.router import router as transaction_router
from src.me.router import router as me_router

all_routers = [
    auth_router,
    me_router,
    category_router,
    transaction_router,
]