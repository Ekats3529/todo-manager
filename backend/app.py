from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from db import db, Task, init_db 

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app)


@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([t.to_dict() for t in tasks])

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    if not data or "title" not in data:
        return jsonify({"error": "Требуется title"}), 400

    task = Task(title=data["title"])
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict())

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Задача не найдена"}), 404

    data = request.json
    if "title" in data:
        task.title = data["title"]
    if "completed" in data:
        task.completed = data["completed"]

    db.session.commit()
    return jsonify(task.to_dict())

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Задача не найдена"}), 404

    db.session.delete(task)
    db.session.commit()
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
