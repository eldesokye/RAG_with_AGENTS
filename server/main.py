# from fastapi import FastAPI, UploadFile, File, Form, Request
# from fastapi.responses import JSONResponse
# from fastapi.middleware.cors import CORSMiddleware
# from fastembed import TextEmbedding
# from langchain_core.documents import Document
# from langchain.schema import BaseRetriever
# from pinecone import Pinecone
# from pydantic import Field
# from typing import List, Optional
# from modules.load_vectorstore import load_vectorstore
# from modules.llm import get_llm_chain
# from modules.query_handlers import query_chain
# from logger import logger
# import os

# app = FastAPI(title="RagBot2.0")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,      # ← was ["*"], invalid
#     allow_methods=["*"],
#     allow_headers=["*"]
# )

# # Initialize once at startup — not per request
# embed_model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
# from pinecone import Pinecone

# pc = Pinecone(api_key="pcsk_288wVV_CMNMhUJ5X9WDWbM8Rvcp8JdqYUswcez4BktKedvtZgfcFPY1hftCn9Mfgj7SYt1")
# index = pc.Index("simple-rag")


# @app.middleware("http")
# async def catch_exception_middleware(request: Request, call_next):
#     try:
#         return await call_next(request)
#     except Exception as exc:
#         logger.exception("UNHANDLED EXCEPTION")
#         return JSONResponse(status_code=500, content={"error": str(exc)})


# @app.post("/upload_pdfs/")
# async def upload_pdfs(files: List[UploadFile] = File(...)):
#     try:
#         logger.info(f"received {len(files)} files")
#         load_vectorstore(files)
#         logger.info("documents added to vectorstore")
#         return {"message": "Files processed and vectorstore updated"}
#     except Exception as e:
#         logger.exception("Error during pdf upload")
#         return JSONResponse(status_code=500, content={"error": str(e)})


# @app.post("/ask/")
# async def ask_question(question: str = Form(...)):
#     try:
#         logger.info(f"user query: {question}")

#         # Embed the question
#         embedded_query = list(embed_model.embed([question]))[0]

#         # Query Pinecone
#         res = index.query(vector=embedded_query.tolist(), top_k=3, include_metadata=True)

#         # Convert to LangChain Documents
#         docs = [
#             Document(
#                 page_content=match["metadata"].get("text", ""),
#                 metadata=match["metadata"]
#             ) for match in res["matches"]
#         ]

#         # Simple retriever
#         class SimpleRetriever(BaseRetriever):
#             tags: Optional[List[str]] = Field(default_factory=list)
#             metadata: Optional[dict] = Field(default_factory=dict)

#             def __init__(self, documents: List[Document]):
#                 super().__init__()
#                 self._docs = documents

#             def _get_relevant_documents(self, query: str) -> List[Document]:
#                 return self._docs

#         retriever = SimpleRetriever(docs)
#         chain = get_llm_chain(retriever)
#         result = query_chain(chain, question)

#         logger.info("query successful")
#         return result

#     except Exception as e:
#         logger.exception("Error processing question")
#         return JSONResponse(status_code=500, content={"error": str(e)})


# @app.get("/test")
# async def test():
#     return {"message": "Testing successful..."}


from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from modules.load_vectorstore import PERSIST_DIR, load_vectorstore
from modules.llm import get_llm_chain
from modules.query_handlers import query_chain
from logger import logger
from output.Active_research_agent import Active_research_agent
from output.costs_failures import ReActAgent as Costs_ReActAgent


app = FastAPI(title="Simple RAG")


## allow frontend to call our API without CORS issues
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,      # ← was ["*"], invalid
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.middleware("http")
async def catch_exception_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        logger.exception("UNHANDLED EXCEPTION")
        return JSONResponse(status_code=500, content={"error": str(exc)})
    


@app.post("/upload_pdfs/")
async def upload_pdfs(files: List[UploadFile] = File(...)):
    try:
        logger.info(f"received {len(files)} files")
        load_vectorstore(files)
        logger.info("documents added to vectorstore")
        return {"status": "success", "message": "Files processed and vectorstore updated"}
    except Exception as e:
        logger.exception("Error during pdf upload")
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})
    


@app.post("/ask/")
async def ask_question(question: str = Form(...)):
    try:
        logger.info(f"user query: {question}")
        from langchain.vectorstores import Chroma
        from langchain.embeddings import HuggingFaceEmbeddings
        from modules.load_vectorstore import PERSIST_DIR
        vectorstore = Chroma(persist_directory=PERSIST_DIR, embedding_function=HuggingFaceEmbeddings(model_name="all-MiniLM-L12-v2"))
        chain = get_llm_chain(vectorstore)
        result = query_chain(chain, question)
        logger.info("query successful")
        return {"status": "success", "result": {
            "answer": result.get("result", "No answer returned"),
            "sources": result.get("sources", [])
        }}
    except Exception as e:
        logger.exception("Error processing question")
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})


@app.get("/search/")
async def search(query: str,user_id: str = "default"):
    try:
        logger.info(f"search query: {query}")
        research_agent = Active_research_agent(message=query)
        result = research_agent.research(user_id=user_id)
        cost = research_agent.costs_failures(user_id=user_id)
        logger.info("search successful")
        return {"status": "success", "result": result , "cost_analysis": cost}
    except Exception as e:
        logger.exception("Error processing search")
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})


@app.get("/suport/")
async def search(query: str,user_id: str = "default"):
    try:
        logger.info(f"search query: {query}")
        research_agent = Active_research_agent(message=query)
        result = research_agent.handle_customer_with_memory(user_id=user_id)
        cost = research_agent.costs_failures(user_id=user_id)
        logger.info("search successful")
        return {"status": "success", "result": result , "cost_analysis": cost}
    except Exception as e:
        logger.exception("Error processing search")
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})
