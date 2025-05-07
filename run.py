from flask import Flask, jsonify, request 
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

client = MongoClient("mongodb+srv://ayomiidoherty:G9rpgjxPiJf0XL0z@cluster0.n491gmo.mongodb.net/")
db = client.hospital_database

# Helper function to convert ObjectId to string
def convert_objectid(data):
    if isinstance(data, ObjectId):
        return str(data)
    elif isinstance(data, dict):
        return {k: convert_objectid(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_objectid(item) for item in data]
    else:
        return data

@app.route('/patients', methods=['GET'])
def get_patients():
    patients = list(db.patients.find({}, {'_id': 0}))  # Retrieve all patients, excluding MongoDB's default `_id`
    return jsonify(patients), 200

if __name__ == '__main__':
    app.run(debug=True)