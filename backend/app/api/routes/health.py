from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("")
def health():

    return {
        "status": "healthy",
        "service": "Support Docs Copilot",
        "version": "1.0.0",
    }