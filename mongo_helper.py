from pymongo import MongoClient
from bson import ObjectId

client = MongoClient('mongodb://localhost:27017/')
db = client['TEST_DB']
books_collection = db['books']

def insertBookToMongo(new_book):
    """Add a new book to the MongoDB collection."""
    result = books_collection.insert_one(new_book)
    return str(result.inserted_id)