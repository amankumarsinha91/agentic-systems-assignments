import os
import chromadb
from chromadb.config import Settings
from openai import OpenAI

# -----------------------------
# HR POLICY DOCUMENTS
# -----------------------------

HR_POLICY_DOCUMENTS = [
    {
        "id": "leave_policy",
        "text": (
            "Employees are entitled to 24 days of annual leave per calendar year. "
            "Up to 10 days of sick leave are available and cannot be carried forward. "
            "Unused annual leave can be carried forward up to a maximum of 8 days. "
            "Any excess leave lapses at the end of the year."
        ),
        "metadata": {"category": "Leave Policy", "source": "InnoTech HR Handbook"}
    },
    {
        "id": "wfh_policy",
        "text": (
            "Employees may work from home up to two days per week depending on role eligibility. "
            "Eligibility begins after successful completion of three months of employment. "
            "Manager approval is mandatory for regular work‑from‑home schedules. "
            "The company may revoke WFH privileges if performance is affected."
        ),
        "metadata": {"category": "Work From Home Policy", "source": "InnoTech HR Handbook"}
    },
    {
        "id": "appraisal_policy",
        "text": (
            "Employee appraisals are conducted annually at the end of the financial year. "
            "Performance is measured on a five‑point rating scale. "
            "Salary increments are linked to appraisal ratings and company performance. "
            "Final decisions are approved by senior leadership."
        ),
        "metadata": {"category": "Appraisal Policy", "source": "InnoTech HR Handbook"}
    },
    {
        "id": "code_of_conduct",
        "text": (
            "All employees must maintain respectful and professional workplace behavior. "
            "Confidential company and customer data must be protected at all times. "
            "Conflicts of interest must be disclosed immediately. "
            "Violations may lead to disciplinary action."
        ),
        "metadata": {"category": "Code of Conduct", "source": "InnoTech HR Handbook"}
    },
]

client = OpenAI()

# -----------------------------
# EMBEDDINGS
# -----------------------------

def create_embeddings(texts):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )
    return [e.embedding for e in response.data]

# -----------------------------
# VECTOR DATABASE
# -----------------------------

def setup_vector_database():
    chroma_client = chromadb.PersistentClient(
        path="./chroma_hr_policy_db",
        settings=Settings()
    )
    return chroma_client.get_or_create_collection(
        name="hr_policy_collection",
        metadata={"hnsw:space": "cosine"}
    )

def index_hr_documents(collection):
    texts = [d["text"] for d in HR_POLICY_DOCUMENTS]
    embeddings = create_embeddings(texts)

    collection.upsert(
        ids=[d["id"] for d in HR_POLICY_DOCUMENTS],
        documents=texts,
        metadatas=[d["metadata"] for d in HR_POLICY_DOCUMENTS],
        embeddings=embeddings
    )

# -----------------------------
# RETRIEVAL
# -----------------------------

def retrieve_hr_content(collection, query, top_k=3):
    query_embedding = create_embeddings([query])[0]
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i]
        })
    return chunks

# -----------------------------
# PROMPT + GENERATION
# -----------------------------

def build_grounded_prompt(query, chunks):
    context = "\n\n".join(
        f"[{c['metadata']['category']}]\n{c['text']}" for c in chunks
    )

    return f"""
You are an HR Policy Assistant.
Answer ONLY using the policy context below.
If the answer is not present, say:
"I’m unable to find this information in the HR policies."

Policy Context:
{context}

Question:
{query}

Answer:
"""

def generate_answer(query, chunks):
    prompt = build_grounded_prompt(query, chunks)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content.strip()

def generate_answer_without_retrieval(query):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": query}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def answer_with_rag(collection, query):
    chunks = retrieve_hr_content(collection, query)
    print("\nRetrieved Chunks:")
    for c in chunks:
        print("-", c["metadata"]["category"], ":", c["text"])

    print("\nAnswer:")
    print(generate_answer(query, chunks))

# -----------------------------
# MAIN
# -----------------------------

if __name__ == "__main__":
    collection = setup_vector_database()
    index_hr_documents(collection)

    queries = [
        "How many days of annual leave do I get?",
        "Do I need approval to work from home?",
        "When is the appraisal cycle and how are increments decided?"
    ]

    for q in queries:
        print("\n==============================")
        print("Question:", q)
        answer_with_rag(collection, q)

    print("\n==============================")
    print("WITHOUT RAG:")
    print(generate_answer_without_retrieval("How many annual leave days are employees entitled to?"))