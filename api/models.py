from django.db import models

class Employee(models.Model):
    employee_id = models.CharField(max_length=100, unique=True, primary_key=True)
    employee_name = models.CharField(max_length=200)
    employee_age = models.IntegerField()
    employee_address = models.TextField()

    def __str__(self):
        return f"{self.employee_id} - {self.employee_name}"

    class Meta:
        db_table = 'employees'
