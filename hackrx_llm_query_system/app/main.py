# app/main.py
from fastapi import FastAPI, Request, Header, HTTPException
from app.models import QueryRequest, QueryResponse
from app.document_parser import parse_documents_from_blob_url
from app.vectorstore import build_pinecone_index, semantic_search
from app.llm_reasoner import synthesize_llm_answer
from app.config import AUTHORIZED_TOKEN

app = FastAPI(title="HackRx LLM-Powered Query System")

@app.post("/api/v1/hackrx/run", response_model=QueryResponse)
async def hackrx_run(query: QueryRequest, authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer ") or AUTHORIZED_TOKEN not in authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    # Download & Parse
    chunks = parse_documents_from_blob_url(query.documents)
    namespace = "current_doc_01"  # For prod, generate unique per doc
    build_pinecone_index(chunks, namespace)
    answers = []
    for q in query.questions:
        top_chunks = semantic_search(q, namespace, chunks)
        answer = synthesize_llm_answer(q, top_chunks)
        answers.append(answer)
    return {"answers": answers}
