import fitz  # PyMuPDF
from docx import Document


class ParserService:

    @staticmethod
    def extract_text(file_path: str) -> str:
        """
        Detect file type and extract text.
        """

        if file_path.lower().endswith(".pdf"):
            return ParserService._extract_pdf(file_path)

        elif file_path.lower().endswith(".docx"):
            return ParserService._extract_docx(file_path)

        elif file_path.lower().endswith(".txt"):
            return ParserService._extract_txt(file_path)

        else:
            raise ValueError("Unsupported file type.")

    @staticmethod
    def _extract_pdf(file_path: str) -> str:
        text = ""

        pdf = fitz.open(file_path)

        for page in pdf:
            text += page.get_text()

        pdf.close()

        return text

    @staticmethod
    def _extract_docx(file_path: str) -> str:
        document = Document(file_path)

        return "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

    @staticmethod
    def _extract_txt(file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()