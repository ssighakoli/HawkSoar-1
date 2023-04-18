from django import forms
from django.forms import ModelForm
from db_connect.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

class UserSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['user_type', 'first_name', 'last_name', 'email', 'password1', 'password2']

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput)

class CoursesForm(forms.ModelForm):
    class Meta:
        model = Course_Registered
        fields = ['Course_id', 'Course_Name']

class EventForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = ('event_name', 'event_date')
        widgets = {
            'event_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }




# class User_register_Form(forms.ModelForm):

#     Account_Type_choices = ( 
#     ("1", "Mentor"),
#     ("2", "Tutor"),
#     ("3", "Student")
#     )
#     User_Email = forms.EmailField(label = "Email")
#     Password = forms.CharField(label = "Passcode",max_length = "8")
#     Account_Type = forms.ChoiceField(choices  = Account_Type_choices)
#     class Meta:
#         model = User_register
#         fields = '__all__'