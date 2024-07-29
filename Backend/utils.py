from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.schema import Document
from typing import List, Dict, Any
import io
from config import DB_CHROMA_PATH

def get_pdf_text(pdf_docs: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    pdf_texts = {}
    for pdf_info in pdf_docs:
        pdf_name = pdf_info["name"]
        pdf_stream = pdf_info["content"]
        pdf_reader = PdfReader(pdf_stream)
        for page_number, page in enumerate(pdf_reader.pages):
            text = page.extract_text()
            pdf_texts.setdefault(pdf_name, []).append({"text": text, "page_number": page_number + 1})
    return pdf_texts

def get_text_chunks(pdf_texts: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
    )
    text_chunks = []
    for pdf_name, pages in pdf_texts.items():
        for page in pages:
            chunks = text_splitter.split_text(page["text"])
            for chunk in chunks:
                text_chunks.append({
                    "text": chunk,
                    "pdf_name": pdf_name,
                    "page_number": page["page_number"]
                })
    return text_chunks

def get_vectorstore(text_chunks: List[Dict[str, Any]]):
    documents = [
        Document(page_content=chunk["text"], metadata={"pdf_name": chunk["pdf_name"], "page_number": chunk["page_number"]})
        for chunk in text_chunks
    ]
    embeddings = OpenAIEmbeddings()
    vector_database = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=DB_CHROMA_PATH,
    )
    vector_database.persist()
    return vector_database

def load_vectorstore():
    vector_database = Chroma(
        persist_directory=DB_CHROMA_PATH,
        embedding_function=OpenAIEmbeddings(),
    )
    return vector_database
