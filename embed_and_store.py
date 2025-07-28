# embed_and_store.py

import time
from sentence_transformers import SentenceTransformer
import lancedb
import pandas as pd
import os

# -------------------- Timer Start --------------------
start_time = time.time()

# -------------------- Load Chunks --------------------
with open("text_chunks.txt", "r", encoding="utf-8") as f:
    raw_chunks = f.read().split("\n--- Chunk")

# Clean and keep non-empty chunks
chunks = [chunk.strip() for chunk in raw_chunks if chunk.strip()]

# Print sample chunk (for debugging)
print(f"Sample chunk preview:\n{chunks[0][:200]}...\n")

# -------------------- Clean Cache (Optional Fix for Model Errors) --------------------
from sentence_transformers import SentenceTransformer
import shutil
import os

cache_path = os.path.expanduser("~/.cache/huggingface/hub/models--sentence-transformers--all-MiniLM-L6-v2")
if os.path.exists(cache_path):
    print("⚠️ Corrupted cache found. Clearing...")
    shutil.rmtree(cache_path)

# -------------------- Load Embedding Model --------------------
from sentence_transformers import SentenceTransformer

# Use a PyTorch-compatible model from Hugging Face
model = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L6-v2")
print("Embedding model loaded!")

# -------------------- Embed the Chunks --------------------
embeddings = model.encode(chunks, show_progress_bar=True)
print(f"✅ Generated {len(embeddings)} embeddings.")

# Sanity check
assert len(chunks) == len(embeddings), "❌ Mismatch between number of chunks and embeddings!"

# -------------------- Setup LanceDB --------------------
db_path = "lance_db"
table_name = "chunk_embeddings"

# Create LanceDB connection
db = lancedb.connect(db_path)

# Check if table exists
if table_name in db.table_names():
    print(f"⚠️ Table '{table_name}' already exists. It will be overwritten.")

# Create or overwrite table
table = db.create_table(
    table_name,
    data=pd.DataFrame({"text": chunks, "vector": embeddings.tolist()}),
    mode="overwrite"
)

print(" -> Embeddings saved to LanceDB!")

# -------------------- Timer End --------------------
end_time = time.time()
elapsed = end_time - start_time
print(f"\n Done in {elapsed:.2f} seconds.")
