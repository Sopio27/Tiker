from django.contrib import admin
from .models import EmployeeRole, Department, Team, Task, Status, Priority, Employee

# Register your models here.

admin.site.register(EmployeeRole)
admin.site.register(Department)
admin.site.register(Team)
admin.site.register(Task)
admin.site.register(Status)
admin.site.register(Priority)
admin.site.register(Employee)
