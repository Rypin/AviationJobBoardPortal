from django.shortcuts import render, redirect
from django.contrib import messages
from .models import EventListing
from datetime import datetime, timedelta, timezone
from django.db.models.functions import Lower
from .forms import EventForm, UpdateEventForm
from users.models import CompanyProfile as cp
from postjob.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.sessions import  *
from django.core.mail import send_mail, EmailMessage


# Create your views here.
def events_view(request):
    now = datetime.now(timezone.utc)
    order_by = request.GET.get('order_by')
    ordering = order_by

    # if order_by == None:
    #     ordering = 'posted'

    ob = 'title'
    if request.GET.get('order_by') is None:
        if 'order_by' in request.session:
            if request.session.get('order_by') is not None:
                ob = request.session.get('order_by')
            else:
                request.session['order_by'] = 'title'
    else:
        request.session['order_by'] = order_by
        ob = request.session.get('order_by')



    events_listings = EventListing.objects.all().filter(deadline__gte=now).order_by(ob) #change to ordering maybe

    eventsPerPage = request.GET.get('eventsPerPage')


    if eventsPerPage == '1':
        request.session['eventsPerPage'] = 1
    if eventsPerPage == '2':
        request.session['eventsPerPage'] = 2


    epp = 10

    if request.GET.get('eventsPerPage') is None:
        if 'eventsPerPage' in request.session:
            if request.session.get('eventsPerPage') is not None:
                epp = request.session.get('eventsPerPage')
            else:
                request.session['eventsPerPage'] = 10
    else:
        if eventsPerPage == '1':
            request.session['eventsPerPage'] = 1
        if eventsPerPage == '2':
            request.session['eventsPerPage'] = 2
        epp = request.session.get('eventsPerPage')

    page = request.GET.get('page', 1)
    paginator = Paginator(events_listings, epp) # num of how many events per page

    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)


    context = {
        'now' : now,
        'order_by' : order_by,
        'ordering' : ordering,
        'events_listings' : events_listings,
        'eventsPerPage' : eventsPerPage,
        'events' : events,
        'epp' : epp
    }

    return render(request, "events_app/events.html", context=context)

def addEvent(request):
    e_form = EventForm(request.POST)
    if request.method == 'POST':
        e_form = EventForm(request.POST)
        if e_form.is_valid():
            obj = EventListing()
            obj.title = e_form.cleaned_data['title']
            obj.description = e_form.cleaned_data['description']
            obj.posted = e_form.cleaned_data['posted']
            obj.deadline = e_form.cleaned_data['deadline']

            cp_id = request.user.id
            id = cp.objects.get(id=cp_id)
            obj.company = id

            obj.save()
            subscribed = id.subscribed_users.all()
            if subscribed.exists():
                for x in subscribed:
                    send_mail(
                    'You have received a notification from Aviation Job Portal',
                    'A company you have subscribed to has posted a new event: ' + str(obj.title) + ' at ' + str(id.name) + ' is now available for applications. The Event description is as follows: '+str(obj.description)+' Please visit the Aviation Job Portal for additional information.',
                    'DoNotReply.AJP@gmail.com',
                    [x.Email],
                    fail_silently=False,
                )
            messages.success(request, f'Event Posted')
            return redirect('company_profile')
        else:
            e_form = EventForm()

    context = {
        'e_form': e_form,
    }
 

    return render(request, 'events_app/post_event.html', context)

def editEvent(request, pk):
    u_event = EventListing.objects.get(id=pk)
    eu_form = UpdateEventForm(instance=u_event)
    if request.method == 'POST':
        u_event = EventListing.objects.get(id=pk)
        eu_form = UpdateEventForm(request.POST, request.FILES, instance=u_event)
        if eu_form.is_valid():
            eu_form.save()
            messages.success(request, f'Event Edited')
            return redirect('company_profile')
    else:
        u_event = EventListing.objects.get(id=pk)
        eu_form = UpdateEventForm(instance=u_event)

    context = {
        'eu_form': eu_form
    }

    return render(request, 'events_app/edit_event.html', context)