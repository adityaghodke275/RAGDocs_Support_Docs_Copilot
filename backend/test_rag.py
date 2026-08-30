from app.rag.rag_service import RAGService

rag = RAGService()

response = rag.ask(
    question = "What is PPE Detection?" \
    "What are its advantages?"
)

print("\nQUESTION")
print(response["question"])

print("\nANSWER")
print(response["answer"])

print("\nSOURCES")

for source in response["sources"]:
    print(source)