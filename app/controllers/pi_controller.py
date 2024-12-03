from flask import Blueprint, request, jsonify
from app.services.pi_service import PiCalculationService
from app.models.pi_calculation import PiCalculationRequest
from app.utils.decorators import require_auth
from app.controllers.statistics_controller import log_request
from app.utils.queue_manager import QueueManager
from asgiref.sync import async_to_sync
import asyncio
import time
import threading

pi_blueprint = Blueprint('pi', __name__)
pi_service = PiCalculationService()
queue_manager = QueueManager()

def run_async_task(coro):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()

@pi_blueprint.route('/pi', methods=['POST'])
@require_auth
def calculate_pi():
    start_time = time.time()
    data = request.get_json()
    try:
        # Extract parameters
        simulations = data.get('simulations', 1000)
        concurrency = data.get('concurrency', 1)
        is_async = data.get('async', False)
        
        # Create request object
        pi_request = PiCalculationRequest(
            simulations=simulations,
            concurrency=concurrency
        )
        
        if is_async:
            # Enqueue task for async processing
            task_id = async_to_sync(queue_manager.enqueue_calculation)(data)
            
            def process_task():
                async def async_process():
                    try:
                        result = await pi_service.calculate_pi(pi_request)
                        await queue_manager.set_result(task_id, {
                            "pi": result.pi,
                            "simulations": result.simulations,
                            "concurrency": result.concurrency,
                            "execution_time": result.execution_time
                        })
                    except Exception as e:
                        await queue_manager.set_result(task_id, {"error": str(e)})
                
                run_async_task(async_process())
            
            # Start background thread
            thread = threading.Thread(target=process_task)
            thread.daemon = True
            thread.start()
            
            return jsonify({
                "task_id": task_id,
                "status": "pending"
            })
        
        # Synchronous calculation
        result = async_to_sync(pi_service.calculate_pi)(pi_request)
        execution_time = time.time() - start_time
        
        # Log successful request
        log_request('/pi', execution_time, True, data)
        
        return jsonify({
            "pi": result.pi,
            "simulations": result.simulations,
            "concurrency": result.concurrency,
            "execution_time": result.execution_time
        })
        
    except ValueError as e:
        execution_time = time.time() - start_time
        log_request('/pi', execution_time, False, data)
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        execution_time = time.time() - start_time
        log_request('/pi', execution_time, False, data)
        return jsonify({"error": str(e)}), 500 