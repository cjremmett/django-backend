from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Employee
from .serializers import EmployeeSerializer
from .tasks import notify_external_service

@api_view(['POST'])
def create_employee(request):
    """
    Create a new employee
    """
    serializer = EmployeeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

         # Trigger Celery task asynchronously
        notify_external_service.delay(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_employees(request):
    """
    Get employees. Optionally filter by employee_id query parameter.
    """
    employee_id = request.query_params.get('employee_id', None)
    
    if employee_id:
        try:
            employee = Employee.objects.get(employee_id=employee_id)
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data)
        except Employee.DoesNotExist:
            return Response(
                {'error': 'Employee not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    else:
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)
