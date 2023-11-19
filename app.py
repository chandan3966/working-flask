from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

# Establish a connection to MongoDB
client = MongoClient("mongodb+srv://marrisaichandanms:1qkBBuIrdWoDnBOi@cluster0.ghs94r3.mongodb.net/")
db = client["todomodel"]
collection = db["users"]

@app.route('/users', methods=['POST'])
def create_user():
    user = request.json  # Retrieve user data from the request body
    result = collection.insert_one(user)  # Insert user data into the collection
    return jsonify({'message': 'User created successfully', 'id': str(result.inserted_id)})

@app.route('/users', methods=['GET'])
def get_users():
    users = [user for user in collection.find({}, {'_id': False})]  # Retrieve all users from the collection
    return jsonify(users)

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = collection.find_one({'_id': ObjectId(id)}, {'_id': False})  # Retrieve a specific user by id
    if user:
        return jsonify(user)
    else:
        return jsonify({'message': 'User not found'})

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    user = request.json  # Retrieve updated user data from the request body
    result = collection.update_one({'_id': ObjectId(id)}, {'$set': user})
    return jsonify({'message': 'User updated successfully', 'id': str(result.upserted_id)})

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        user_id = ObjectId(id)
        if collection.find_one({'_id': ObjectId(id)}):
            result = collection.delete_one({'_id': ObjectId(id)})
            if result.deleted_count > 0:
                return jsonify({'message': 'User deleted successfully'})
            else:
                return jsonify({'message': 'User not found'})
        else:
            return jsonify({'message': 'User not found'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run()