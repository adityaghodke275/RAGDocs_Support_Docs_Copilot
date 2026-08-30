from app.services.parser_service import ParserService


class LoaderFactory:

    def load(self, filepath: str):

        return ParserService.extract_text(filepath)