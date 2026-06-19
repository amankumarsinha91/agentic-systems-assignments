import os
import shutil
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "hostel_policy_docs"


def main():
    # ✅ Delete old DB if exists
    if os.path.exists(CHROMA_DIR):
        shutil.rmtree(CHROMA_DIR)
        print("Old chroma_db deleted.")

    # ✅ Load documents
    loader = DirectoryLoader(
        "documents",
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    docs = loader.load()
    print(f"Loaded {len(docs)} documents.")

    # ✅ Split documents
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=60,
        add_start_index=True,
    )
    chunks = splitter.split_documents(docs)
    print(f"Split into {len(chunks)} chunks.")

    # ✅ Embeddings
    embedding = OpenAIEmbeddings(model="text-embedding-3-small")

    # ✅ Store in Chroma
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embedding,
        persist_directory=CHROMA_DIR,
        collection_name=COLLECTION_NAME,
    )

    vectordb.persist()
    print("✅ Ingestion completed and persisted.")


if __name__ == "__main__":
    main()