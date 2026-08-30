from app.services.parser_service import ParserService

text = ParserService.extract_text(
    "../data/uploads/3d5d0aea-e194-4085-95fb-33472db9853a.pdf"
)

print(text[:1000])