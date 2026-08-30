from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """
    Generates embeddings for text using SentenceTransformers.
    """

    def __init__(
        self,
        model_name: str = "BAAI/bge-base-en-v1.5",
    ):
        self.model = SentenceTransformer(model_name)

    def embed_text(self, text: str):

        return self.model.encode(
            text,
            convert_to_numpy=True
        )

    def embed_texts(self, texts: list[str]):

        return self.model.encode(
            texts,
            convert_to_numpy=True
        )