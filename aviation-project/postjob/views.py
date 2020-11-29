from django.shortcuts import render, redirect
from django.core import serializers
from django.http import HttpResponse, Http404
from .forms import PostingForm, UpdateJobForm
from postjob.models import Jobform, Jobtype, Category
from datetime import timedelta, date, datetime
from django.http import JsonResponse
import math
from users.models import Users
from users.models import CompanyProfile as cp
from events_app.models import *
from django.core.mail import send_mail, EmailMessage
# Create your views here.

def posting(request):
    if request.method == 'POST':
        filled_form = PostingForm(request.POST)

        if filled_form.is_valid():
            obj = Jobform()
            obj.title = filled_form.cleaned_data['title']
            obj.description = filled_form.cleaned_data['description']
            obj.postdate = filled_form.cleaned_data['postdate']
            obj.jobtype = filled_form.cleaned_data['jobtype']
            obj.deadlinedate = filled_form.cleaned_data['deadlinedate']
            obj.posttime = filled_form.cleaned_data['posttime']
            obj.deadlinetime = filled_form.cleaned_data['deadlinetime']
            obj.address = filled_form.cleaned_data['address']
            obj.geolocation = filled_form.cleaned_data['geolocation']
            obj.salary_min = filled_form.cleaned_data['salary_min']
            obj.salary_max = filled_form.cleaned_data['salary_max']


            #done_job = filled_form.save()
            companyid = request.GET.get('company') #Till this day I don't know how I was able to make this line work it, request.user.id will work just as fine
            id = cp.objects.get(id=companyid)
            obj.company = id
            obj.category = Category.objects.get(name=filled_form.cleaned_data['category'])
            #done_job.save()
            # filled_form.save(company=companyid, title=title, description=description, postdate=postdate,
            #                         jobtype=jobtype, deadlinedate=deadlinedate, posttime=posttime, deadlinetime=deadlinetime,
            #                          address=address, geolocation=geolocation, salary_min=salary_min, salary_max=salary_max)
            obj.save()
            subscribed = id.subscribed_users.all()
            if subscribed.exists():
                for x in subscribed:
                    print(x.Email)
                    send_mail(
                    'You have received a notification from Aviation Job Portal',
                    'A company you have subscribed to has posted a new job: ' + str(obj.title) + ' at ' + str(id.name) + ' is now available for applications. The Job description is as follows: '+str(obj.description)+' Please visit the Aviation Job Portal for additional information.',
                    'DoNotReply.AJP@gmail.com',
                    [x.Email],
                    fail_silently=False,
                )
            return redirect('company_profile')
    else:
        filled_form = PostingForm()
    context = {
        'postingform' : filled_form,
    }

    return render(request, 'post_job.html', context)

def editJob(request, pk):
    u_job = Jobform.objects.get(id=pk)
    u_form = UpdateJobForm(instance=u_job)
    if request.method == 'POST':
        u_form = UpdateJobForm(request.POST, request.FILES, instance=u_job)
        if u_form.is_valid():
            u_form.save()
            return redirect('company_profile')
    else:
        u_form = UpdateJobForm(instance=u_job)

    context = {
        'u_form' : u_form
    }

    return render(request, 'editJob.html', context)

def calculate_miles(search_lat, search_lon, lat, lon):
    earth_radius = 6371
    dlat = deg2rad(lat - search_lat)
    dlon = deg2rad(lon - search_lon)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(deg2rad(search_lat)) * math.cos(deg2rad(lat)) * math.sin(dlon/2) * math.sin(dlon/2)

    b = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return (earth_radius * b) * 0.621

def deg2rad(deg):
    return deg * (math.pi/180)

def jobPostCount(querySet):
    size = len(querySet)
    if size == 0:
        return "No Jobs Found"
    elif size == 1:
        return "1 Job Found"
    else:
        return "{} Jobs Found".format(size)

