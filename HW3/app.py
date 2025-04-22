import os
import pymongo
from flask import Flask, request, jsonify, render_template
from bson import ObjectId

app = Flask(__name__)

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['loan_system']
applications_collection = db['applications']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/add_application', methods=['POST'])
def add_application():
    data = request.get_json()
    name = data.get('name')
    zipcode = data.get('zipcode')

    application = {
        'name': name,
        'zipcode': zipcode,
        'status': 'received',
        'notes': []
    }

    result = applications_collection.insert_one(application)
    return jsonify({'message': 'Application submitted successfully', 'application_id': str(result.inserted_id)})

@app.route('/api/status/<application_id>', methods=['GET'])
def check_status(application_id):
    application = applications_collection.find_one({'_id': ObjectId(application_id)})
    if application:
        return jsonify({'status': application['status']})
    else:
        return jsonify({'message': 'Application not found'}), 404

@app.route('/api/change_status', methods=['POST'])
def change_status():
    data = request.get_json()
    application_id = data.get('application_id')
    new_status = data.get('new_status')

    result = applications_collection.update_one(
        {'_id': ObjectId(application_id)},
        {'$set': {'status': new_status}}
    )

    if result.matched_count:
        return jsonify({'message': 'Status updated'})
    else:
        return jsonify({'message': 'Application not found'}), 404

@app.route('/api/add_note', methods=['POST'])
def add_note():
    data = request.get_json()
    application_id = data.get('application_id')
    note = data.get('note')

    result = applications_collection.update_one(
        {'_id': ObjectId(application_id)},
        {'$push': {'notes': note}}
    )

    if result.matched_count:
        return jsonify({'message': 'Note added'})
    else:
        return jsonify({'message': 'Application not found'}), 404

@app.route('/api/details/<application_id>', methods=['GET'])
def get_details(application_id):
    application = applications_collection.find_one({'_id': ObjectId(application_id)})
    if application:
        application['_id'] = str(application['_id'])  # Convert ObjectId to string
        return jsonify(application)
    else:
        return jsonify({'message': 'Application not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
