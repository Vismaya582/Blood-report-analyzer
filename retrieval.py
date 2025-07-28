from sentence_transformers import SentenceTransformer
import lancedb

LANCE_DB_PATH = "lance_db"  
LANCE_TABLE_NAME = "chunk_embeddings"
TOP_K = 5 # top 5 retrieval

embedder = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L6-v2")
db = lancedb.connect(LANCE_DB_PATH)  #connecting lancedb
table = db.open_table(LANCE_TABLE_NAME)

def retrieve_context(prompt_text, top_k=TOP_K): # taking prompt from user, embedded it, does the search in lancedb 
    prompt_embedding = embedder.encode(prompt_text).tolist()
    results_df = table.search(prompt_embedding).limit(top_k).to_pandas()
    return "\n".join(results_df["text"].tolist())

