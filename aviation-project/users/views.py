from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from urllib.parse import urlencode
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm , UserUpdateForm , CompanyRegisterForm , CompanyUpdateForm , CompanyProfileForm
from django.core.files.storage import FileSystemStorage
from pyresparser import ResumeParser
from django.conf import settings
import os
from django.http import HttpResponse
from django.contrib.auth.models import User , auth
from .models import Users , CompanyProfile , Skill
from .models import workExperience
from .models import educationExperience
from postjob.models import Jobform
from apply.models import *
from django.shortcuts import get_object_or_404
import datetime
from datetime import datetime
from .decorators import unauthenticated_user , allowed_users
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate , login
from postjob.models import Jobform , Jobtype, Category
from django.http import HttpResponse , HttpResponseRedirect
import psycopg2,pytz
from django.core.mail import send_mail, EmailMessage
from .filters import UsersFilter
from events_app.models import EventListing


# Create your views here.

def applicationStatus_view(request , *args , **kwargs):
    return render(request , "userprofile/applicationStatus.html" , {})


@login_required()
@allowed_users(allowed_roles=['company_owner'])
def sendEmailToJobseeker(request, pk):
    jobseeker = Users.objects.get(id=pk)
    company_profile = CompanyProfile.objects.get(user_id=request.user.id)

    if request.method == "POST":
        message = request.POST['message']

        #send email
        send_mail(
            'From ' + company_profile.name + ' at Aviation Job Board', #subject
            message + '\n\n To reply to this message please use the ' + company_profile.name + ' personal email: ' + request.user.email, #message
            settings.EMAIL_HOST_USER, #from email
            [jobseeker.Email], #to email
        )
        #Alternate way of sending an email that also works
        # message = request.POST['message']
        # msg = EmailMessage('From ' + company_profile.name,
        #                    message, to=[jobseeker.Email])
        # msg.send()

        messages.success(request, f'Message was sent')
        return redirect('user_search_page')

    return render(request, "users/sendEmailToJobseeker.html", {'jobseeker': jobseeker})

@login_required()
@allowed_users(allowed_roles=['company_owner'])
def user_search_page(request):
    all_users = Users.objects.all().order_by('name')

    myFilter = UsersFilter(request.GET, queryset=all_users)
    all_users = myFilter.qs

    #send email
    # send_mail(
    #
    #
    # )

    context = {
        'all_users': all_users,
        'myFilter': myFilter,
    }

    return render(request, "users/user_search.html", context)


