import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import InMemoryVectorStore

load_dotenv()

WEBSITES = [
    "https://google.com",
    "https://google.com/about",
    "https://google.com/faq",
    "https://en.wikipedia.org/wiki/Google",
    "https://about.google/",
     "https://about.google/company-info/"


]

def extract_text(url: str) -> str:
    html = requests.get(url, timeout=10).text
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style"]):
        tag.decompose()

    return "\n".join(
        line.strip()
        for line in soup.get_text("\n").splitlines()
        if line.strip()
    )

def build_vector_store():
    documents = []

    # Load website content
    for url in WEBSITES:
        text = extract_text(url)
        documents.append(
            Document(
                page_content=text,
                metadata={"source": url}
            )
        )

    # Chunk documents
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )
    chunks = splitter.split_documents(documents)

    # Create embeddings
    embeddings = OpenAIEmbeddings()

    # Create in-memory vector store
    vectorstore = InMemoryVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    print("✅ In-memory knowledge base created")
    return vectorstore


if __name__ == "__main__":
    build_vector_store()
