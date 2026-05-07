import os
import chromadb
from chromadb.config import Settings
from pypdf import PdfReader
from openai import OpenAI

# ---------- CONFIG ----------
CHUNK_SIZE = 150
OVERLAP = 25
COLLECTION_NAME = "campus_policies"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------- HELPERS ----------

def infer_policy_type(filename):
    fname = filename.lower()
    if "hostel" in fname:
        return "hostel"
    elif "refund" in fname:
        return "refund"
    elif "library" in fname:
        return "library"
    else:
        return "general"


def clean_text(text):
    return " ".join(text.replace("\n", " ").split())


def split_text(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = words[i:i + chunk_size]
        chunks.append(" ".join(chunk))
        i += chunk_size - overlap
    return chunks


def load_pdfs(folder_path):
    documents = []
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            path = os.path.join(folder_path, filename)
            reader = PdfReader(path)
            
            print(f"Loaded {len(reader.pages)} pages from: {filename}")
            
            policy_type = infer_policy_type(filename)
            
            for page_num, page in enumerate(reader.pages):
                text = clean_text(page.extract_text() or "")
                documents.append({
                    "text": text,
                    "source": filename,
                    "page": page_num,
                    "policy_type": policy_type
                })
    
    return documents


# ---------- EMBEDDINGS ----------

def get_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding


# ---------- VECTOR STORE ----------

def build_vector_db(documents):
    chroma_client = chromadb.Client(Settings(
        persist_directory="chroma_db"
    ))

    collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)

    chunks = []
    metadatas = []
    ids = []
    embeddings = []

    idx = 0

    for doc in documents:
        splits = split_text(doc["text"])
        
        for chunk in splits:
            chunks.append(chunk)
            metadatas.append({
                "source": doc["source"],
                "page": doc["page"],
                "policy_type": doc["policy_type"]
            })
            ids.append(f"id_{idx}")
            embeddings.append(get_embedding(chunk))
            idx += 1

    print(f"\nTotal chunks created: {len(chunks)}")

    collection.upsert(
        documents=chunks,
        metadatas=metadatas,
        ids=ids,
        embeddings=embeddings
    )

    chroma_client.persist()
    print(f"Successfully stored {len(chunks)} chunks in vector database.\n")

    return collection


# ---------- RETRIEVAL ----------

def retrieve_chunks(query, collection, top_k=3):
    query_embedding = get_embedding(query)
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    print(f"Retrieved {top_k} relevant chunks.")

    return results["documents"][0], results["metadatas"][0]


# ---------- PROMPT ----------

def build_prompt(context_chunks, question):
    context = "\n\n".join(context_chunks)

    prompt = f"""
You are a campus policy assistant.

Answer ONLY from the context below.
If the answer is not present, say: "I don't have that information."

Context:
{context}

Question:
{question}

Answer in a simple and student-friendly way.
"""
    return prompt


# ---------- ANSWER ----------

def answer_question(question, collection):
    print(f"\nUser Query: {question}")
    
    chunks, metadata = retrieve_chunks(question, collection)

    prompt = build_prompt(chunks, question)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    answer = response.choices[0].message.content
    print("Answer:", answer)


# ---------- MAIN ----------

if __name__ == "__main__":
    print("Initializing RAG pipeline...\n")

    docs = load_pdfs("policy_documents")
    
    collection = build_vector_db(docs)

    print("Vector DB ready. Collection:", COLLECTION_NAME)

    # -------- TEST QUERIES --------
    queries = [
        "Can I get a refund after dropping a course?",
        "What is the deadline for returning a library book?",
        "Are hostel visitors allowed on weekends?"
    ]

    for q in queries:
        answer_question(q, collection)