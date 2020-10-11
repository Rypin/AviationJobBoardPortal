from django.shortcuts import render,redirect
from apply.models import *
from users.models import *
from postjob.models import *
from django.contrib.auth.models import User
from .filters import *
from django.core.mail import send_mail, EmailMessage
# Create your views here.

def applicationList(request):
    company = CompanyProfile.objects.get(id=request.user.id)
    jobs = Jobform.objects.filter(company=company.id)
    applications = Application.objects.filter(company=company).order_by('job')
    applicationStatus = {
        "Unread": len(applications.filter(status='SB')) ,
        "Rejected": len(applications.filter(status='RJ')) ,
        "Reviewed": len(applications.filter(status='PR')) ,
        "Accepted": len(applications.filter(status='AC'))
    }
    job_filter = 'on'
    status_filter = 'on'
    if request.method == 'GET':
        print('in Get')
    elif request.method == 'POST' and 'review' in request.POST:
        app_id = request.POST.get('review')
        app = Application.objects.get(id=app_id)
        app.status = 'PR'
        app.save()
        return redirect('candidate_applications_page')
    elif request.method == 'POST' and 'hire' in request.POST:
        app_id = request.POST.get('hire')
        app = Application.objects.get(id=app_id)
        app.status = 'AC'
        app.save()
        return redirect('candidate_applications_page')
    elif request.method == 'POST' and 'reject' in request.POST:
        app_id = request.POST.get('reject')
        app = Application.objects.get(id=app_id)
        app.status = 'RJ'
        send_mail(
                'You have received a notification from Aviation Job Portal',
                'Your job application for ' + str(app.job.title) + ' at ' + str(app.company.name) + ' has been updated to ' + 'Rejected'+ '. Please visit the Aviation Job Portal to find out more information about this status update, or if any of this information appears to be incorrect please contact AJP support.',
                'DoNotReply.AJP@gmail.com',
                [User.objects.get(username=app.applicant.email)],
                fail_silently=False,
            )
        app.save()
        return redirect('candidate_applications_page')
    elif request.method == 'POST' and 'filters' in request.POST:
        job_filter = request.POST.get('job_filter')
        status_filter = request.POST.get('status_filter')
        if job_filter != 'on':
            applications = applications.filter(job__id = job_filter)
            job_filter = Jobform.objects.get(id=job_filter).title
        applicationStatus = {
            "Unread": len(applications.filter(status='SB')) ,
            "Rejected": len(applications.filter(status='RJ')) ,
            "Reviewed": len(applications.filter(status='PR')) ,
            "Accepted": len(applications.filter(status='AC'))
        }
        if status_filter != 'on':
            status = ''
            if status_filter == 'Unread':
                status = 'SB'
            elif status_filter == 'Rejected':
                status = 'RJ'
            elif status_filter == 'Reviewed':
                status = 'PR'
            elif status_filter == 'Accepted':
                status = 'AC'
            applications = applications.filter(status=status)
        print(job_filter)
        print(status_filter)
    elif request.method == 'POST' and 'notes' in request.POST:
        text = request.POST.get('noteText')
        app = Application.objects.get(id=request.POST.get('notes'))
        app.notes = text
        app.save()
    if job_filter == 'on':
        job_filter = 'All Applications'
    if status_filter == 'on':
        status_filter = 'All'

    filterInfo = {
        "count": len(applications),
        "jobFilter": job_filter,
        "statusFilter": status_filter
    }
    context = {
        'jobs': jobs ,
        'applications': applications ,
        'app_count': applicationStatus ,
        'files': getFiles(applications),
        'info': filterInfo
    }
    print(job_filter)
    print(status_filter)
    return render(request, "candidateApplications.html", context)
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
