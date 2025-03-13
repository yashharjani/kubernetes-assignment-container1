from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# Persistent storage directory
STORAGE_DIR = "/yash_PV_dir"
os.makedirs(STORAGE_DIR, exist_ok=True)

@app.route('/store-file', methods=['POST'])
def store_file():
    data = request.get_json()

    if not data or 'file' not in data or 'data' not in data:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    file_name = data['file']
    file_content = data['data']

    if not file_name.strip():
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    file_path = os.path.join(STORAGE_DIR, file_name)

    try:
        with open(file_path, 'w') as f:
            f.write(file_content)

        return jsonify({"file": file_name, "message": "Success."}), 201
    except Exception as e:
        return jsonify({"file": file_name, "error": "Error while storing the file to the storage."}), 500

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()

    if not data or 'file' not in data or not data['file']:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    file_name = data['file']
    file_path = os.path.join(STORAGE_DIR, file_name)

    # Check if the file exists in persistent volume
    if not os.path.exists(file_path):
        return jsonify({"file": file_name, "error": "File not found."}), 404

    try:
        response = requests.post('http://container2:7000/sum', json=data)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as error:
        return jsonify({'error': str(error)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000, debug=True)