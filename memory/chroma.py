import os
import chromadb
from chromadb.config import Settings
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

CHROMA_URL = os.getenv("CHROMA_URL", "http://localhost:8000")

def get_vector_store(collection_name: str = "codebase"):
    host = "localhost"
    port = 8000
    try:
        if "://" in CHROMA_URL:
            host = CHROMA_URL.split("://")[1].split(":")[0]
            port = int(CHROMA_URL.split("://")[1].split(":")[1].split("/")[0])
    except Exception:
        pass

    client = chromadb.HttpClient(
        host=host,
        port=port,
        settings=Settings(allow_reset=True)
    )
    
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma(
        client=client,
        collection_name=collection_name,
        embedding_function=embeddings
    )
    return vectorstore
