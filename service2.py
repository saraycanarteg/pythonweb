from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
import os

app = Flask(__name__)

# MongoDB connection
MONGO_URI = "mongodb+srv://mrsproudd:mrsproudd@cluster0.ad7fs0q.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client['users_db']
users_collection = db['users']

@app.route('/')
def home():
    return jsonify({"message": "Users API - Service 2"})

@app.route('/users', methods=['GET'])
def get_users():
    users = list(users_collection.find())
    for user in users:
        user['_id'] = str(user['_id'])
    return jsonify(users)

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    try:
        user = users_collection.find_one({"_id": ObjectId(id)})
        if user:
            user['_id'] = str(user['_id'])
            return jsonify(user)
        return jsonify({"error": "User not found"}), 404
    except:
        return jsonify({"error": "Invalid ID"}), 400

@app.route('/users', methods=['POST'])
def create_user():
    new_user = {
        "name": request.json.get("name"),
        "email": request.json.get("email")
    }
    result = users_collection.insert_one(new_user)
    new_user['_id'] = str(result.inserted_id)
    return jsonify(new_user), 201

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    try:
        update_data = {
            "name": request.json.get("name"),
            "email": request.json.get("email")
        }
        result = users_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
        if result.modified_count:
            return jsonify({"message": "User updated"})
        return jsonify({"error": "User not found"}), 404
    except:
        return jsonify({"error": "Invalid ID"}), 400

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        result = users_collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count:
            return jsonify({"message": "User deleted"})
        return jsonify({"error": "User not found"}), 404
    except:
        return jsonify({"error": "Invalid ID"}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 4007))
    app.run(host='0.0.0.0', port=port)