def jobsearch(request):
    results = Jobform.objects.all()
    jobtypes = Jobtype.objects.all()
    search = request.GET.get('title')
    category = request.GET.get('category')
    fulltime = request.GET.get('Full-Time')
    parttime = request.GET.get('Part-Time')
    internship = request.GET.get('Internship')
    contract = request.GET.get('Contract')
    temporary = request.GET.get('Temporary')
    job_id = request.GET.get('job')
    searchaddress = request.GET.get('address')
    searchgeo = request.GET.get('geolocation')
    auth_req = request.GET.get('work_auth')
    minimum = request.GET.get('min_sal')
    duration = request.GET.get('posted_dur')
    distance = request.GET.get('distance')
    today = date.today()
    form = PostingForm(request.GET)
    
    if fulltime == 'on' or parttime == 'on' or internship == 'on' or contract == 'on' or temporary == 'on':
        if fulltime is None :
            results = results.exclude(jobtype__name = 'Full Time')

        if parttime is None:
            results = results.exclude(jobtype__name = 'Part Time')

        if internship is None:
            results = results.exclude(jobtype__name = 'Internship')

        if contract is None:
            results = results.exclude(jobtype__name = 'Contract')
    
        if temporary is None:
            results = results.exclude(jobtype__name = 'Temporary')

    if auth_req == "on":
        results = results.filter(US_author_required = True)
    if category != '' and category is not None:
        results= results.filter(category=category)
    if search != '' and search is not None:
        results = results.filter(title__icontains=search)


    # if searchaddress != '' and searchaddress is not None:
    #     results = results.filter(address__icontains=searchaddress)

    if minimum != '' and minimum is not None:
        results = results.filter(salary_max__gte = minimum)
    # if duration != 'on' and duration is not None:
    #     listjobs = [r.id for r in results if date.today() - r.postdate <= timedelta(days=int(duration))]
    #     results = results.filter(id__in=listjobs)

    if distance != 'on' and distance is not None and searchgeo != '' and searchgeo is not None:
        geosearch = searchgeo.split(",")
        searchlat = float(geosearch[0])
        searchlon = float(geosearch[1])
        print(geosearch)
        listjobs = [r.id for r in results if calculate_miles(searchlat, searchlon, float(str(r.geolocation).split(",")[0]), float(str(r.geolocation).split(",")[1])) <= float(distance)]
        for r in results:
            print(calculate_miles(searchlat , searchlon , float(str(r.geolocation).split(",")[0]) , float(str(r.geolocation).split(",")[1])))
        print(listjobs)
        print(results)
        results = results.filter(id__in=listjobs)
        print(results)

    job_exists = request.GET.get('jobexists')
    job_exists = True   

    if not results.exists():
        print('no jobs')
        job_exists = False
        return render(request, 'search.html', {'PostingForm':form, 'jobtypes':jobtypes, 'jobexists': job_exists})
        #raise Http404('There are no Open jobs that match this search')
    else:
        if job_id is not None:
            job = Jobform.objects.get(id = job_id)
        else:
            job = False
    print(results)
    return render(request, 'search.html', {'results': results, 'jobtypes':jobtypes, 'PostingForm':form, "count":jobPostCount(results),'job': job, 'jobexists': job_exists})

def job_detail(request, job_id):
    try:
        job = Jobform.objects.get(id=job_id)
    except job.DoesNotExist:
        raise Http404('Job not found')
    return render(request, 'job_detail.html', {'job': job,})


def searchpage(request, *args, **kwargs):
    results = Jobform.objects.all()
    form = PostingForm()
    if request.method == 'POST' and 'company' in request.POST:
        request.session['companyUsername'] = request.POST['company']
        print(request.POST['company'])

    return render(request, "search.html", {'results': results, "count":jobPostCount(results), 'PostingForm':form})

