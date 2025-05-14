from src.auth.router import router as auth_router
from src.category.router import router as category_router
from src.transaction.router import router as transaction_router

all_routers = [
    auth_router,
    category_router,
    transaction_router,
]