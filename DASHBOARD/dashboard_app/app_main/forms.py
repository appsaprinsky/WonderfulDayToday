from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import ToDo, Spendings, UploadFile



class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )




class ToDoForm(ModelForm):
    class Meta:
        model = ToDo
        fields = ('titel', 'run', 'importance', 'completed', 'detailed_description', 'deadline_date',)





class SpendingsForm(ModelForm):
    class Meta:
        model = Spendings
        fields = ('type', 'value', 'titel', 'importance', 'detailed_description', 'date_of_spending',)





class UploadFileForm(ModelForm):
    file = forms.FileField(
        label="Select a CSV file",
    )


    class Meta:
        model = UploadFile
        fields = ('title', 'file',)


