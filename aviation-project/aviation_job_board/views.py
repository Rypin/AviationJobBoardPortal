from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from postjob.models import Jobtype, Jobform, Category
from postjob.forms import PostingForm
from users.decorators import unauthenticated_user, allowed_users
from django.contrib.auth.models import Group
from users.models import User, Users, applicationStatus


# from django import template
#
# register = template.Library()
# #
# @register.filter(name='has_group')
# def has_group(user, group_name):
#     return user.groups.filter(name=group_name).exists()


def base_view(request):
    # filter = True
    # allowed_roles = "jobseeker"
    # if request.user.groups.exists():
    #     group = request.user.groups.all()[0].name
    # if group in allowed_roles:
    #     filter = True

    #User.groups.filter()
    a_filter = True
    wtf = 'wtf'
    # if User.groups.get() == 'jobseeker':
    #     filter = True

    context = {
        'a_filter' : a_filter,
        'wtf' : wtf,
        # 'allowed_roles' : allowed_roles,
    }

    return render(request, "base.html", context=context)

def home_view(request):
    if (request.user.groups.filter(name='jobseeker').exists()):
        return redirect('search_page')
    elif (request.user.groups.filter(name='company_owner').exists()):
        return redirect('company_profile')

    jobtypes = Jobtype.objects.all()
    form = PostingForm()
    return render(request, "index.html", {'jobtypes':jobtypes, 'PostingForm':form})

    context = {
        'jobtypes' : jobtypes,
    }

    return render(request, "index.html", context=context)

def portal_view(request, *args, **kwargs):
    return render(request, "profilePortal.html", {})

def companypage_view(request, *args, **kwargs):
    jobs = Jobform.objects.all()
    if request.method == 'POST' and 'apply' in request.POST:
        title = request.POST['name']
        jobtype = request.POST['type']
        description = request.POST['description']
        username = request.user.username
        application = applicationStatus(title = title, jobtype = jobtype, description = description, username = username)
        application.save()
    return render(request, "CompanyPage.html", {'jobs': jobs})

def chatRoom_view(request, *args, **kwargs):
    return render(request, "chat_room.html", {})

"""
def searchpage_view(request, *args, **kwargs):
    return render(request, "search.html", {}) 
    
"""

def postjob_view(request, *args, **kwargs):
    pj_form = PostingForm(request.POST)
    if request.method == 'POST':
        filled_form = PostingForm(request.POST)
        error = ''
        if filled_form.is_valid():
            if filled_form.cleaned_data['postdate'] > filled_form.cleaned_data['deadlinedate']:
                error = error + 'Error the date posted has to be before the deadline \n'
            if filled_form.cleaned_data['salary_min'] > filled_form.cleaned_data['salary_max']:
                error = error + 'Error the minimum salary has to be less than or equal to the maximum \n'
            if error == '':
                filled_form.save()
                note = '%s Posting has been submitted!!' %(filled_form.cleaned_data['title'],)
                new_form = PostingForm()
                return render(request, 'post_job.html', {'postingform':new_form, 'note':note})
            else:
                form = PostingForm()
                return render(request, 'post_job.html', {'postingform':filled_form, 'error':error})
    else: 
        form = PostingForm()
        return render(request, 'post_job.html', {'postingform':form,})

    #     pj_form = PostingForm(request.POST)
    #     if pj_form.is_valid():
    #         #jobs = Jobform()
    #         title = pj_form.cleaned_data['title']
    #         description = pj_form.cleaned_data['description']
    #         #zipcode = pj_form.cleaned_data['zipcode']
    #         postdate = pj_form.cleaned_data['postdate']
    #         posttime = pj_form.cleaned_data['posttime']
    #         deadlinedate = pj_form.cleaned_data['deadlinedate']
    #         deadlinetime = pj_form.cleaned_data['deadlinetime']
    #         jobtype = pj_form.cleaned_data['jobtype']
    #         user = request.user
    #         Jobform.objects.create(user=user, jobtype=jobtype, title=title, description=description, postdate=postdate, posttime=posttime, deadlinedate=deadlinedate, deadlinetime=deadlinetime)
    #         #jobs.save()
    #         #message.success(request, f'Your job has been posted!')
    #         #pj_form.save()
    #         return redirect('company_profile')
    #     else:
    #         pj_form = PostingForm(request.POST)
    #
    # context = {
    #     'pj_form': pj_form,
    # }
    # return render(request, "post_job.html", context)

def chooseRegister_view(request, *args, **kwargs):
    return render(request, "choose_register.html", {})
