import os
from dotenv import load_dotenv
import chromadb
from openai import OpenAI
from chromadb.utils import embedding_functions
load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=openai_key,
    model_name="text-embedding-3-small"
)
collection_name = "document_qa_collection"
chroma_client = chromadb.PersistentClient("./db3/chromadb_openai")
collection = chroma_client.get_or_create_collection(
    name=collection_name,
    embedding_function=openai_ef
)

client = OpenAI(api_key=openai_key)

def load_documents_from_directory(directory_path):
    print("==== Loading documents from directory ====")
    documents = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            with open(
                    os.path.join(directory_path,  filename)
            ) as file:
                documents.append({"id":  filename,  "text":  file.read()})
    return documents

def split_text(text,  chunk_size=1000,  chunk_overlap=20):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start: end])
        start = end - chunk_overlap
    return chunks

def load_documents():
    directory_path = "./raw_docs/"
    documents = load_documents_from_directory(directory_path)

    print(f"=== Loaded documents {len(documents)} ===")

    chunked_documents = []
    for doc in documents:
        chunks = split_text(doc["text"])
        print("=== Splitting docs into chunks ===")
        for i,  chunk in enumerate(chunks):
            chunked_documents.append({"id": f"{doc['id']}_chunk{i+1}",  "text": chunk})

def get_openai_embeddings(text):
    response = client.embeddings.create(input=text, model="text-embedding-3-small")
    embedding = response.data[0].embedding
    print("=== Generating embbeddings ===")
    return embedding

def embed_docs():
    for doc in chunked_documents:
        doc["embedding"] = get_openai_embeddings(doc["text"])

def insert_to_db():
    for doc in chunked_documents:
        print("=== Inserting into database ===")
        collection.upsert(
            ids=doc["id"],
            documents=[doc["text"]],
            embeddings=[doc["embedding"]]
        )

def init_database():
    load_documents()
    embed_docs()
    insert_to_db()


def query_documents(query_text):
    results = collection.query(query_texts=[query_text],  n_results=3)
    relevant_chunks = [doc for sublist in results["documents"] for doc in sublist]
    print("==== Returning relevant chunks ====")
    return relevant_chunks

    #for idx, document in enumerate(results["documents"][0]):
    #    doc_id = results["ids"][0][idx]
    #    distance = results["distances"][0][idx]
    #    print(f"Found document chunk {document} with relevance {distance} :{doc_id}\n ==========================================")


def generate_response(question, relevant_chunks):
    context = "\n\n".join(relevant_chunks)
    prompt = (
        "You are an assistant for question-answering tasks. Use the following pieces of "
        "retrieved context to answer the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the answer concise."
        "\n\nContext:\n" + context + "\n\nQuestion:\n" + question
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": prompt,
            },
            {
                "role": "user",
                "content": question,
            },
        ],
    )

    answer = response.choices[0].message
    return answer


question = input()#"give me a brief overview of the articles. Be concise, please."
relevant_chunks = query_documents(question)
answer = generate_response(question, relevant_chunks)
#query_documents("History facts")


print("==== Answer ====")
print(answer.content)
