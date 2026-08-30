from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter


class TextChunker:
    """
    Splits documents into overlapping semantic chunks.
    """

    def __init__(
        self,
        chunk_size: int = 1000,
        overlap: int = 200,
    ):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ],
        )

    def split_text(self, text: str) -> List[str]:

        if not text:
            return []

        text = text.strip()

        return self.splitter.split_text(text)