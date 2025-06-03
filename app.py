from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = 'data/queue.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"queue": [], "eaten": []}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/queue", methods=["GET"])
def get_queue():
    return jsonify(load_data())

@app.route("/api/queue", methods=["POST"])
def add_to_queue():
    name = request.json.get("name", "").strip()
    if not name:
        return jsonify({"error": "Name required"}), 400
    data = load_data()
    data["queue"].append(name)
    save_data(data)
    return jsonify(data)

@app.route("/api/eat", methods=["POST"])
def eat_user():
    index = int(request.json.get("index", -1))
    data = load_data()
    if 0 <= index < len(data["queue"]):
        eaten_user = data["queue"].pop(index)
        data["eaten"].append(eaten_user)
        save_data(data)
    return jsonify(data)

@app.route("/api/clear", methods=["POST"])
def clear_all():
    data = {"queue": [], "eaten": []}
    save_data(data)
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
