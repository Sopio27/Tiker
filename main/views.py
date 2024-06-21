from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm, CreateTaskForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Department, Team, Task, Status, Employee
from django.views.generic import UpdateView, DeleteView
from django.db.models import Q
from django.urls import reverse

# Create your views here.
@login_required(login_url='/login')
def index(request):

    query = request.GET.get('q')

    if query:
        departments = Department.objects.filter(Q(DepartmentName__icontains=query))

    else:
        departments = Department.objects.all()

    departments = departments.order_by('id')
    return render(request, 'main/index.html', {"departments": departments})

class TaskUpdateView(UpdateView):

    model = Task
    template_name = 'main/update_task.html'
    fields = ['Title', 'Description', 'TeamId', 'AssignedUserId', 'StatusId', 'PriorityId', 'TaskStartDate', 'TaskDueDate']



    def form_valid(self, form):

        instance = form.save()
        return redirect('team', id_d=instance.TeamId.DepartmentId.id, id_t=instance.TeamId.id)


    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['Title'].label = 'Title'
        form.fields['Description'].label = 'Description'
        form.fields['TeamId'].label = 'Team'
        form.fields['AssignedUserId'].label = 'Assigneee'
        form.fields['StatusId'].label = 'Status'
        form.fields['PriorityId'].label = 'Priority'
        form.fields['TaskStartDate'].label = 'Start Date'
        form.fields['TaskDueDate'].label = 'Due Date'
        return form


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'main/delete_task.html'

    def get_success_url(self):
        obj = self.get_object()
        id_d = obj.TeamId.DepartmentId.id
        id_t = obj.TeamId.id
        success_url = reverse('team', kwargs={'id_d': id_d, 'id_t': id_t})
        return success_url


@login_required(login_url='/login')
def department(request, id):

    query = request.GET.get('q')

    if query:
        department_teams = Team.objects.filter(Q(TeamName__icontains=query) & Q(DepartmentId=id))

    else:
        department_teams = Team.objects.filter(DepartmentId=id)

    department = Department.objects.all()

    for j in department:
        if j.id == id:
            requested_department = j
            break

    context = {
        "department_teams": department_teams,
         "requested_department": requested_department
    }

    return render(request, 'main/department.html', context)

@login_required(login_url='/login')
def team(request, id_d, id_t):

    requested_team = Team.objects.all()

    for i in requested_team:
        if i.id == id_t:
            requested_team = i
            break

    column_names = ["Title", "Start date", "Due date", "Assignee", "Priority", "Creator", "Details"]
    status_names = Status.objects.all()

    query = request.GET.get('q')

    if query:
        team_tasks = Task.objects.filter(Q(Title__icontains=query) & Q(TeamId=id_t))

    else:
        team_tasks = Task.objects.filter(TeamId=id_t)

    context = {
        "requested_team": requested_team,
        "team_tasks": team_tasks,
        "column_names": column_names,
        "status_names": status_names
    }

    return render(request, 'main/team.html', context)


@login_required(login_url='/login')
def task_details(request, id):

    requested_task = Task.objects.all()

    for i in requested_task:
        if i.id == id:
            requested_task = i
            break

    column_names = [ "Create Date", "Description", "Creator", "Assignee","Start date", "Due date", "Status","Priority" ]

    context = {
        "requested_task": requested_task,
        "column_names": column_names
    }

    return render(request, 'main/task_details.html', context)

@login_required(login_url='/login')
def create_task(request):

    if request.method == 'POST':

        form = CreateTaskForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.CreatorUserId = request.user
            instance.save()
            form.save_m2m()
            return redirect('team', id_d=instance.TeamId.DepartmentId.id, id_t=instance.TeamId.id)
    else:
        form = CreateTaskForm()

    return render(request, 'main/create_task.html', {'form': form})

@login_required(login_url='/login')
def add_assignee(request, id):
    task = get_object_or_404(Task, pk = id)
    task.AssignedUserId.add(request.user)
    return redirect('team', id_d=task.TeamId.DepartmentId.id, id_t=task.TeamId.id)
#Authentication
def sign_up(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            team = form.cleaned_data.get('team')
            Employee.objects.create(UserName=user, TeamId=team)
            login(request, user)
            return redirect('main')
        else:
            return render(request, 'registration/sign_up.html', {'form':form})

    else:
        form = RegistrationForm(request.POST)
        return render(request, 'registration/sign_up.html', {'form':form})

def logout_user(request):
    logout(request)

    return redirect('login')


