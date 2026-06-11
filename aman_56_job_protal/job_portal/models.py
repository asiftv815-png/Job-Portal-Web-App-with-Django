from django.db import models 
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    User_type = [
        ('recruiter' , 'recruiter'),
        ('seeker' , 'seeker'),
    ]

    user_type = models.CharField(max_length=100 , choices=User_type , null=True)
    display_name = models.CharField(max_length=100 , null=True) 

    def __str__(self):
        return f'{self.username}'
    
class RecruiterModel(models.Model):
    recruiter = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        null=True,
        related_name='recruiter_profile',
    )
    company_name = models.CharField(max_length=100 , null=True)
    address = models.TextField(null=True)
    contact = models.EmailField(null=True)
    logo = models.ImageField(upload_to='company_image' , null=True)

    created_at = models.DateField(auto_now_add=True , null=True)
    updated_at = models.DateField(auto_now=True , null=True)

    def __str__(self):
        return f'{self.recruiter}'
    
class SeekerModel(models.Model):
    seeker = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        null=True,
        related_name='seeker_profile',
    )
    address = models.TextField(null=True)
    contact = models.EmailField(null=True)
    profile_image = models.ImageField(upload_to='user_image' , null=True)
    skill_set = models.TextField(null=True)

    created_at = models.DateField(auto_now_add=True , null=True)
    updated_at = models.DateField(auto_now=True , null=True)

    def __str__(self):
        return f'{self.seeker}'

class Category(models.Model):
    name = models.CharField(max_length=100 , null=True)

    def __str__(self):
        return f'{self.name}'
    

class JobPostModel(models.Model):
    posted_by = models.ForeignKey(
        RecruiterModel,
        on_delete=models.CASCADE,
        null=True , 
        related_name= 'job_post',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
    )
    title = models.CharField(max_length=100 , null=True)
    number_of_opening = models.PositiveIntegerField(null=True)
    description = models.TextField(null=True)
    skill_set = models.TextField(null=True)
    salary = models.FloatField(null=True)

    created_at = models.DateField(auto_now_add=True , null=True)
    updated_at = models.DateField(auto_now=True , null=True)

    def __str__(self):
        return f'{self.title}'
    
class JobApplyModel(models.Model):
    applied_by = models.ForeignKey(
        SeekerModel,
        on_delete=models.CASCADE,
        null=True , 
        related_name= 'applied_by_info',
    )
    applied_job = models.ForeignKey(
        JobPostModel,
        on_delete=models.CASCADE,
        null=True,
        related_name='applied_job_info',
    )
    Stetus = [
        ('pending' , 'pending'),
        ('reviewing' , 'reviewing'),
        ('interview' , 'interview'),
        ('rejected' , 'rejected'),
        ('accepted' , 'accepted'),
    ]
    status = models.CharField(max_length=100, choices=Stetus, null=True)
    resume = models.FileField(upload_to='seeker_resume', null=True)
    applied_at = models.DateField(auto_now_add=True , null=True)

    def __str__(self):
        return f'{self.applied_by}-{self.applied_job}'
    
