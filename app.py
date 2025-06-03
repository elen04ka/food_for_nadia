from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)

DATA_FILE = 'data.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"queue": [], "eaten": []}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/queue', methods=['GET'])
def get_queue():
    data = load_data()
    return jsonify(data)

@app.route('/api/queue', methods=['POST'])
def add_to_queue():
    data = load_data()
    name = request.json.get('name', '').strip()
    if not name:
        return jsonify({"error": "Name is required"}), 400
    if name.lower() == 'nadia':
        return jsonify({"error": "Name 'nadia' is reserved"}), 400
    data['queue'].append(name)
    save_data(data)
    return jsonify({"message": f"{name} додано в чергу"})

@app.route('/api/eat', methods=['POST'])
def eat_user():
    data = load_data()
    index = request.json.get('index')
    if index is None or not (0 <= index < len(data['queue'])):
        return jsonify({"error": "Invalid index"}), 400
    eaten_name = data['queue'].pop(index)
    data['eaten'].append(eaten_name)
    save_data(data)
    return jsonify({"message": f"{eaten_name} з'їдений", "eatenName": eaten_name})

@app.route('/api/clear', methods=['POST'])
def clear_data():
    data = {"queue": [], "eaten": []}
    save_data(data)
    return jsonify({"message": "Дані очищено"})

if __name__ == '__main__':
    app.run(debug=True)
