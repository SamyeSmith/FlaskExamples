from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId

app = Flask(__name__)

# MongoDB configuration
client = MongoClient("mongodb+srv://yashcsltu:IF06UkFiiEBNVTxp@cluster0.b99hgkl.mongodb.net/toolsDB")
db = client.toolsDB
tools_collection = db.tools
comments_collection = db.comments

# 1. Landing page
@app.route('/')
def home():
    return render_template('home.html')

# 2. Add tools page
@app.route('/add_tool', methods=['GET', 'POST'])
def add_tool():
    if request.method == 'POST':
        tool_data = {
            "name": request.form['name'],
            "image_url": request.form['image_url'],
            "description": request.form['description'],
            "product_url": request.form['product_url']
        }
        tools_collection.insert_one(tool_data)
        return redirect(url_for('view_tools'))
    return render_template('add_tool.html')

# 3. View all tools page
@app.route('/view_tools', methods=['GET'])
def view_tools():
    tools = tools_collection.find()
    return render_template('view_tools.html', tools=tools)

# 4. Search for a tool page
@app.route('/search_tool', methods=['GET', 'POST'])
def search_tool():
    if request.method == 'POST':
        search_query = request.form['tool_name']
        tool = tools_collection.find_one({"name": {"$regex": search_query, "$options": "i"}})
        if tool:
            comments = comments_collection.find({"tool_id": str(tool["_id"])})
            return render_template('tool_details.html', tool=tool, comments=comments)
        return "Tool not found", 404
    return render_template('search_tool.html')

# 5. Add comments for a tool
@app.route('/add_comment/<tool_id>', methods=['POST'])
def add_comment(tool_id):
    try:
        comment_data = {
            "tool_id": tool_id,
            "user": request.form['user'],
            "rating": int(request.form['rating']),
            "comment": request.form['comment']
        }
        comments_collection.insert_one(comment_data)
        return redirect(url_for('search_tool'))
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
