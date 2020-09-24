from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, CompanyRegisterForm, CompanyUpdateForm, CompanyProfileForm, \
    ApplicationForm
from django.core.files.storage import FileSystemStorage
from pyresparser import ResumeParser
from django.conf import settings
import os
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from .models import Users, CompanyProfile, Skill
from .models import workExperience
from .models import educationExperience
from postjob.models import Jobform
from apply.models import *
from django.shortcuts import get_object_or_404
import datetime
from .decorators import unauthenticated_user, allowed_users
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login
from postjob.models import Jobform, Jobtype
from django.http import HttpResponse, HttpResponseRedirect
import psycopg2


# Create your views here.

def applicationStatus_view(request, *args, **kwargs):
    return render(request, "userprofile/applicationStatus.html", {})


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
            messages.success(request, f'Account Successfully Created! You May Now Log In')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


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
            messages.success(request, f'Account Successfully Created! You May Now Create Your Profile')
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password1'],
                                )
            login(request, user)
            return redirect('company_profile_creator')
    else:
        form = CompanyRegisterForm()
    return render(request, 'users/company_register.html', {'form': form})


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
            CompanyProfile.objects.filter(user_id=id).update(name=name, phoneNumber=phoneNumber, address=address,
                                                             company_description=company_description)
            messages.success(request, f'Your account has been updated!')
            return redirect('company_profile')
        else:
            cp_form = CompanyProfileForm(request.POST)

    context = {
        'cp_form': cp_form,
    }

    return render(request, 'users/company_profile_creator.html', context)


@login_required()
@allowed_users(allowed_roles=['company_owner'])
def company_profile(request):
    u_form = UserUpdateForm(instance=request.user)
    cp_Update_form = CompanyUpdateForm(instance=request.user.companyprofile)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        cp_Update_form = CompanyUpdateForm(request.POST, request.FILES, instance=request.user.companyprofile)
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
            messages.success(request, f'Your account has been updated!')
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

    # if request.POST.get("delete_job"):
    #     jobs.object.filter(id=request.GET.get('id')).delete()
    #     return redirect('company_profile')

    delete_job = request.GET.get('d_job')
    Jobform.objects.filter(id=delete_job).delete()

    context = {
        'u_form': u_form,
        'cp_Update_form': cp_Update_form,
        'company_profile': company_profile,
        'jobs': jobs,
        'delete_job': delete_job,
    }

    return render(request, 'users/company_profile.html', context)


@login_required()
def resume(request):
    parsed_info = {}
    if request.method == 'POST' and 'upload' in request.POST:
        uploaded_file = request.FILES['resume']
        if uploaded_file.name.endswith(".pdf") or uploaded_file.name.endswith(".docx"):
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'resumes'))
            new_name = str(request.user.id) + uploaded_file.name
            fs.save(new_name, uploaded_file)
            path = os.path.join(settings.MEDIA_ROOT, 'resumes') + '/' + new_name
            parsed_info = ResumeParser(path).get_extracted_data()
            request.session['parsed_name'] = parsed_info.pop('name')
            request.session['parsed_email'] = parsed_info.pop('email')
            request.session['parsed_number'] = parsed_info.pop('mobile_number')
            request.session['parsed_skills'] = parsed_info.pop('skills')
            os.remove(path)
            return redirect('review')
        else:
            print("Invalid Request")
    return render(request, 'users/resume.html', parsed_info)


def ParseSkills(request, skills):
    skill_len = len(skills)
    count = 0
    connection = psycopg2.connect(user=settings.DATABASES['default']['USER'],
                                  password=settings.DATABASES['default']['PASSWORD'],
                                  host=settings.DATABASES['default']['HOST'],
                                  port=settings.DATABASES['default']['PORT'],
                                  database=settings.DATABASES['default']['NAME'])
    user = Users.objects.get(Username=request.user.username)
    try:
        cursor = connection.cursor()
        postgres_relational_query = """INSERT INTO users_users_skills (USERS_ID, SKILL_ID) VALUES (%s,%s)"""
        postgres_insert_query = """INSERT INTO users_skill (SKILL_NAME) VALUES (%s)"""
        postgres_select_query = """SELECT id FROM users_skill WHERE skill_name = (%s)"""
        for i in range(skill_len):
            cursor.execute(postgres_select_query, (skills[i],))
            in_table = cursor.fetchone()
            if (in_table is not None):
                skill_insert = (user.id, (in_table[0]))
                cursor.execute(postgres_relational_query, skill_insert)
                count = count + 1
            else:
                cursor.execute(postgres_insert_query, (skills[i],))
                connection.commit()
                cursor.execute(postgres_select_query, (skills[i],))
                in_table = cursor.fetchone()
                skill_insert = (user.id, (in_table[0]))
                cursor.execute(postgres_relational_query, skill_insert)
                count = count + 1
            connection.commit()
    except (Exception, psycopg2.Error)as error:
        if connection:
            print("Failed to insert", error)
    finally:
        if (connection):
            connection.commit()
            cursor.close()
            connection.close()
            print(count, "Record inserted")
    return


