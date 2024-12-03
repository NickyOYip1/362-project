from flask import Blueprint, jsonify, request
from app.utils.queue_manager import QueueManager
from app.utils.decorators import require_auth
from asgiref.sync import async_to_sync

task_blueprint = Blueprint('task', __name__)
queue_manager = QueueManager()

@task_blueprint.route('/task/<task_id>', methods=['GET'])
@require_auth
def get_task(task_id):
    try:
        result = async_to_sync(queue_manager.get_result)(task_id)
        if result is None:
            return jsonify({"error": "Task not found"}), 404
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@task_blueprint.route('/task/cleanup', methods=['POST'])
@require_auth
def cleanup_tasks():
    try:
        max_age = request.json.get('max_age', 3600)  # Default 1 hour
        async_to_sync(queue_manager.cleanup_jobs)(max_age)
        return jsonify({"message": "Cleanup completed"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500