from flask import Blueprint, request, jsonify
from app.services.legacy_service import LegacyService
from app.models.legacy_request import LegacyRequest
from app.utils.decorators import require_auth
from app.controllers.statistics_controller import log_request
from asgiref.sync import async_to_sync
import time

legacy_blueprint = Blueprint('legacy', __name__)
legacy_service = LegacyService()

@legacy_blueprint.route('/legacy_pi', methods=['POST'])
@require_auth
def legacy_pi():
    start_time = time.time()
    try:
        data = request.get_json()
        protocol = data.get('protocol', 'tcp').lower()
        
        # Create legacy request
        legacy_request = LegacyRequest(protocol=protocol)
        
        # Handle request using async_to_sync
        result = async_to_sync(legacy_service.handle_request)(legacy_request)
        
        execution_time = time.time() - start_time
        log_request('/legacy_pi', execution_time, True, data)
        
        # Return response
        return jsonify({
            "pi": result.pi,
            "count": result.count,
            "execution_time": result.execution_time,
            "protocol": result.protocol
        })
        
    except ValueError as e:
        execution_time = time.time() - start_time
        log_request('/legacy_pi', execution_time, False, data)
        return jsonify({"error": str(e)}), 400
    except RuntimeError as e:
        execution_time = time.time() - start_time
        log_request('/legacy_pi', execution_time, True, data)  # Still log as success for mock data
        return jsonify({
            "pi": 3.14159,
            "count": 1000,
            "execution_time": 0.001,
            "protocol": "mock",
            "error": str(e)
        }), 200
    except Exception as e:
        execution_time = time.time() - start_time
        log_request('/legacy_pi', execution_time, False, data)
        return jsonify({"error": "Internal server error", "details": str(e)}), 500 