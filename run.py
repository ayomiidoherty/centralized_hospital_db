from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
from flask_cors import CORS
import os 

app = Flask(__name__)
CORS(app)

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client.hospital_database

admin_api_key = "d9C5bK-2z6K9cA8gWq5iWdHi7Yp1PwT4u0bAoR3nPdV"

def convert_objectid(data):
    if isinstance(data, ObjectId):
        return str(data)
    elif isinstance(data, dict):
        return {k: convert_objectid(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_objectid(item) for item in data]
    else: 
        return data 

@app.route('/')
def index():
    return "Welcome to the Flask API!"

@app.route('/medical_records', methods=['GET'])
def get_all_records():
    api_key = request.headers.get('x-api-key')

    # Admin key required to access all records
    if api_key != admin_api_key:
        return jsonify({"error": "Unauthorized"}), 403

    try:
        # Get all medical records from the database
        records = list(db.medical_records.find())
        return jsonify(convert_objectid(records)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Route to get a specific patient's record
@app.route('/medical_records/<string:patient_id>', methods=['GET'])
def get_patient(patient_id):
    # Get the hospital name (this could be passed via the body or a different method)
    hospital_name = request.headers.get('x-hospital-name')  # For example, pass the hospital name here
    
    if not hospital_name:
        return jsonify({"error": "Hospital name missing"}), 400

    # Check if the hospital has been granted access to the patient's record
    access_request = db.access_requests.find_one({"hospital_name": hospital_name, "patient_id": patient_id, "status": "approved"})
    
    if not access_request:
        return jsonify({"error": "Access not granted or pending approval"}), 403

    try:
        # Get the specific patient's record from the database
        patient = db.medical_records.find_one({"patient_id": patient_id})
        if not patient:
            return jsonify({"error": "Patient not found"}), 404

        return jsonify(convert_objectid(patient)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Route for hospitals to request access to a patient's record
@app.route('/request_access', methods=['POST'])
def request_access():


    # Get hospital info and patient info from the request body
    hospital_name = request.json.get('hospital_name')
    patient_id = request.json.get('patient_id')
    reason = request.json.get('reason')

    # Create the access request
    access_request = {
        "hospital_name": hospital_name,
        "patient_id": patient_id,
        "reason": reason,
        "status": "pending"  # This status will be updated once admin approves
    }

    # Insert the access request into the database
    db.access_requests.insert_one(access_request)

    return jsonify({"message": "Access request submitted successfully"}), 201

# Route for the admin to approve an access request
@app.route('/approve_access/<access_request_id>', methods=['PATCH'])
def approve_access(access_request_id):
    api_key = request.headers.get('x-api-key')

    # Admin authentication
    if api_key != admin_api_key:
        return jsonify({"error": "Unauthorized"}), 403
    
    request_id = request.json.get('request_id')
    status = request.json.get('status')

    # Update the access request status to 'approved'
    result = db.access_requests.update_one(
        {"_id": ObjectId(access_request_id)},
        {"$set": {"status": "approved"}}
    )

    if result.matched_count == 0:
        return jsonify({"error": "Access request not found"}), 404

    return jsonify({"message": "Access request approved"}), 200

# Run Flask App
if __name__ == '__main__':
    app.run(debug=True)