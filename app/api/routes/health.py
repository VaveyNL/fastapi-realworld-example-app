from fastapi import APIRouter, Request, Response, status

router = APIRouter()


@router.get("/health", name="health:check", tags=["health"])
async def health(request: Request, response: Response) -> dict:
    try:
        async with request.app.state.pool.acquire() as connection:
            await connection.fetchval("SELECT 1")
    except Exception:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "error", "database": "unavailable"}
    return {"status": "ok", "database": "ok"}
