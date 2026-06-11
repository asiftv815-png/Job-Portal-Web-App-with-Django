from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from job_portal.models import *
from django import forms

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username' , 'display_name' , 'email' ,  'user_type' ,'password1' , 'password2' ]

class LoginForm(AuthenticationForm):
    pass 

class RecruiterForm(forms.ModelForm):
    class Meta:
        model = RecruiterModel
        fields = '__all__'
        exclude = ['recruiter']

class SeekerForm(forms.ModelForm):
    class Meta:
        model = SeekerModel
        fields = '__all__'
        exclude = ['seeker']

class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPostModel
        fields = '__all__'
        exclude = ['posted_by']
 
class JobApplyForm(forms.ModelForm):
    class Meta:
        model = JobApplyModel
        fields = ['resume']

