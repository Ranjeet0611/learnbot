from rich.console import Console
from src.learnbot.constants import console_styles
from pymongo import MongoClient, ASCENDING

console = Console(force_terminal=True)


def get_database(db_name, uri="mongodb://localhost:27017/"):
    try:
        console.print(f"[INFO] Connecting to MongoDB at {uri}...", style=console_styles.console_blue_styles)
        client = MongoClient(uri)
        console.print(f"[SUCCESS] Connected to database: {db_name}", style=console_styles.console_green_styles)
        return client[db_name]
    except Exception as e:
        console.print(f"[ERROR] Database connection failed: {e}", style=console_styles.console_red_styles)
        return None


def get_kafka_topics():
    try:
        client = get_database("kafka_learning", "mongodb://localhost:27017/")
        if client is None:
            console.print("[ERROR] No database client available.", style=console_styles.console_red_styles)
            return None
        collection = client.get_collection("kafka_topics")
        document = collection.find({"isRead": False}).sort({"day": ASCENDING}).limit(1)
        document = list(document)
        if not document:
            console.print("[WARNING] No unread Kafka topics found.", style=console_styles.console_yellow_styles)
            return None
        title = document[0]['title']
        concepts = document[0]['concepts']
        new_concept = ""
        for concept in concepts:
            is_read = concept['isRead']
            if not is_read:
                new_concept = new_concept + concept['name']
                update_kafka_topic_as_read(collection, document, concept, concepts)
                break
        console.print(f"[SUCCESS] Kafka topic fetched: {title}", style=console_styles.console_green_styles)
        return {'title': title, 'concept': new_concept}
    except Exception as e:
        console.print(f"[ERROR] Failed to fetch Kafka topics: {e}", style=console_styles.console_red_styles)
        return None


def check_all_concept_read(concepts):
    try:
        for concept in concepts:
            if not concept['isRead']:
                return False
        return True
    except Exception as e:
        console.print(f"[ERROR] Error checking concepts: {e}", style=console_styles.console_red_styles)
        return False


def update_kafka_topic_as_read(collection, document, concept, concepts):
    try:
        concept['isRead'] = True
        if check_all_concept_read(concepts):
            collection.update_one({"_id": document[0]['_id']}, {"$set": {"isRead": True}})
            console.print(f"[INFO] All concepts read. Marked topic as read.", style=console_styles.console_blue_styles)
        collection.update_one({"concepts.name": concept['name']}, {"$set": {"concepts": concepts}})
        console.print(f"[SUCCESS] Updated concept as read: {concept['name']}", style=console_styles.console_green_styles)
    except Exception as e:
        console.print(f"[ERROR] Failed to update concept as read: {e}", style=console_styles.console_red_styles)
