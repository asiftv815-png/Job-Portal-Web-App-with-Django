from django.shortcuts import render , redirect
from django.contrib.auth import login, logout
from job_portal.forms import *
from job_portal.views import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.

def register_page(request):
    if request.method == 'POST':
        form_data = RegistrationForm(request.POST)
        if form_data.is_valid():
            form_data.save()
            return redirect('login_page')
    form_data = RegistrationForm()
    context = {
        'form_data' : form_data,
        'form_titlt' : 'Registration Form',
        'form_btn' : 'Register'
    }
    return render(request, 'master/base_form.html' , context)

def login_page(request):
    if request.method == 'POST':
        form_data = LoginForm(request, request.POST)
        if form_data.is_valid():
            user = form_data.get_user()
            login(request, user)
            return redirect('dashboard')
    form_data = LoginForm()
    context = {
        'form_data' : form_data,
        'form_title' : 'Login Form',
        'form_btn' : 'Login',
    }
    return render(request, 'master/base_form.html' , context)

@login_required
def dashboard(request):
    try:
        seeker_data = request.user.seeker_profile
    except:
        return redirect('update_profile_page')
    job_data = JobPostModel.objects.none()
    if request.user.user_type == 'seeker':
        seeker_skill = request.user.seeker_profile.skill_set

        for skill in seeker_skill.split(','):
            cleaned_skill = skill.strip()
            job_data |= JobPostModel.objects.filter(skill_set__icontains = cleaned_skill)
    context = {
        'job_data' : job_data,
    }

    return render(request, 'dashboard.html', context) 

@login_required
def logout_page(request):
    logout(request)
    return redirect('login_page')

@login_required
def profile_page(request):
    return render(request, 'profile.html')

@login_required
def update_profile_page(request):
    current_user = request.user
    if current_user.user_type == 'recruiter':
        try:
            profile_data = RecruiterModel.objects.get(recruiter = current_user)
        except:
            profile_data = None
        if request.method == 'POST':
            form_data = RecruiterForm(request.POST , request.FILES , instance=profile_data)
            if form_data.is_valid():
                data = form_data.save(commit=False)
                data.recruiter = current_user
                data.save()
                return redirect('profile_page')
        form_data = RecruiterForm(instance=profile_data)
    else:
        try:
            profile_data = SeekerModel.objects.get(seeker = current_user)
        except:
            profile_data = None
        if request.method == 'POST':
            form_data = SeekerForm(request.POST , request.FILES , instance=profile_data)
            if form_data.is_valid():
                data = form_data.save(commit=False)
                data.seeker = current_user
                data.save()
                return redirect('profile_page')
        form_data = SeekerForm(instance=profile_data)
    context = {
        'form_data' : form_data,
        'form_title' : 'Update Profile',
        'form_btn' : 'Update',
    }
    return render(request, 'master/base_form.html', context)


def browse_job_page(request):
    current_user = request.user
    search_query = request.GET.get('search_query')

    # Default: show all jobs
    job_data = JobPostModel.objects.all()

    # If recruiter is logged in, show only their jobs
    if current_user.is_authenticated:
        if current_user.user_type == 'recruiter':
            try:
                recruiter_profile = current_user.recruiter_profile
                job_data = JobPostModel.objects.filter(
                    posted_by=recruiter_profile
                )
            except:
                return redirect('update_profile_page')

    # Search functionality
    if search_query:
        job_data = JobPostModel.objects.filter(
            Q(title__icontains=search_query) |
            Q(category__name__icontains=search_query) |
            Q(posted_by__company_name__icontains=search_query)
        )

    context = {
        'job_data': job_data,
    }

    return render(request, 'browse_jobs.html', context)

@login_required
def post_job_page(request):
    try:
        recruiter_data = request.user.recruiter_profile
    except:
        return redirect('update_profile_page')
    
    if request.method=='POST':
        form_data = JobPostForm(request.POST , request.FILES)
        if form_data.is_valid():
            data = form_data.save(commit=False)
            data.posted_by = recruiter_data
            data.save()
            return redirect('browse_job_page')
    form_data = JobPostForm()
    context = {
        'form_data' : form_data,
        'form_title' : 'job post form',
        'form_btn' : 'Post',
    }
    return render(request , 'master/base_form.html' , context)

@login_required
def update_job_page(request ,id):
    try:
        recruiter_data = request.user.recruiter_profile
        job = JobPostModel.objects.get(id = id)
    except:
        return redirect('update_profile_page')
    
    if request.method=='POST':
        form_data = JobPostForm(request.POST , request.FILES , instance=job)
        if form_data.is_valid():
            data = form_data.save(commit=False)
            data.posted_by = recruiter_data
            data.save()
            return redirect('browse_job_page')
    form_data = JobPostForm(instance=job)
    context = {
        'fprm_data' : form_data,
        'form_title' : 'Update job form',
        'form_btn' : 'Update',
    }
    return render(request, 'master/base_form.html' , context)

@login_required
def delete_job_page(request, id):
    try:
        JobPostModel.objects.get(id = id).delete()
        return redirect('browse_job_page')
    except:
        return redirect('browse_job_page')
    
@login_required
def apply_job_page(request , id):
    try:
        seeker_profile = request.user.seeker_profile 
        job = JobPostModel.objects.get(id = id)
    except:
        return redirect('update_profile_page')
    
    if request.method=='POST':
        form_data = JobApplyForm(request.POST ,  request.FILES)
        if form_data.is_valid():
            data = form_data.save(commit=False)
            data.applied_by = seeker_profile
            data.applied_job = job
            data.save()
            return redirect('browse_job_page')
    form_data = JobApplyForm()
    context = {
        'form_data' : form_data,
        'form_title' : 'Apply Job Form',
        'form_btn' : 'Apply',
    }
    return render(request, 'master/base_form.html', context)


def my_applications(request):
    try: 
        my_applications = JobApplyModel.objects.filter(applied_by = request.user.seeker_profile)
    except:
        return redirect('update_profile_view')
    
    context = {
        'application_list' : my_applications,
    }
    return render(request, 'my_applications.html', context)

def candidate_list_page(request, id):
    job_data = JobPostModel.objects.get(id = id)
    candidate_data = JobApplyModel.objects.filter(applied_job = job_data)

    # status update
    if request.method == 'POST':
        candidate_id = request.POST.get('candidate_id')
        status = request.POST.get('status')
        candidate = JobApplyModel.objects.get(id = candidate_id)
        candidate.status = status
        candidate.save()
        return redirect('candidate_list_page', id=id)
    
    context = {
        'candidate_data' : candidate_data,
        'job_data' : job_data,
        'title' : 'candidate_list_page',
    }
    return render(request, 'candidate_list.html', context)


 