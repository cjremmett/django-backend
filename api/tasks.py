from celery import shared_task
import requests
import logging
from api.utils import append_to_log

logger = logging.getLogger(__name__)

@shared_task
def notify_external_service(employee_data):
    """
    Celery task to notify an external service when a new employee is created.
    
    Args:
        employee_data: Dictionary containing employee information
    """
    try:
        response = append_to_log('TRACE', str(employee_data))
        
        response.raise_for_status()  # Raise exception for bad status codes
        
        logger.info(
            f"Successfully notified external service for employee {employee_data.get('employee_id')}. "
            f"Status: {response.status_code}, Response: {response.text}"
        )
        
        return {
            'success': True,
            'status_code': response.status_code,
            'response': response.json() if response.headers.get('content-type') == 'application/json' else response.text
        }
        
    except requests.exceptions.Timeout:
        logger.error(f"Timeout when notifying external service for employee {employee_data.get('employee_id')}")
        return {'success': False, 'error': 'Request timeout'}
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error notifying external service for employee {employee_data.get('employee_id')}: {str(e)}")
        return {'success': False, 'error': str(e)}