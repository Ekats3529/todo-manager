from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='../frontend')
CORS(app)

tasks = [
    {"id": 1, "title": "Пример задачи", "completed": False}
]

# API
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    if not data or "title" not in data:
        return jsonify({"error": "Требуется title"}), 400
    new_task = {"id": int(max([t["id"] for t in tasks], default=0) + 1),
                "title": data["title"], "completed": False}
    tasks.append(new_task)
    return jsonify(new_task)

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return jsonify({"error": "Задача не найдена"}), 404
    data = request.json
    if "title" in data:
        task["title"] = data["title"]
    if "completed" in data:
        task["completed"] = data["completed"]
    return jsonify(task)

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return jsonify({"success": True})

# Раздача статических файлов frontend
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def serve_frontend(path):
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return "Файл не найден", 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
