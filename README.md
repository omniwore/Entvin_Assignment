Multiple PDF information retrieval app:

Please install the requirements using pip install -r requiremnts.txt

If any other requiremnts remain please install 

Run frontend by going to frontend directory using streamlit run ui.py

Run Backend by going to backend and uvicorn main:app --reload



Architecture of the WebApplication:





TECH USED:
FRONTEND= Streamlit
BACKEND=FastAPI
DB = ChromaDB(For storing vector embeddings)


How Application Works:

-It will take multiple or single PDF file from user

-Read all text from PDFs

-String of text will be converted to smaller chunks of texts

-Chunks will contain content, page number and pdf file name


-Then will convert these chunks into vector embeddings using OpenAI Embeddings model
(Vector representation of text)

-We can use other open source Embedding models as well but they will be slow as they
will be running on our Hardware

-After converting to vector embeddings we will store them in vector store (Knowledge base)
I have used ChromaDB for storing the Vector Embeddings. (We can use Faiss or Pinecone as well)

-But Faiss will store it in memory and to persist we should use ChromaDB,

-Now user can ask question from the PDF

-We will embed this question similarly as we embedded the text chunks

-This will allow us to find similar vector that are similar from all chunks of text.

-This will give us the ranked results of the chunks of text that are relevant to the question user asked.

-Will send that chunk as context to LLM(OpenAI)

-Then LLM will answer the question based on context that we gave and send the answer back to user with source(Page Number and Pdf Name)
