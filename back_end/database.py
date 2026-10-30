
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/")

client = MongoClient(MONGO_URL)

db = client["restaurant_management"]

# Collections
users_collection = db["users"]
categories_collection = db["categories"]
menu_collection = db["menuItems"]
tables_collection = db["tables"]
reservations_collection = db["reservations"]
orders_collection = db["orders"]
payments_collection = db["payments"]
feedback_collection = db["feedback"]
chatbot_collection = db["chatbotMessages"]

print("MongoDB database connected successfully!")
