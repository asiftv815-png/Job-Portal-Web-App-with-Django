from django.urls import path
from job_portal.views import *

urlpatterns = [
    path('register/' , register_page, name='register_page'),
    path('login_page/', login_page, name='login_page'),
    path('logout_page/', logout_page, name= 'logout_page'),

    path('', dashboard, name='dashboard'),
    path('profile_page/', profile_page, name='profile_page'),
    path('update_profile_page/', update_profile_page, name='update_profile_page'),
    
    path('browse_job_page/', browse_job_page, name='browse_job_page'),
    path('post_job_page/', post_job_page, name = 'post_job_page'),
    path('update_job_page/<str:id>/', update_job_page, name='update_job_page'),
    path('delete_job_page/<str:id>/', delete_job_page, name='delete_job_page'),

    path('apply_job_page/<str:id>/', apply_job_page, name='apply_job_page'),
    path('my_applications', my_applications, name='my_applications'),

    path('canditate_list_page/<str:id>/', candidate_list_page, name='candidate_list_page'),
]