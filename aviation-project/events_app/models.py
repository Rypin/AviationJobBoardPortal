from django.db import models
from datetime import datetime, timedelta, timezone

# Create your models here.
class EventListing(models.Model):
    eventID = models.IntegerField(null=False, unique=True)
    image = models.ImageField(default='default.jpg', upload_to='company_logos')
    title = models.CharField(max_length=100)
    description = models.TextField()
    posted = models.DateTimeField()
    deadline = models.DateTimeField()
    now = datetime.now(timezone.utc)
