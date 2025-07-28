# -------------------- Import Libraries --------------------
import fitz  # PyMuPDF
import time

print("PyMuPDF is installed correctly!")

# -------------------- Chunking Function (Simple) --------------------
def chunk_text(input_txt_path, chunk_size=500, overlap=100):
    with open(input_txt_path, "r", encoding="utf-8") as f:
        full_text = f.read()

    words = full_text.split()
    chunks = []
    i = 0

    while i < len(words):
        chunk = words[i:i + chunk_size]
        chunks.append(" ".join(chunk))
        i += chunk_size - overlap  # move forward with overlap

    print(f"✅ Created {len(chunks)} chunks.")
    return chunks

# -------------------- PDF Text Extraction --------------------
def extract_pdf_text(pdf_path, output_txt_path):
    doc = fitz.open(pdf_path)
    with open(output_txt_path, "w", encoding="utf-8") as f_out:
        for page_num in range(len(doc)):
            text = doc[page_num].get_text()
            f_out.write(f"\n--- Page {page_num + 1} ---\n")
            f_out.write(text + "\n")
    doc.close()
    print("✅ Text extraction complete!")

# -------------------- Save Chunks to File --------------------
def save_chunks_to_file(chunks, output_file="text_chunks.txt"):
    with open(output_file, "w", encoding="utf-8") as f:
        for i, chunk in enumerate(chunks):
            f.write(f"\n--- Chunk {i+1} ---\n")
            f.write(chunk + "\n")
    print("✅ All chunks saved to text_chunks.txt")

# -------------------- Run the Pipeline with Timer --------------------
start_time = time.time()

extract_pdf_text("nutrition_book.pdf", "extracted_text.txt")
chunks = chunk_text("extracted_text.txt")
save_chunks_to_file(chunks)

end_time = time.time()
print(f"\n⏱️ Total Execution Time: {end_time - start_time:.2f} seconds")