def getSkills(request):
    postgres_select_query = """SELECT skill_id FROM users_users_skills WHERE users_id = (%s)"""
    connection = psycopg2.connect(user=settings.DATABASES['default']['USER'],
                                  password=settings.DATABASES['default']['PASSWORD'],
                                  host=settings.DATABASES['default']['HOST'],
                                  port=settings.DATABASES['default']['PORT'],
                                  database=settings.DATABASES['default']['NAME'])
    user = Users.objects.get(Username=request.user.username)
    skills = []
    try:
        cursor = connection.cursor()
        cursor.execute(postgres_select_query, (user.id,))
        skill_ids = cursor.fetchall()
        skill_len = len(skill_ids)
        for i in range(skill_len):
            skills.append((Skill.objects.get(id=skill_ids[i][0])).skill_name)
    except (Exception, psycopg2.Error)as error:
        if connection:
            print("Connection failed", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
    return skills


def removeSkill(users_id, skill):
    postgres_delete_query = """DELETE FROM users_users_skills WHERE users_id = %s AND skill_id = %s"""
    postgres_select_query = """SELECT id FROM users_skill WHERE skill_name = (%s)"""
    connection = psycopg2.connect(user=settings.DATABASES['default']['USER'],
                                  password=settings.DATABASES['default']['PASSWORD'],
                                  host=settings.DATABASES['default']['HOST'],
                                  port=settings.DATABASES['default']['PORT'],
                                  database=settings.DATABASES['default']['NAME'])
    try:
        cursor = connection.cursor()
        cursor.execute(postgres_select_query, (skill,))
        in_table = cursor.fetchone()
        delete = (users_id, in_table[0],)
        print(delete)
        cursor.execute(postgres_delete_query, (users_id, in_table[0]))
        print(cursor.statusmessage)

    except (Exception, psycopg2.Error)as error:
        if connection:
            print("Connection failed", error)
    finally:
        if (connection):
            connection.commit()
            cursor.close()
            connection.close()


def review(request):
    if request.method == 'GET':
        return render(request, 'users/review.html', context={'name': request.session.get('parsed_name'),
                                                             'email': request.session.get('parsed_email'),
                                                             'mobile_number': request.session.get('parsed_number'),
                                                             'parsed_skills': request.session.get('parsed_skills')})
    if request.method == 'POST' and 'save' in request.POST:
        ParseSkills(request, request.session['parsed_skills'])
        return redirect('userProfile-home')
    elif request.method == 'POST' and 'delete' in request.POST:
        skills = request.session.get('parsed_skills')
        print(skills)
        remove_skill = request.POST.get('delete')
        skills.remove(remove_skill)
        request.session['parsed_skills'] = skills
        return redirect('review')
    return render(request, 'users/review.html', context={'name': request.session.get('parsed_name'),
                                                         'email': request.session.get('parsed_email'),
                                                         'mobile_number': request.session.get('parsed_number'),
                                                         'parsed_skills': request.session.get('parsed_skills')})


@login_required()
@allowed_users(allowed_roles=['jobseeker'])
def jobseeker_profile_view(request):
    users = Users.objects.filter(Username=request.user.username)
    print(request.user.username)
    print(request.user.email)
    if not users.exists():
        print(request.user.username)
        print('111')
        user = Users(Username=request.user.username, Email=request.user.email)
        user.save()
    users = Users.objects.filter(Username=request.user.username)
    works = workExperience.objects.filter(Username=request.user.username)
    educations = educationExperience.objects.filter(Username=request.user.username)
    skills = getSkills(request)
    if request.method == 'POST' and 'editProfile' in request.POST:
        fullname = request.POST['name']
        nickname = request.POST['nickname']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        thisuser = Users.objects.filter(Username=request.user.username).update(name=fullname, nickName=nickname,
                                                                               Email=email, phoneNumber=phone,
                                                                               address=address)
        thatuser = User.objects.get(username=request.user.username, password=request.user.password)
        thatuser.email = email
        thatuser.save()
    if request.method == 'POST' and 'deleteWork' in request.POST:
        obj = works.get(comment=request.POST['comments'], job=request.POST['job'], company=request.POST['company'],
                        Username=request.user.username).delete()
    if request.method == 'POST' and 'deleteEducation' in request.POST:
        obj = educations.get(duration=request.POST['duration'], title=request.POST['title'],
                             school=request.POST['school'], Username=request.user.username).delete()
    if request.method == 'POST' and 'deleteSkill' in request.POST:
        id = (Users.objects.get(Username=request.user.username)).id
        print(id)
        print(request.POST.get('deleteSkill'))
        removeSkill(id, request.POST.get('deleteSkill'))
        skills = getSkills(request)
        redirect('userProfile-home')
    if request.method == 'POST' and 'submitSkill' in request.POST:
        ParseSkills(request, [request.POST['newSkill']])
        skills = getSkills(request)
        redirect('userProfile-home')
    applications = Application.objects.filter(applicant=users.first()).all()
    print(applications)
    #apptest =
    #application_statuses = ApplicationStatus.objects.filter(application=applications.id)
    return render(request, 'userProfile/profile2.html',
                  {'users': users, 'works': works, 'educations': educations, 'applications': applications,
                   'skills': skills})

def uploadProfilePic_view(request):
    users = Users.objects.filter(Username=request.user.username)
    if request.method == 'GET':
        return render(request, 'users/uploadProfilePic.html')
    if request.method == 'POST' and 'upload' in request.POST:
            profilePic = request.FILES['image']
            thisuser = Users.objects.get(Username=request.user.username)
            thisuser.image = profilePic
            thisuser.save()
            return redirect('userProfile-home')
    return render(request, 'userProfile/profile2.html')
                    

def trysearch(request):
    jobs = Jobform.objects.all()
    if request.method == 'POST' and 'apply' in request.POST:
        title = request.POST['name']
        jobtype = request.POST['type']
        description = request.POST['description']
        username = request.user.username
        #application = ApplicationStatus(title=title, jobtype=jobtype, description=description, username=username)
        #application.save()
    return render(request, 'trysearch.html', {'jobs': jobs})

######FUNCTION FOR GETTING APPLICATIONSTATUSES OF USER FROM USERS OBJECT######
def getStatuses(user):
    applications = Application.objects.filter(applicant = user).all()
@login_required()
@allowed_users(allowed_roles=['jobseeker'])
def applyjob(request, job_id):
    if request.method == 'POST' and 'submit' in request.POST:
        x = (request.FILES).getlist('file')
        users = Users.objects.filter(Username=request.user.username).first()
        job = Jobform.objects.filter(id=job_id).first()
        files=[]
        if len(x)>0:
            if len(x)>1:
                for i in x:
                    files.append(i.name)
                    print(i.name)
            else:
                print(x[0].name)
                files.append(x[0].name)
                print('no list')
            app = Application(applicant=users, job=job, files=files)
            app.save()
            path = settings.MEDIA_ROOT +"\\"+ str(request.user.id) + "\\application_files\\" + str(app.id)
            fs = FileSystemStorage(location = path)
            for i in x:
                fs.save(i.name, i)
        else:
            app = Application(applicant=users, job=job, files=files)
            app.save()
        return redirect('userProfile-home')
        ##SOME ISSUES WITH FS IDK HOW TO FIX THE ISSUE OF HAVING DUPLICATE FILES IN SAME APPLICATION##
    return render(request, 'applyjob.html')


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
            findwork = workExperience.objects.filter(job=job, years=years, company=company, comment=comment,
                                                     Username=name)
            if not findwork.exists():
                works = workExperience(job=job, years=years, company=company, comment=comment, Username=name)
                works.save()
            else:
                messages.info(request, 'Already have a same record.')
                return redirect('/addwork')
            return redirect('/userprofile')
    else:
        return render(request, 'userProfile/addwork.html')


def addEducationExperience(request):
    if request.method == 'POST':
        title = request.POST['title']
        duration = request.POST['duration']
        school = request.POST['school']
        major = request.POST['major']
        if request.user.is_authenticated:
            name = request.user.username
            findEducation = educationExperience.objects.filter(title=title, duration=duration, school=school,
                                                               major=major, Username=name)
            if not findEducation.exists():
                education = educationExperience(title=title, duration=duration, school=school, major=major,
                                                Username=name)
                education.save()
            else:
                messages.info(request, 'Already have a same record.')
                return redirect('/addeducation')
            return redirect('/userprofile')
    else:
        return render(request, 'userProfile/addeducation.html')


def about(request):
    return render(request, 'userProfile/profile2.html')

#
# def redirect(request):
#     if(request.user.groups.filter(name= 'jobseeker').exists()):
#         return HttpResponseRedirect('jobsearch')
#     elif(request.user.groups.filter(name= 'company_owner').exists()):
#         return HttpResponseRedirect('company_profile')
#     return HttpResponseRedirect('home')
