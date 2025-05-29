import os
import logging
import mimetypes

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.common.database import migrate
from src.common.redis_db import redis_client
from src.common.logger import ch
from src.routers import all_routers

logger = logging.getLogger("root")
logger.setLevel(logging.INFO)
logger.addHandler(ch)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await migrate()
    mimetypes.add_type("image/webp", ".webp")
    yield
    await redis_client.close()


if os.environ.get("ENV") == "prod":
    app = FastAPI(
        title="New App API",
        openapi_url=None,
        docs_url=None,
        redoc_url=None,
        lifespan=lifespan,
    )
else:
    app = FastAPI(
        title="WalkMoneyAPI",
        openapi_url="/api/openapi.json",
        docs_url="/api/docs",
        lifespan=lifespan,
    )

api = APIRouter(
    prefix="/api",
    responses={404: {"description": "Page not found"}},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)

for router in all_routers:
    api.include_router(router)

app.include_router(api)
