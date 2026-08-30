from fastapi import APIRouter, HTTPException

from app.rag.rag_service import RAGService
from app.schemas.chat import ChatRequest, ChatResponse


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


rag_service = RAGService()


@router.post(
    "",
    response_model=ChatResponse,
)
def chat(request: ChatRequest):

    try:

        result = rag_service.ask(
            question=request.question
        )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )