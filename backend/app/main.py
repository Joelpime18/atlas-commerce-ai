from fastapi import FastAPI

from app.api.webhook import router as webhook_router
from app.config.settings import settings


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.include_router(webhook_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}
