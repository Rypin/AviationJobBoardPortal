from django.shortcuts import render
from .models import EventListing
from datetime import datetime, timedelta, timezone
from django.db.models.functions import Lower
# Create your views here.
def events_view(request):
    now = datetime.now(timezone.utc)
    order_by = request.GET.get('order_by')
    ordering = Lower(order_by)

    if order_by == None:
        ordering = 'posted'

    events_listings = EventListing.objects.all().filter(deadline__gte=now).order_by(ordering)


    context = {
        'now' : now,
        'order_by' : order_by,
        'ordering' : ordering,
        'events_listings' : events_listings,
    }

    return render(request, "events_app/events.html", context=context)