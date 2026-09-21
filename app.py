import chromadb
chroma_client = chromadb.Client()


collection_name = "TestCollection"
collection = chroma_client.get_or_create_collection(collection_name)

documents = [
    {"id": "a3f9k2", "text": "Штучний інтелект швидко змінює підходи до аналізу великих масивів даних."},
    {"id": "b7x1p4", "text": "Сьогодні в Києві очікується сонячна погода з невеликою хмарністю."},
    {"id": "c2m8q9", "text": "Кава є одним із найпопулярніших напоїв у світі завдяки своєму аромату та бадьорому ефекту."},
    {"id": "d5z3w7", "text": "Космічні місії до Марса вимагають ретельного планування через тривалість польоту."},
    {"id": "e9y6t1", "text": "Football is often called the most popular sport on the planet."},
    {"id": "f4n0r8", "text": "Читання книг допомагає розвивати критичне мислення та розширює словниковий запас."},
    {"id": "g8k5v2", "text": "The stock market experienced significant volatility during the last quarter."},
    {"id": "h1c7l3", "text": "Бджоли відіграють ключову роль в запиленні рослин та підтримці екосистем."},
    {"id": "i6d4s9", "text": "Renewable energy sources are becoming increasingly cost-effective compared to fossil fuels."},
    {"id": "j3b2m6", "text": "Українська кухня славиться борщем, варениками та іншими традиційними стравами."},
    {"id": "k7p9x4", "text": "Quantum computing promises to solve certain problems exponentially faster than classical computers."},
    {"id": "l2f8n1", "text": "Подорожі розширюють світогляд та дозволяють познайомитися з новими культурами."},
    {"id": "m5w3q7", "text": "Climate change continues to affect weather patterns across different regions of the world."},
    {"id": "n9t6y2", "text": "Собаки вважаються одними з найвідданіших домашніх тварин людини."},
    {"id": "o4v1k8", "text": "Machine learning models require large amounts of quality data to perform well."},
    {"id": "p8r5c3", "text": "Мистецтво епохи Відродження суттєво вплинуло на розвиток західної культури."},
    {"id": "q1l7z9", "text": "Electric vehicles are gradually replacing traditional cars in many urban areas."},
    {"id": "r6s2d4", "text": "Медитація та фізичні вправи допомагають знижувати рівень стресу."},
    {"id": "s3g9m8", "text": "The history of ancient civilizations offers valuable lessons for modern society."},
    {"id": "t7h4x1", "text": "Технології блокчейн застосовуються не лише в криптовалютах, а й у логістиці."}
]

for doc in documents:
    collection.upsert(ids=doc["id"], documents=doc["text"])


query = "Machine Learning"

results = collection.query(query_texts=[query], n_results=3)


for idx,  documents in enumerate(results['documents'][0]):
    for doc in documents:
        print(f"- Document ID: { doc['id'] }")
        print(f"- Document text: { doc['text'] }")

