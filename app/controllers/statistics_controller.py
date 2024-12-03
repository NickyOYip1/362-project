from flask import Blueprint, jsonify, request
from app.services.statistics_service import StatisticsService
from app.utils.decorators import require_auth
from datetime import datetime
from app.models.statistics import RequestStats
from asgiref.sync import async_to_sync

statistics_blueprint = Blueprint('statistics', __name__)
statistics_service = StatisticsService()

@statistics_blueprint.route('/statistics', methods=['GET'])
@require_auth
def get_statistics():
    try:
        stats = async_to_sync(statistics_service.get_statistics)()
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@statistics_blueprint.route('/statistics', methods=['DELETE'])
@require_auth
def clear_statistics():
    try:
        async_to_sync(statistics_service.clear_statistics)()
        return jsonify({"message": "Statistics cleared"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def log_request(endpoint: str, execution_time: float, success: bool, parameters: dict):
    stats = RequestStats(
        endpoint=endpoint,
        timestamp=datetime.now(),
        execution_time=execution_time,
        success=success,
        parameters=parameters
    )
    async_to_sync(statistics_service.add_request)(stats) 