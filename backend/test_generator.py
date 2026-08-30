from app.rag.generator.generator_service import GeneratorService

generator = GeneratorService()

response = generator.generate(
    "Explain Artificial Intelligence in one paragraph."
)

print(response)