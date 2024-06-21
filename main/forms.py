from django import forms
from .models import Task, Employee, Team
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CreateTaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['Title', 'Description', 'TeamId', 'AssignedUserId',
                  'StatusId', 'PriorityId', 'TaskStartDate', 'TaskDueDate']
        widgets = {
            'Title': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Task Title', 'style': 'width: 700px'}),
            'Description': forms.Textarea(attrs={'class': 'form-control',
                                            'placeholder': 'Describe Your Task in Details...', 'rows':5}),
            'TaskStartDate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'TaskDueDate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})}

    def __init__(self, *args, **kwargs):
        super(CreateTaskForm, self).__init__(*args, **kwargs)
        self.fields['TeamId'].label = "Team"
        self.fields['AssignedUserId'].label = "Assignee"
        self.fields['StatusId'].label = "Status"
        self.fields['PriorityId'].label = "Priority"
        self.fields['TaskStartDate'].label = "Start Date"
        self.fields['TaskDueDate'].label = "Due Date"

class RegistrationForm(UserCreationForm):

    email = forms.EmailField(required=True)
    team = forms.ModelChoiceField(queryset=Team.objects.all(),  required=True, empty_label="Select your team")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'team']