from app.rag.chunking.chunker import TextChunker

sample_text = """
The Smart Pharmacy Predictive Analytics System is an intelligent healthcare
solution designed to improve medicine inventory management using Artificial
Intelligence and Machine Learning. The system predicts demand, detects expiry
risks, analyzes medicine consumption patterns, and recommends stock levels.
""" * 20


chunker = TextChunker(
    chunk_size=300,
    overlap=50,
)

chunks = chunker.split_text(sample_text)

print(f"Total Chunks : {len(chunks)}")

for i, chunk in enumerate(chunks):

    print("=" * 60)
    print(f"Chunk {i+1}")
    print("=" * 60)
    print(chunk)
    print()