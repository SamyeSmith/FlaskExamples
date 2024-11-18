from pymongo import MongoClient

client = MongoClient("mongodb+srv://2405327:Samye1234@cluster0.jzy7v.mongodb.net/toolsDB?retryWrites=true&w=majority")
db = client.toolsDB
comments_collection = db.comments

# Test insertion
comment_data = {
    "tool_id": "64abcd1234ef567890123456",  # Replace with a valid ObjectId string from your tools collection
    "user": "Test User",
    "rating": 5,
    "comment": "This is a test comment."
}

# Insert a comment to create the collection if it doesn’t exist
result = comments_collection.insert_one(comment_data)
print(f"Inserted comment ID: {result.inserted_id}")