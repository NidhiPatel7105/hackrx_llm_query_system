# app/vectorstore.py
import pinecone
from sentence_transformers import SentenceTransformer
from app.config import PINECONE_API_KEY, PINECONE_ENV

model = SentenceTransformer('all-MiniLM-L6-v2')

pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)

INDEX_NAME = "hackrx-insure"
if INDEX_NAME not in pinecone.list_indexes():
    pinecone.create_index(INDEX_NAME, dimension=384)

def build_pinecone_index(chunks, namespace):
    index = pinecone.Index(INDEX_NAME)
    ids_texts = []
    for i, chunk in enumerate(chunks):
        ids_texts.append((f"{namespace}_{i}", chunk['text']))
    # Create embeddings
    emb = model.encode([text for _, text in ids_texts]).tolist()
    # Upsert
    to_upsert = list(zip([_id for _id, _ in ids_texts], emb))
    index.upsert(vectors=to_upsert, namespace=namespace)
    # Store mapping for clause_ids, etc.
    return ids_texts

def semantic_search(query, namespace, chunks, top_k=3):
    index = pinecone.Index(INDEX_NAME)
    q_emb = model.encode([query]).tolist()[0]
    result = index.query(vector=q_emb,
        namespace=namespace,
        filter=None, top_k=top_k, include_values=False)
    # Map back to chunk (by ID)
    answers = []
    for match in result.matches:
        idx = int(match.id.split("_")[-1])
        answers.append(chunks[idx])
    return answers
