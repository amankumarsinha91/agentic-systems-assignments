from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "hostel_policy_docs"


def format_docs(docs):
    return "\n\n".join(
        f"{doc.page_content}\nSOURCE: {doc.metadata.get('source', 'unknown')}"
        for doc in docs
    )


def main():
    # ✅ Load embeddings
    embedding = OpenAIEmbeddings(model="text-embedding-3-small")

    # ✅ Load vector store (no re-ingest)
    vectordb = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embedding,
        collection_name=COLLECTION_NAME,
    )

    # ✅ Retriever
    retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 2})

    # ✅ Prompt with guardrails
    prompt = PromptTemplate(
        template="""
You are a hostel policy assistant.

Use ONLY the context provided below to answer the question.
If the answer is not in the context, say:
"I don't know based on the provided documents."

Also mention the source file name if possible.

Context:
{context}

Question:
{question}

Answer:
""",
        input_variables=["context", "question"],
    )

    # ✅ LLM
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # ✅ LCEL chain
    rag_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    # ✅ Queries
    questions = [
        "What are the quiet hours on weekdays?",
        "What is the scholarship amount for hostel residents?",
    ]

    for i, q in enumerate(questions, 1):
        print(f"\nQ{i}: {q}")
        answer = rag_chain.invoke(q)
        print(f"A{i}: {answer}")


if __name__ == "__main__":
    main()