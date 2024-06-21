from django.db import models
from django.contrib.auth.models import User

class EmployeeRole(models.Model):

    # UserTypeId = models.AutoField(primary_key=True)
    UserTypeName = models.CharField(max_length=50)

    class Meta:
        db_table = 'DimEmployeeType'

    def __str__(self):
        return self.UserTypeName

class Department(models.Model):

    DepartmentName = models.CharField(max_length=256)
    ImageSource = models.CharField(null=True, blank=True)

    class Meta:
        db_table = 'DimDepartment'

    def __str__(self):
        return self.DepartmentName

class Team(models.Model):

    TeamName = models.CharField(max_length=256)
    TeamDescription = models.TextField(null=True, blank=True)
    DepartmentId = models.ForeignKey(Department, to_field='id', on_delete=models.CASCADE)

    class Meta:
        db_table = 'DimTeam'

    def __str__(self):
        return self.TeamName

class Status(models.Model):

    StatusName = models.CharField(max_length=50)

    class Meta:
        db_table = 'DimStatus'

    def __str__(self):
        return self.StatusName

class Priority(models.Model):

    PriorityName = models.CharField(max_length=20)

    class Meta:
        db_table = 'DimPriority'

    def __str__(self):
        return self.PriorityName

class Task(models.Model):

    Title = models.CharField(max_length=60)
    Description = models.TextField()
    CreateDate = models.DateField(auto_now_add=True)
    CreatorUserId = models.ForeignKey(User,  related_name='creator', on_delete=models.CASCADE)
    AssignedUserId = models.ManyToManyField(User, related_name='users')
    TeamId = models.ForeignKey(Team, to_field='id', on_delete=models.CASCADE)
    TaskStartDate = models.DateField(null=True, blank=True)
    TaskDueDate = models.DateField(null=True, blank=True)
    StatusId = models.ForeignKey(Status, to_field='id', on_delete=models.CASCADE)
    PriorityId = models.ForeignKey(Priority, to_field='id', on_delete=models.CASCADE)

    def assigned_users_list(self):
        return ", ".join([str(p) for p in self.AssignedUserId.all()])

    class Meta:
        db_table = 'Task'

    def __str__(self):
        return self.Title

class Employee(models.Model):

    UserName = models.OneToOneField(User, on_delete=models.CASCADE)
    TeamId = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Employee'

    def __str__(self):
        return self.UserName.username