from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def create_vector_store(pdf_path):

    try:
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()

        if not documents:
            raise ValueError("PDF contains no readable pages.")

        documents = [
            doc for doc in documents
            if doc.page_content.strip()
        ]

        if not documents:
            raise ValueError(
                "No extractable text found. "
                "The PDF may be scanned or image-based."
            )

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        chunks = splitter.split_documents(documents)

        if not chunks:
            raise ValueError("Could not create PDF text chunks.")

        vector_store = FAISS.from_documents(
            chunks,
            embeddings
        )

        return vector_store

    except Exception as e:
        raise RuntimeError(f"PDF processing failed: {e}")


def ask_pdf(vector_store, question):

    if not question.strip():
        raise ValueError("Question cannot be empty.")

    try:
        documents = vector_store.similarity_search(
            question,
            k=4
        )

        if not documents:
            return {
                "answer": "No relevant information found.",
                "sources": []
            }

        context = ""
        sources = []

        for document in documents:

            page = document.metadata.get("page", 0) + 1

            context += f"""
Page {page}:
{document.page_content}
"""

            sources.append({
                "page": page,
                "content": document.page_content
            })

        prompt = f"""
You are a PDF question-answering assistant.

Answer ONLY using the provided context.

If the answer is unavailable, say:
"The information was not found in the PDF."

Context:
{context}

Question:
{question}

Give a clear and concise answer.
"""

        response = llm.invoke(prompt)

        return {
            "answer": response.content,
            "sources": sources
        }

    except Exception as e:
        raise RuntimeError(f"PDF question failed: {e}")
