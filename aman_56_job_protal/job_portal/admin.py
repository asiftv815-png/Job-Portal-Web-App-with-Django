from django.contrib import admin
from job_portal.models import *

# Register your models here.
admin.site.register([
    User,
    RecruiterModel,
    SeekerModel,
    Category,
    JobApplyModel,
    JobPostModel,
])