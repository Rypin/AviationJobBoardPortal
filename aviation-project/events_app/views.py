from django.shortcuts import render, redirect
from django.contrib import messages
from .models import EventListing
from datetime import datetime, timedelta, timezone
from django.db.models.functions import Lower
from .forms import EventForm
from users.models import CompanyProfile as cp

# Create your views here.
def events_view(request):
    now = datetime.now(timezone.utc)
    order_by = request.GET.get('order_by')
    ordering = order_by

    if order_by == None:
        ordering = 'posted'

    events_listings = EventListing.objects.all().filter(deadline__gte=now).order_by(ordering) #change to ordering maybe


    context = {
        'now' : now,
        'order_by' : order_by,
        'ordering' : ordering,
        'events_listings' : events_listings,
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
            messages.success(request, f'Event Posted')
            return redirect('company_profile')
        else:
            e_form = EventForm()

    context = {
        'e_form': e_form,
    }

    return render(request, 'events_app/post_event.html', context)