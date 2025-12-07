from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

app = Flask(__name__, 
            template_folder="../frontend/templates", 
            static_folder="../frontend/static")


CORS(app)


tasks = [
    {"id": 1, "title": "Пример задачи", "completed": False}
]

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    if not data or "title" not in data:
        return jsonify({"error": "Требуется title"}), 400

    new_task = {
        "id": int(max([t["id"] for t in tasks], default=0) + 1),
        "title": data["title"],
        "completed": False
    }

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


@app.route('/')
def render_home():
    return render_template('pages/index.html')

@app.route('/tasks-page')
def render_tasks():
    return render_template('pages/tasks.html')

@app.route('/about')
def render_about():
    return render_template('pages/about.html')



if __name__ == '__main__':
    app.run(debug=True, port=5000)
