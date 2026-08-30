from pydantic import BaseModel, Field
from typing import List


class ChatRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=1,
        description="Question to ask about the uploaded documents.",
    )


class Source(BaseModel):

    document: str
    chunks: List[int]


class ChatResponse(BaseModel):

    question: str
    answer: str
    sources: List[Source]