@unauthenticated_user
def register(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            # user = Users(Username = username, Email = email)

            group = Group.objects.get(name='jobseeker')
            user.groups.add(group)

            user.save()
            messages.success(request , f'Account Successfully Created! You May Now Create Your Profile')
            user = authenticate(username=form.cleaned_data['username'] ,
                                password=form.cleaned_data['password1'] ,
                                )
            login(request , user)
            user = Users(Username=username , Email=email)
            user.save()
            return redirect('review')
    else:
        form = UserRegisterForm()
        # request.session.flush()
    return render(request , 'users/register.html' , {'form': form})


@unauthenticated_user
def company_register(request):
    if request.method == 'POST':
        form = CompanyRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            # first_name = form.cleaned_data.get('name')
            # phoneNumber = form.cleaned_data.get('phoneNumber')
            # address = form.cleaned_data.get('address')
            # company_description = form.cleaned_data.get('company_description')
            # user = User(name=name, PhoneNumber=phoneNumber
            #              , address=address, company_description=company_description)

            group = Group.objects.get(name='company_owner')
            user.groups.add(group)

            user.save()
            # cp.save()
            messages.success(request , f'Account Successfully Created! You May Now Create Your Profile')
            user = authenticate(username=form.cleaned_data['username'] ,
                                password=form.cleaned_data['password1'] ,
                                )
            login(request , user)
            return redirect('company_profile_creator')
    else:
        form = CompanyRegisterForm()
    return render(request , 'users/company_register.html' , {'form': form})


def addCompanyProfile(request):
    cp_form = CompanyProfileForm(request.POST)
    if request.method == 'POST':
        cp_form = CompanyProfileForm(request.POST)
        if cp_form.is_valid():
            name = cp_form.cleaned_data['name']
            phoneNumber = cp_form.cleaned_data['phoneNumber']
            address = cp_form.cleaned_data['address']
            company_description = cp_form.cleaned_data['company_description']
            id = request.user.id
            # user = request.user
            # if user_id is not None:
            #    request.session.delete('user_id')
            #    comp = CompanyProfile.objects.get(user_id=user_id)
            # else:
            #    comp = Client.objects.create(user=user)
            # company_profile = CompanyProfile.objects.get(name=name, phoneNumber=phoneNumber
            #             , address=address, company_description=company_description)
            # cp.save()
            # company_profile.save()
            CompanyProfile.objects.filter(user_id=id).update(name=name , phoneNumber=phoneNumber , address=address ,
                                                             company_description=company_description)
            messages.success(request , f'Your account has been updated!')
            return redirect('company_profile')
        else:
            cp_form = CompanyProfileForm(request.POST)

    context = {
        'cp_form': cp_form ,
    }

    return render(request , 'users/company_profile_creator.html' , context)


@login_required()
@allowed_users(allowed_roles=['company_owner'])
def company_profile(request):
    u_form = UserUpdateForm(instance=request.user)
    cp_Update_form = CompanyUpdateForm(instance=request.user.companyprofile)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST , instance=request.user)
        cp_Update_form = CompanyUpdateForm(request.POST , request.FILES , instance=request.user.companyprofile)
        if u_form.is_valid() and cp_Update_form.is_valid():
            # username = u_form.cleaned_data.get('username')
            # email = u_form.cleaned_data.get('email')
            # first_name = form.cleaned_data.get('name')
            # phoneNumber = form.cleaned_data.get('phoneNumber')
            # address = form.cleaned_data.get('address')
            # company_description = form.cleaned_data.get('company_description')
            # user = CompanyProfile(Username=username, Email=email)
            # user.save()
            u_form.save()
            cp_Update_form.save()
            messages.success(request , f'Your account has been updated!')
            return redirect('company_profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        cp_Update_form = CompanyUpdateForm(instance=request.user.companyprofile)

    # if request.method == 'POST':
    #     cp_Update_form = CompanyUpdateForm(request.POST, instance=request.CompanyProfile)
    #     if cp_Update_form():
    #         name = cp_form.cleaned_data['name']
    #         phoneNumber = cp_form.cleaned_data['phoneNumber']
    #         address = cp_form.cleaned_data['address']
    #         company_description = cp_form.cleaned_data['company_description']
    #         company_profile = CompanyProfile(name=name, phoneNumber=phoneNumber
    #                     , address=address, company_description=company_description)

    company_profile = CompanyProfile.objects.get(user_id=request.user.id)
    jobs = Jobform.objects.filter(company=company_profile.id)
    events = EventListing.objects.filter(company=company_profile.id)

    company_profile = CompanyProfile.objects.get(user_id=request.user.id)
    print(company_profile.user.email)
    # if request.POST.get("delete_job"):
    #     jobs.object.filter(id=request.GET.get('id')).delete()
    #     return redirect('company_profile')

    delete_job = request.GET.get('d_job')
    delete_event = request.GET.get('d_event')
    if delete_job is not None:
        job = Jobform.objects.filter(id=delete_job).first()
        count = job.category.count - 1
        Category.objects.filter(name=job.category.name).update(count=count)
    Jobform.objects.filter(id=delete_job).delete()
    EventListing.objects.filter(id=delete_event).delete()

    context = {
        'u_form': u_form ,
        'cp_Update_form': cp_Update_form ,
        'company_profile': company_profile ,
        'jobs': jobs ,
        'events': events,
        'delete_job': delete_job ,
        'delete_event': delete_event,
    }

    return render(request , 'users/company_profile.html' , context)


@login_required()
def resume(request):
    parsed_info = {}
    if request.method == 'POST' and 'upload' in request.POST:
        uploaded_file = request.FILES['resume']
        if uploaded_file.name.endswith(".pdf") or uploaded_file.name.endswith(".docx"):
            user = Users.objects.get(Username=request.user.username)
            if QuickApply.objects.filter(user=user).exists():
                qa = QuickApply.objects.get(user=user)
                qa.replace_resume(uploaded_file)
            else:
                qa = QuickApply(user=user, resume=uploaded_file)
                qa.save()
            parsed_info = ResumeParser(qa.resume.path).get_extracted_data()
            request.session['parsed_name'] = parsed_info.pop('name')
            request.session['parsed_email'] = parsed_info.pop('email')
            request.session['parsed_number'] = parsed_info.pop('mobile_number')
            request.session['parsed_skills'] = parsed_info.pop('skills')
            request.session['parsed_status'] = True
            return redirect('review')
        else:
            print("Invalid Request")
    return render(request , 'users/resume.html' , parsed_info)


def ParseSkills(request , skills):
    skill_len = len(skills)
    count = 0
    connection = psycopg2.connect(user=settings.DATABASES['default']['USER'] ,
                                  password=settings.DATABASES['default']['PASSWORD'] ,
                                  host=settings.DATABASES['default']['HOST'] ,
                                  port=settings.DATABASES['default']['PORT'] ,
                                  database=settings.DATABASES['default']['NAME'])
    user = Users.objects.get(Username=request.user.username)
    try:
        cursor = connection.cursor()
        postgres_relational_query = """INSERT INTO users_users_skills (USERS_ID, SKILL_ID) VALUES (%s,%s)"""
        postgres_insert_query = """INSERT INTO users_skill (SKILL_NAME) VALUES (%s)"""
        postgres_select_query = """SELECT id FROM users_skill WHERE skill_name = (%s)"""
        for i in range(skill_len):
            cursor.execute(postgres_select_query , (skills[i] ,))
            in_table = cursor.fetchone()
            if (in_table is not None):
                skill_insert = (user.id , (in_table[0]))
                cursor.execute(postgres_relational_query , skill_insert)
                count = count + 1
            else:
                cursor.execute(postgres_insert_query , (skills[i] ,))
                connection.commit()
                cursor.execute(postgres_select_query , (skills[i] ,))
                in_table = cursor.fetchone()
                skill_insert = (user.id , (in_table[0]))
                cursor.execute(postgres_relational_query , skill_insert)
                count = count + 1
            connection.commit()
    except (Exception , psycopg2.Error)as error:
        if connection:
            print("Failed to insert" , error)
    finally:
        if (connection):
            connection.commit()
            cursor.close()
            connection.close()
            print(count , "Record inserted")
    return


def getSkills(username):
    postgres_select_query = """SELECT skill_id FROM users_users_skills WHERE users_id = (%s)"""
    connection = psycopg2.connect(user=settings.DATABASES['default']['USER'] ,
                                  password=settings.DATABASES['default']['PASSWORD'] ,
                                  host=settings.DATABASES['default']['HOST'] ,
                                  port=settings.DATABASES['default']['PORT'] ,
                                  database=settings.DATABASES['default']['NAME'])
    user = Users.objects.get(Username=username)
    skills = []
    try:
        cursor = connection.cursor()
        cursor.execute(postgres_select_query , (user.id ,))
        skill_ids = cursor.fetchall()
        skill_len = len(skill_ids)
        for i in range(skill_len):
            skills.append((Skill.objects.get(id=skill_ids[i][0])).skill_name)
    except (Exception , psycopg2.Error)as error:
        if connection:
            print("Connection failed" , error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
    return skills


def removeSkill(users_id , skill):
    postgres_delete_query = """DELETE FROM users_users_skills WHERE users_id = %s AND skill_id = %s"""
    postgres_select_query = """SELECT id FROM users_skill WHERE skill_name = (%s)"""
    connection = psycopg2.connect(user=settings.DATABASES['default']['USER'] ,
                                  password=settings.DATABASES['default']['PASSWORD'] ,
                                  host=settings.DATABASES['default']['HOST'] ,
                                  port=settings.DATABASES['default']['PORT'] ,
                                  database=settings.DATABASES['default']['NAME'])
    try:
        cursor = connection.cursor()
        cursor.execute(postgres_select_query , (skill ,))
        in_table = cursor.fetchone()
        delete = (users_id , in_table[0] ,)
        print(delete)
        cursor.execute(postgres_delete_query , (users_id , in_table[0]))
        print(cursor.statusmessage)

    except (Exception , psycopg2.Error)as error:
        if connection:
            print("Connection failed" , error)
    finally:
        if (connection):
            connection.commit()
            cursor.close()
            connection.close()

@login_required()
@allowed_users(allowed_roles=['jobseeker'])
def review(request):
    if request.method == 'GET':
        using_resume = request.session.get('parsed_status', None)
        user = Users.objects.filter(Username=request.user.username)
        if not user.exists():
            user = Users(Username=request.user.username , Email=request.user.email)
            user.save()
        print(using_resume)
        if using_resume is None:
            using_resume = False
        else:
            using_resume = True
        # if request.session['parsed_status'] in request.session:
        #     using_resume = True
        # else:
        #     using_resume = False
        if 'parsed_skills' in request.session:
            context = {'name': request.session.get('parsed_name') ,
                       'email': request.session.get('parsed_email') ,
                       'mobile_number': request.session.get('parsed_number') ,
                       'parsed_skills': request.session.get('parsed_skills'),
                        'nickname': request.session.get('parsed_nickName'),
                        'address': request.session.get('parsed_address'),
                        'using_resume': using_resume}
        else:
            context = {
                'name': "",
                'email': "",
                'mobile_number': "",
                'parsed_skills': [],
                'nickname':"",
                'address': "",
                'using_resume': using_resume
            }
        return render(request , 'users/review.html' , context)
    if request.method == 'POST':
        request.session['parsed_name'] = request.POST.get('name')
        request.session['parsed_email'] = request.POST.get('email')
        request.session['parsed_number'] = request.POST.get('phone')
        request.session['parsed_nickName'] = request.POST.get('nickname')
        request.session['parsed_address'] = request.POST.get('address')
        request.session['parsed_status'] = True
        if 'save' in request.POST:
            ParseSkills(request , request.session['parsed_skills'])
            user = Users.objects.filter(Username=request.user.username)
            if not user.exists():
                user = Users(Username=request.user.username, Email=request.user.email)
                user.save()
                user = Users.objects.filter(Username=request.user.username)
            user.update(
                name=request.session.get('parsed_name'), nickName=request.session.get('parsed_nickName'),
                Email=request.session.get('parsed_email') , phoneNumber=request.session.get('parsed_number') ,
                address=request.session.get('parsed_address')
            )
            if 'parsed_skills' in request.session:
                request.session.modified = True
                del request.session['parsed_name']
                del request.session['parsed_email']
                del request.session['parsed_number']
                del request.session['parsed_nickName']
                del request.session['parsed_address']
                del request.session['parsed_status']
                del request.session['parsed_skills']
            #Flush parsed data
            return redirect('userProfile-home')
        elif 'add' in request.POST:
            if 'parsed_skills' in request.session:
                skills = request.session.get('parsed_skills')
            else:
                skills = []
            add_skill = request.POST.get('addSkill')
            if add_skill != '':
                skills.append(add_skill)
            request.session['parsed_skills'] = skills
            print(request.session['parsed_skills'])
            return redirect('review')
        elif 'delete' in request.POST:
            skills = request.session.get('parsed_skills')
            remove_skill = request.POST.get('delete')
            skills.remove(remove_skill)
            request.session['parsed_skills'] = skills
            return redirect('review')
    return render(request , 'users/review.html' , context = {'name': request.session.get('parsed_name') ,
                       'email': request.session.get('parsed_email') ,
                       'mobile_number': request.session.get('parsed_number') ,
                       'parsed_skills': request.session.get('parsed_skills'),
                        'nickname': request.session.get('parsed_nickName'),
                        'address': request.session.get('parsed_address')})

@login_required()
@allowed_users(allowed_roles=['jobseeker'])
def jobseeker_profile_view(request):
    users = Users.objects.filter(Username=request.user.username)
    if not users.exists():
        print(request.user.username)
        user = Users(Username=request.user.username , Email=request.user.email)
        user.save()
    users = Users.objects.filter(Username=request.user.username)
    works = workExperience.objects.filter(Username=request.user.username)
    educations = educationExperience.objects.filter(Username=request.user.username)
    skills = getSkills(request.user.username)
    if request.method == 'POST' and 'editProfile' in request.POST:
        fullname = request.POST['name']
        nickname = request.POST['nickname']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        thisuser = Users.objects.filter(Username=request.user.username).update(name=fullname , nickName=nickname ,
                                                                               Email=email , phoneNumber=phone ,
                                                                               address=address)
        thatuser = User.objects.get(username=request.user.username , password=request.user.password)
        thatuser.email = email
        thatuser.save()
    if request.method == 'POST' and 'deleteWork' in request.POST:
        obj = works.get(comment=request.POST['comments'] , job=request.POST['job'] , company=request.POST['company'] ,
                        Username=request.user.username).delete()
    if request.method == 'POST' and 'deleteEducation' in request.POST:
        obj = educations.get(duration=request.POST['duration'] , title=request.POST['title'] ,
                             school=request.POST['school'] , Username=request.user.username).delete()
    if request.method == 'POST' and 'deleteSkill' in request.POST:
        id = (Users.objects.get(Username=request.user.username)).id
        removeSkill(id , request.POST.get('deleteSkill'))
        skills = getSkills(request.user.username)
        redirect('userProfile-home')
    if request.method == 'POST' and 'submitSkill' in request.POST:
        ParseSkills(request , [request.POST['newSkill']])
        skills = getSkills(request.user.username)
        redirect('userProfile-home')
    if request.method == 'POST' and 'uploadResume' in request.FILES:
        print(request.FILES['uploadResume'])
        user = Users.objects.get(Username=request.user.username)
        if QuickApply.objects.filter(user=user).exists():
            qa = QuickApply.objects.get(user=user)
            qa.replace_resume(request.FILES['uploadResume'])
        else:
            print('qa not found')
            resume = request.FILES['uploadResume']
            # fs = FileSystemStorage(location=(settings.MEDIA_ROOT + "\\" + str(request.user.id) + "\\"))
            # filename = fs.save('resume.pdf', resume)
            qa = QuickApply(user=user, resume=request.FILES['uploadResume'])
            qa.save()
            print(qa)
    applications = Application.objects.filter(applicant=users.first()).all()
    # apptest =
    # application_statuses = ApplicationStatus.objects.filter(application=applications.id)
    print('rendering')
    return render(request , 'userProfile/profile2.html' ,
                  {'users': users , 'works': works , 'educations': educations , 'applications': applications ,
                   'skills': skills})

@login_required()
@allowed_users(allowed_roles=['company_owner'])
def view_jobseeker_profile(request, user_id):
    x = user_id
    user = Users.objects.filter(id=x)
    username = user.first().Username
    skills = getSkills(username)
    works = workExperience.objects.filter(Username=username)
    educations = educationExperience.objects.filter(Username=username)
    context={
        'users':user,
        'works':works,
        'educations':educations,
        'skills':skills
    }
    return render(request, 'userProfile/profileViewer.html', context)
def trysearch(request):
    jobs = Jobform.objects.all()
    if request.method == 'POST' and 'apply' in request.POST:
        title = request.POST['name']
        jobtype = request.POST['type']
        description = request.POST['description']
        username = request.user.username
        # application = ApplicationStatus(title=title, jobtype=jobtype, description=description, username=username)
        # application.save()
    return render(request , 'trysearch.html' , {'jobs': jobs})
@login_required()
def quickApply(request, job_id):
    user = Users.objects.get(Username = request.user.username)
    job = Jobform.objects.get(id=job_id)
    company = CompanyProfile.objects.get(id=job.company.id)
    files = []
    qa = QuickApply.objects.filter(user=user)
    if qa.exists():
        qa = qa.first()
        fileName = qa.resume.name
        if '/' in fileName:
            fileName = qa.resume.name.split('/')
            fileName = fileName[len(fileName) - 1]
        files.append(fileName)
        if not (Application.objects.filter(applicant=user,job=job).exists()):
            app = Application(applicant=user, job = job, company = company, files = files)
            app.save()
            path = settings.MEDIA_ROOT + "\\" + str(user.id) + "\\application_files\\" + str(app.id)
            fs = FileSystemStorage(location=path)
            print('Saving to '+ path)
            file = qa.resume.open()
            print(fileName)
            fs.save(fileName,file)
            file = qa.resume.close()
            messages.success(request , f'Successfully Applied for the Job.')
        else:
            messages.warning(request ,
                             f'You have already applied to this job.')
            print('Already Applied')
    else:
        messages.warning(request , f'Quick Apply not initialized, please go to your user profile and upload a resume.')
        return redirect('userProfile-home')
    return redirect('search_page')
@login_required()
@allowed_users(allowed_roles=['jobseeker'])
def applyjob(request , job_id):
    if request.method == 'POST' and 'submit' in request.POST:
        x = (request.FILES).getlist('file')
        users = Users.objects.filter(Username=request.user.username).first()
        if users is None:
            return redirect('userProfile-home')
        job = Jobform.objects.filter(id=job_id).first()
        company = CompanyProfile.objects.filter(id=job.company.id).first()
        files = []
        if len(x) > 0:
            if len(x) > 1:
                for i in x:
                    files.append(i.name)
            else:
                files.append(x[0].name)
            app = Application(applicant=users , job=job , company=company , files=files)
            print(app)
            app.save()
            path = settings.MEDIA_ROOT + "\\" + str(users.id) + "\\application_files\\" + str(app.id)
            fs = FileSystemStorage(location=path)
            for i in x:
                fs.save(i.name , i)
        else:
            app = Application(applicant=users , job=job , company=company , files=files)
            print(app)
            app.save()

        return redirect('userProfile-home')
        ##SOME ISSUES WITH FS IDK HOW TO FIX THE ISSUE OF HAVING DUPLICATE FILES IN SAME APPLICATION##
    return render(request , 'applyjob.html')


def getFiles(applications):
    app_files = dict()
    for x in applications:
        user = User.objects.get(username=x.applicant.Username)
        for y in x.files:
            path = "/media/" + str(user.id) + "/application_files/" + str(x.id) + "/" + y

            test = {
                y:path
            }
            if x.id in app_files:
                app_files[x.id].append(test)
            else:
                app_files[x.id] = [test]
    return app_files


def viewApplications(request):
    company = CompanyProfile.objects.get(id=request.user.id)
    jobs = Jobform.objects.filter(company=company.id)
    applications = Application.objects.filter(company=company)
    applicationStatus = {
        "Unread": len(Application.objects.filter(status='SB')) ,
        "Rejected": len(Application.objects.filter(status='RJ')) ,
        "Reviewed": len(Application.objects.filter(status='PR')) ,
        "Accepted": len(Application.objects.filter(status='AC'))
    }
    context = {
        'jobs': jobs ,
        'applications': applications ,
        'app_count': applicationStatus ,
        'files': getFiles(applications)
    }
    if request.method == 'POST':
        app_id = request.POST.get('app')
        status = request.POST.get('status')
        app = Application.objects.get(id=app_id)
        app.status = status
        app.save()
        return redirect('company_applications')
    return render(request , 'viewApplications.html' , context)

def uploadProfilePic_view(request):
    users = Users.objects.filter(Username=request.user.username)
    if request.method == 'GET':
        return render(request, 'users/uploadProfilePic.html')
    if request.method == 'POST' and 'upload' in request.POST:
            profilePic = request.FILES['image']
            thisuser = Users.objects.get(Username=request.user.username)
            thisuser.image = profilePic
            thisuser.save()
            tz_NY = pytz.timezone('America/New_York')
            datetime_NY = datetime.now(tz_NY)
            #send_mail(
            #    'You have received a notification from Aviation Job Portal',
            #    'You have successfully updated your profile picture in your Aviation Job Portal Profile at '+datetime_NY.strftime("%H:%M:%S")+' EST. If this is incorrect please contact AJP support.',
            #    'DoNotReply.AJP@gmail.com',
            #    [request.user.email],
            #    fail_silently=False,
            #)
            return redirect('userProfile-home')
    return render(request, 'userProfile/profile2.html')

######################################################################################################################################################################################
######################################################################################################################################################################################
######################################################################################################################################################################################
######################################################################################################################################################################################
######################################################################################################################################################################################
######################################################################################################################################################################################
######################################################################################################################################################################################
######################################################################################################################################################################################
######################################################################################################################################################################################


def addWorkingExperience(request):
    if request.method == 'POST':
        job = request.POST['job']
        years = request.POST['years']
        company = request.POST['company']
        comment = request.POST['comment']
        if request.user.is_authenticated:
            name = request.user.username
            findwork = workExperience.objects.filter(job=job , years=years , company=company , comment=comment ,
                                                     Username=name)
            if not findwork.exists():
                works = workExperience(job=job , years=years , company=company , comment=comment , Username=name)
                works.save()
            else:
                messages.info(request , 'Already have a same record.')
                return redirect('/addwork')
            return redirect('/userprofile')
    else:
        return render(request , 'userProfile/addwork.html')


def addEducationExperience(request):
    if request.method == 'POST':
        title = request.POST['title']
        duration = request.POST['duration']
        school = request.POST['school']
        major = request.POST['major']
        if request.user.is_authenticated:
            name = request.user.username
            findEducation = educationExperience.objects.filter(title=title , duration=duration , school=school ,
                                                               major=major , Username=name)
            if not findEducation.exists():
                education = educationExperience(title=title , duration=duration , school=school , major=major ,
                                                Username=name)
                education.save()
            else:
                messages.info(request , 'Already have a same record.')
                return redirect('/addeducation')
            return redirect('/userprofile')
    else:
        return render(request , 'userProfile/addeducation.html')


def about(request):
    return render(request , 'userProfile/profile2.html')
