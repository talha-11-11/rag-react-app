from langchain_openai import ChatOpenAI
from ingest import build_vector_store
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

# Build KB at startup
vectorstore = build_vector_store()

def ask_rag(question: str) -> str:
    docs = vectorstore.similarity_search(question, k=4)

    context = "\n\n".join(
        f"Source: {d.metadata['source']}\n{d.page_content}"
        for d in docs
    )

    prompt = f"""
Answer ONLY using the context below.
If the answer is not found, say:
"Information not found in the knowledge base."

Context:
{context}

Question:
{question}
"""

    return llm.invoke(prompt).content
