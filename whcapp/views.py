from django.shortcuts import render,redirect
from django.contrib import messages
from . import models
from .models import Profile, User

def index(request):
    if 'user_id' in request.session:
        return redirect( '/allpostcommunity')
    return render(request,'welcom.html')


def allpostcommunity(request):
    if 'user_id' in request.session:
        context = {
            'first_name':request.session['first_name'],
            'last_name':request.session['last_name'],
            'posts':models.all_posts(),
            'looged_user':models.logged_user(request.session['user_id'])
        }
        return render(request,'allpostcommunity.html',context)
    return redirect('/')   


def register(request):
    if request.method =='POST':
        errors = models.reg_errors(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            user = models.register(request.POST)
            if user is not None:
                if 'user_id' not in request.session:
                    request.session['user_id'] = user.id
                    request.session['first_name'] = user.first_name
                    request.session['last_name'] = user.last_name
                return redirect('/allpostcommunity')
    return redirect('/')


def login(request):
    if request.method=='POST':
        errors = models.login_errors(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            user = models.login(request.POST)
            if user:
                if 'user_id' not in request.session:
                    request.session['user_id'] = user.id
                    request.session['first_name'] = user.first_name
                    request.session['last_name'] = user.last_name
                    return redirect('/allpostcommunity')
    return redirect('/')


def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
        del request.session['first_name']
        del request.session['last_name']
    return redirect('/')


def addpost(request):
    if request.method =='POST':
        errors = models.posts_errors(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            post = models.addpost(request.POST,request.session['user_id'])
            if post is not None:
                return redirect('/allpostcommunity')
    return redirect('/allpostcommunity')


def profile_edit(request):
    context = {
            "country" : "select one",
    }
    return render(request,"profile.html", context)

def profile_view(request, id):
    try:
        current_user = User.objects.get(id = request.session['user_id'])
        current_profile = Profile.objects.filter(user= current_user)
        #print("profile -------->"+current_profile.count())
        if current_profile is not None:
            return redirect("profile_edit")
    except:
        print("exist")
    return render(request,"profile_view_mode.html")

def save_profile_changes(request):
    #print("work is "+request.POST['onoffswitch'])
    name = request.POST['name']
    email = request.POST['email']
    mobile = request.POST['mobile']
    country = request.POST['country']
    education = request.POST['education']
    edu_from = request.POST['edu-from']
    edu_to = request.POST['edu-to']
    experience = request.POST['experience']
    exp_from = request.POST['exp-from']
    exp_to = request.POST['exp-to']
    skills = request.POST['skills']
    links = request.POST['links']
    video_url = request.POST['video-demo-url']

    context = {
            "name" : name,
            "email" : email,
            "mobile" : mobile,
            "country" : country,
            "education" : education,
            "edu_from" : edu_from,
            "edu_to" : edu_to,
            "experience" : experience,
            "exp_from" : exp_from,
            "exp_to" : exp_to,
            "skills" : skills,
            "links" : links,
            "video_url" : video_url,
    }
    current_user = User.objects.get(id = request.session['user_id'])
    current_profile = Profile.objects.filter(user= current_user)
    if current_profile.count() == 0:
        current_user.first_name = name
        current_user.email = email
        current_user.save()
        profile = Profile.objects.create(
        user = current_user,
        mobile = mobile,
        country = country,
        skills = skills,
        education = education,
        education_from = edu_from,
        education_to = edu_to,
        experience = experience,
        experience_from = exp_from,
        experience_to = exp_to,
        links = links,
        video_url = video_url)
        profile.save()
    else:
        current_user.first_name = request.POST['name']
        current_user.email = request.POST['email']
        current_user.profile.mobile = request.POST['mobile']
        current_user.profile.country = request.POST['country']
        current_user.profile.education = request.POST['education']
        current_user.profile.education_from = request.POST['edu-from']
        current_user.profile.education_to = request.POST['edu-to']
        current_user.profile.experience = request.POST['experience']
        current_user.profile.experience_from = request.POST['exp-from']
        current_user.profile.experience_to = request.POST['exp-to']
        current_user.profile.skills = request.POST['skills']
        current_user.profile.links = request.POST['links']
        current_user.profile.video_url = request.POST['video-demo-url']
        current_user.save()
        current_user.profile.save()
        
    return render(request,"profile_view_mode.html", context)

def update_profile(request):
    try:
        current_user = User.objects.get(id = request.session['user_id'])
        #current_profile = Profile.objects.get(user_id= request.session['user_id'])
        context = {
                "name" : current_user.first_name,
                "email" : current_user.email,
                "mobile" : current_user.profile.mobile,
                "country" : current_user.profile.country,
                "education" : current_user.profile.education,
                "edu_from" : current_user.profile.education_from,
                "edu_to" : current_user.profile.education_to,
                "experience" : current_user.profile.experience,
                "exp_from" : current_user.profile.experience_from,
                "exp_to" : current_user.profile.experience_to,
                "skills" : current_user.profile.skills,
                "links" : current_user.profile.links,
                "video_url" : current_user.profile.video_url
        } 
        return render(request,"profile.html", context)
    except:
        return redirect("/profile_edit")


def showposts(request,id):
    context = {
        'post':models.get_post(id),
        'post_data':models.all_posts(),
    }
    return render(request, "community.html",context)

def community(request):
    context = {
        'user':User.objects.get(id=request.session['user_id']),
    }
    return render (request,'community.html',context)

def addcomment(request,id):
    if request.method == 'POST':
        if 'user_id' in request.session:
            comment = models.addcomment(request.POST,id)
            if comment is not None:
                return redirect('/posts/' + str(id))
    return redirect('/community')




