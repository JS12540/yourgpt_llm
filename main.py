import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File
# Import necessary modules from docchat and related libraries
from docchat import MyGPT4ALL
from knowledgebase import PDFKnowledgeBase 
from langchain.chains import RetrievalQA
from langchain.embeddings import GPT4AllEmbeddings
from knowledgebase import(DOCUMENT_SOURCE_DIRECTORY)


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class QueryRequest(BaseModel):
    query: str

# Initialize components and define constants
GPT4ALL_MODEL_NAME='wizardlm-13b-v1.1-superhot-8k.ggmlv3.q4_0.bin'
GPT4ALL_MODEL_FOLDER_PATH='./llm_model/'
GPT4ALL_BACKEND='llama'
GPT4ALL_ALLOW_STREAMING=True
GPT4ALL_ALLOW_DOWNLOAD=False

llm = MyGPT4ALL(
    model_folder_path=GPT4ALL_MODEL_FOLDER_PATH,
    model_name=GPT4ALL_MODEL_NAME,
    allow_streaming=True,
    allow_download=False
)

embeddings = GPT4AllEmbeddings()

# Use a PDFKnowledgeBase if needed
pdf_source_folder_path = DOCUMENT_SOURCE_DIRECTORY
kb = PDFKnowledgeBase(pdf_source_folder_path)

# Create a retriever
retriever = kb.return_retriever_from_persistent_vector_db(embedder=embeddings)

# Define a QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type='stuff',
    # Use retriever if needed
    retriever=retriever,
    return_source_documents=True,
    verbose=True
)

@app.post('/api/your-ml-endpoint')
async def predict(query_request: QueryRequest):
    try:
        query = query_request.query
        #result = await asyncio.to_thread(qa_chain, query)
        # Call your custom function to answer questions and retrieve source documents
        result = qa_chain(query)
        answer, docs = result['result'], result['source_documents']

        # Prepare the response
        response = {
            "answer": answer,
            "source_documents": [{"source": doc.metadata.get("source", "Unknown"), "content": doc.page_content} for doc in docs]
        }

        return response
    except Exception as e:
        return {"error": str(e)}
    
@app.post("/upload_files")
async def upload(file: UploadFile = File(...)):
    file_type = file.filename.split('.')[-1]
    return file


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)

