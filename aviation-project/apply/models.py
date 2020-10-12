from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import signals
from datetime import *

class Application(models.Model):
    applicant = models.ForeignKey('users.Users', on_delete=models.CASCADE)
    job = models.ForeignKey('postjob.Jobform', on_delete=models.CASCADE)
    company = models.ForeignKey('users.CompanyProfile' , on_delete=models.CASCADE, null=True)
    files = ArrayField(models.CharField(max_length=25, blank=True), null=True)
    STATUS_CHOICES = (
        ('PR', 'Pending Review'),
        ('AC', 'Accepted'),
        ('RJ', 'Rejected'),
        ('SB', 'Submitted')
    )
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='SB')
    submission_date = models.DateField(default=date.today)
    notes = models.TextField(default='')
    def __str__(self):
        return f'{self.applicant.Username}\'s Application for job ID:{self.job.id}'

##SIGNAL FOR CREATING STATUS WITH EVERY APPLICATION##
#def create_status(sender, instance, created, **kwargs):
#    if created:
#        ApplicationNotes.objects.create(application = instance)
#signals.post_save.connect(create_status, sender=Application, weak=False, dispatch_uid='models.create_status')
#not used anymore but keeping here for reference
#ApplicationNotes had Application as a one to one field
#this would create and link an ApplicationNotes as an application was created