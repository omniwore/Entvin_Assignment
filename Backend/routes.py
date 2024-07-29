from fastapi import APIRouter, UploadFile, File, Form
from typing import List
from utils import get_pdf_text, get_text_chunks, get_vectorstore, load_vectorstore
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
import io

router = APIRouter()

def get_conversation_chain(vectorstore, chat_history=None):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(
        memory_key='chat_history',
        return_messages=True,
        output_key='answer'
    )
    if chat_history:
        memory.chat_memory.messages = chat_history
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        memory=memory,
        return_source_documents=True,
        output_key='answer'
    )
    return conversation_chain

@router.post("/upload")
async def upload_pdfs(files: List[UploadFile] = File(...)):
    pdf_docs = [{"name": file.filename, "content": io.BytesIO(await file.read())} for file in files]
    raw_texts = get_pdf_text(pdf_docs)
    text_chunks = get_text_chunks(raw_texts)
    vectorstore = get_vectorstore(text_chunks)
    return {"message": "Files processed successfully."}

@router.post("/ask")
async def ask_question(question: str = Form(...)):
    vectorstore = load_vectorstore()
    conversation_chain = get_conversation_chain(vectorstore)

    response = conversation_chain({'question': question})

    source_documents = response.get('source_documents', [])
    if not source_documents:
        return {"error": "No relevant documents found."}

    best_match = source_documents[0]
    pdf_name = best_match.metadata.get("pdf_name", "Unknown PDF")
    page_number = best_match.metadata.get("page_number", "Unknown page")

    chat_history = response['chat_history']
    
    return {
        "responses": [
            {
                "user": chat_history[i].content,
                "bot": f"{chat_history[i+1].content} (Source: {pdf_name}, Page: {page_number})"
            }
            for i in range(0, len(chat_history), 2)
        ]
    }