def userviewcompany(request, company_id):
    try:
        company = cp.objects.get(id=company_id)
        events = EventListing.objects.filter(company=company_id)
        jobs = Jobform.objects.filter(company=company_id)
        users = Users.objects.filter(Username=request.user.username).first()
        subscribed_boolean = False
        subscribed = company.subscribed_users.all()
        if subscribed.exists():
            for x in subscribed:
                if x == users:
                    subscribed_boolean = True
        print(company)
        print(events)
        print(jobs)
    except company.DoesNotExist:
        raise Http404('There are no Open jobs that match this search')

    return render(request, "userViewCompany.html", {'company': company, 'events': events, 'jobs': jobs, 'subscribed_boolean':subscribed_boolean})

def filterJobtype(request):
    query = {}
    jobs = Jobform.objects.all()
    result = []
    data = {}
    print(request)
    #Getting Data from Ajax request
    url = str(request.GET.get('url')).split('&')
    currentJobs = str(request.GET.get('currentJobs', None)).split(' ')
    currentJobs.remove('')
    #JobType Variables
    jobtypes = {
        'Full Time':request.GET.get('Full-Time', None),
        'Part Time': request.GET.get('Part-Time', None),
        'Internship': request.GET.get('Internship', None),
        'Contract': request.GET.get('Contract', None),
        'Temporary': request.GET.get('Temporary', None)
    }
    jobtypequery = [] # To contain the variables that are chosen for jobtype filter
    #Distance Filter Variable
    distance = request.GET.get('distance', None)
    #Date Filter Variable
    dateRange = request.GET.get('dateRange', None)
    #Salary Filter Variables
    salary = {
        'on': request.GET.get('salary', None), #Store our boolean from our checkbox and range value from our slider
        'range': request.GET.get('salaryRange', None).replace('$','').split(' - ') #replace removes all '$' and split will remove ' - ' and return a list containing our range values
    }
    #Other Filter Variables
    usAuth = request.GET.get('USAuth', None)
    print('usAuth:'+ str(usAuth))
    if url != ['']:
        for i in url: #get the search parameters from the url
            i = i.replace('?','')
            item = i.split('=')
            query[item[0]] = item[1]
    for condition in query: #query for search(Title Location Category) parameters
        if condition == 'title' and query[condition] != '' and query[condition] is not None:
            jobs = jobs.filter(title__icontains=query[condition])
        if condition =='geolocation' and query[condition] != '' and query[condition] is not None:
            coordinates = query[condition].split('%2C')
            jobsInRange=[r.id for r in jobs if calculate_miles(float(coordinates[0]), float(coordinates[1]), float(str(r.geolocation).split(",")[0]),
                                                      float(str(r.geolocation).split(",")[1])) <= float(distance)]
            jobs = jobs.filter(id__in=jobsInRange)
        if condition == 'category' and query[condition] != '' and query[condition] is not None:
            jobs = jobs.filter(category=query[condition])
    #for loop for jobtypes
    print(dateRange)
    if isinstance(dateRange, str) and dateRange != '0':
         listjobs = [r.id for r in jobs if date.today() - r.postdate <= timedelta(days=int(dateRange))]
         jobs = jobs.filter(id__in=listjobs)
    if 'true' in jobtypes.values():
        for type in jobtypes:
            if jobtypes[type] == 'true':
                jobtypequery.append(Jobtype.objects.get(name=type))
        jobs = jobs.filter(jobtype__in = jobtypequery)
    #distance filter
    if salary['on'] == 'true':
        jobs = jobs.filter(salary_min__gte=int(salary['range'][0].replace(',','')))
        jobs = jobs.filter(salary_max__lte=int(salary['range'][1].replace(',','')))
    print(currentJobs)
    data['newPosts'] = {}
    for i in jobs:
        result.append(i.id)
        if str(i.id) not in currentJobs:
            data['newPosts'][str(i.id)] = {
                'id': i.id,
                'title': i.title,
                'company': i.company.name,
                'address': i.address,
                'age': i.age(),
                'banner': i.company.banner.url,
                'category': i.category.name,
                'jobtype': i.jobtype.name,
                'description': i.description,
                'salaryRange': '$' + str(i.salary_min) + ' - $' + str(i.salary_max)
            }
    data['results'] = result
    print(data)
    return JsonResponse(data, safe=False)
