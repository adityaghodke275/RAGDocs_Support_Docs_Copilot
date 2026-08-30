from app.rag.retrieval.retrieval_service import RetrievalService
from app.rag.prompting.prompt_builder import PromptBuilder

retriever = RetrievalService()

chunks = retriever.retrieve(
    "What is Artificial Intelligence?"
)

prompt = PromptBuilder.build(
    question="What is Artificial Intelligence?",
    contexts=chunks,
)

print(prompt)