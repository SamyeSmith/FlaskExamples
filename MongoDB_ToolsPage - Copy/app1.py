from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId  # To handle invalid ObjectId errors

app = Flask(__name__)

# MongoDB configuration
client = MongoClient("mongodb+srv://yashcsltu:IF06UkFiiEBNVTxp@cluster0.b99hgkl.mongodb.net/toolsDB")
db = client.toolsDB
tools_collection = db.tools
comments_collection = db.comments

@app.route('/')
def index():
    tools = tools_collection.find()
    return render_template('index.html', tools=tools)

@app.route('/add_tool', methods=['POST'])
def add_tool():
    tool_data = {
        "name": request.form['name'],
        "image_url": request.form['image_url'],
        "description": request.form['description'],
        "product_url": request.form['product_url']
    }
    tools_collection.insert_one(tool_data)
    return redirect(url_for('index'))

@app.route('/tool/<tool_id>', methods=['GET'])
def tool_details(tool_id):
    try:
        # Attempt to convert tool_id to ObjectId and fetch tool details
        tool = tools_collection.find_one({"_id": ObjectId(tool_id)})
        if not tool:
            return "Tool not found", 404

        # Fetch comments for the tool
        comments = comments_collection.find({"tool_id": tool_id})
        return render_template('tool_details.html', tool=tool, comments=comments)

    except InvalidId:
        return "Invalid Tool ID", 400  # Handle invalid ObjectId

    except Exception as e:
        return str(e), 500  # Handle any other unexpected errors

@app.route('/add_comment/<tool_id>', methods=['POST'])
def add_comment(tool_id):
    try:
        # Insert the comment
        comment_data = {
            "tool_id": tool_id,  # Store tool_id as a string in the comments collection
            "user": request.form['user'],
            "rating": int(request.form['rating']),
            "comment": request.form['comment']
        }

        comments_collection.insert_one(comment_data)

        # Fetch the tool details and comments
        try:
            tool = tools_collection.find_one({"_id": ObjectId(tool_id)})  # Convert tool_id to ObjectId
            if not tool:
                return "Tool not found", 404

            comments = comments_collection.find({"tool_id": tool_id})
            return render_template('tool_details.html', tool=tool, comments=comments)
        
        except InvalidId:
            return "Invalid Tool ID", 400  # Handle invalid ObjectId conversion

    except Exception as e:
        return str(e), 500  # Handle unexpected errors

if __name__ == '__main__':
    app.run(debug=True)
