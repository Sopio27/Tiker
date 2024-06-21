from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='main'),
    path('department/<int:id>', views.department, name='department'),
    path('department/<int:id_d>/team/<int:id_t>', views.team, name='team'),
    path('task_details/<int:id>', views.task_details, name='task_details'),
    path('task_update/<int:pk>', views.TaskUpdateView.as_view(), name='task_update'),
    path('add_assignee/<int:id>', views.add_assignee, name="add_assignee"),
    path('delete_task/<int:pk>', views.TaskDeleteView.as_view(), name='delete_task'),
    path('create_task/', views.create_task, name='create_task'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('logout/', views.logout_user, name='logout_user'),
    path('add_assignee/<int:id>', views.add_assignee, name='add_assignee')
]
