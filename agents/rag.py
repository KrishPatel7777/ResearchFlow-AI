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
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    if not documents:
        raise ValueError("No text found in PDF")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    if not chunks:
        raise ValueError("Could not create text chunks")

    vector_store = FAISS.from_documents(chunks, embeddings)
    return vector_store

def ask_pdf(vector_store, question):
    documents = vector_store.similarity_search(
        question,
        k=4
    )

    context = "\n\n".join(document.page_content for document in documents)

    prompt = f"""
    You are a PDF question-answering assistant.

    Answer the question using ONLY the provided context.

    If the answer is not available in the context,
    say that the information was not found in the PDF.

    Context:
    {context}

    Question:
    {question}

    Answer clearly and concisely.
    """

    response = llm.invoke(prompt)
    return response.content