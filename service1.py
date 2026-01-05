from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
import os

app = Flask(__name__)

# MongoDB connection
MONGO_URI = "mongodb+srv://mrsproudd:mrsproudd@cluster0.ad7fs0q.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client['tasks_db']
tasks_collection = db['tasks']

@app.route('/')
def home():
    return jsonify({"message": "Tasks API - Service 1"})

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = list(tasks_collection.find())
    for task in tasks:
        task['_id'] = str(task['_id'])
    return jsonify(tasks)

@app.route('/tasks/<id>', methods=['GET'])
def get_task(id):
    try:
        task = tasks_collection.find_one({"_id": ObjectId(id)})
        if task:
            task['_id'] = str(task['_id'])
            return jsonify(task)
        return jsonify({"error": "Task not found"}), 404
    except:
        return jsonify({"error": "Invalid ID"}), 400

@app.route('/tasks', methods=['POST'])
def create_task():
    new_task = {
        "title": request.json.get("title"),
        "completed": False
    }
    result = tasks_collection.insert_one(new_task)
    new_task['_id'] = str(result.inserted_id)
    return jsonify(new_task), 201

@app.route('/tasks/<id>', methods=['PUT'])
def update_task(id):
    try:
        update_data = {"completed": request.json.get("completed")}
        result = tasks_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
        if result.modified_count:
            return jsonify({"message": "Task updated"})
        return jsonify({"error": "Task not found"}), 404
    except:
        return jsonify({"error": "Invalid ID"}), 400

@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    try:
        result = tasks_collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count:
            return jsonify({"message": "Task deleted"})
        return jsonify({"error": "Task not found"}), 404
    except:
        return jsonify({"error": "Invalid ID"}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3007))
    app.run(host='0.0.0.0', port=port)