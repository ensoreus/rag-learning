import chromadb

from chromadb.utils import embedding_functions
default_ef =  embedding_functions.DefaultEmbeddingFunction()

chroma_client = chromadb.PersistentClient(path="./db/chroma_resist")

collection = chroma_client.get_or_create_collection("my_story", embedding_function=default_ef)

documents = [
    {"id": "doc1",  "text": "Hello World!"},
    {"id": "doc2", "text": "How are you today?"},
    {"id": "doc3",  "text": "Goodbye, see you later!"}, 
    {"id": "doc4", "text": "Microsoft is a technology company that develops stuff"}
]

for doc in documents:
    collection.upsert(ids=doc["id"], documents=[doc["text"]])

query_text = "Age of the Earth"

results = collection.query(
    query_texts=[query_text],
    n_results=2
)
