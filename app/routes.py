from flask import Blueprint, request, jsonify
from app.models import Task
from app.database import SessionLocal
from flasgger.utils import swag_from

task_bp = Blueprint("task", __name__)


@task_bp.route("/tasks", methods=["POST"])
@swag_from(
    {
        "tags": ["Tasks"],
        "parameters": [
            {
                "name": "body",
                "in": "body",
                "required": True,
                "schema": {
                    "type": "object",
                    "properties": {"title": {"type": "string"}},
                    "required": ["title"],
                },
            }
        ],
        "responses": {
            200: {
                "description": "Task created successfully",
                "schema": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "title": {"type": "string"},
                        "done": {"type": "boolean"},
                    },
                },
            }
        },
    }
)
def create_task():
    session = SessionLocal()
    data = request.get_json()
    task = Task(title=data["title"])
    session.add(task)
    session.commit()
    session.refresh(task)
    session.close()

    return jsonify({"id": task.id, "title": task.title, "done": task.done})


@task_bp.route("/tasks", methods=["GET"])
@swag_from(
    {
        "tags": ["Tasks"],
        "responses": {
            200: {
                "description": "List of all tasks",
                "schema": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "title": {"type": "string"},
                            "done": {"type": "boolean"},
                        },
                    },
                },
            }
        },
    }
)
def list_tasks():
    session = SessionLocal()
    tasks = session.query(Task).all()
    result = [{"id": t.id, "title": t.title, "done": t.done} for t in tasks]
    session.close()
    return jsonify(result)


@task_bp.route("/tasks/<int:task_id>", methods=["PUT"])
@swag_from(
    {
        "tags": ["Tasks"],
        "parameters": [
            {
                "name": "task_id",
                "in": "path",
                "type": "integer",
                "required": True,
                "description": "ID of the task to update",
            }
        ],
        "responses": {
            200: {
                "description": "Task marked as done",
                "schema": {
                    "type": "object",
                    "properties": {"message": {"type": "string"}},
                },
            },
            404: {"description": "Task not found"},
        },
    }
)
def mark_task_done(task_id):
    session = SessionLocal()
    task = session.get(Task, task_id)
    if not task:
        session.close()
        return jsonify({"error": "Task not found"}), 404

    task.done = True
    session.commit()
    session.close()
    return jsonify({"message": f"Task {task_id} marked as done"})


@task_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
@swag_from(
    {
        "tags": ["Tasks"],
        "parameters": [
            {
                "name": "task_id",
                "in": "path",
                "type": "integer",
                "required": True,
                "description": "ID of the task to delete",
            }
        ],
        "responses": {
            200: {
                "description": "Task deleted successfully",
                "schema": {
                    "type": "object",
                    "properties": {"message": {"type": "string"}},
                },
            },
            404: {"description": "Task not found"},
        },
    }
)
def delete_task(task_id):
    session = SessionLocal()
    task = session.get(Task, task_id)
    if not task:
        session.close()
        return jsonify({"error": "Task not found"}), 404

    session.delete(task)
    session.commit()
    session.close()
    return jsonify({"message": f"Task {task_id} deleted successfully"})
