from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import signals

class Application(models.Model):
    applicant = models.ForeignKey('users.Users', on_delete=models.CASCADE)
    job = models.ForeignKey('postjob.Jobform', on_delete=models.CASCADE)
    files = ArrayField(models.CharField(max_length=25, blank=True), null=True)
    def __str__(self):
        return f'{self.applicant.Username}\'s Application for job ID:{self.job.id}'


class ApplicationStatus(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ('PR', 'Pending Review'),
        ('AC', 'Accepted'),
        ('RJ', 'Rejected'),
        ('SB', 'Submitted')
    )
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='SB')
    def __str__(self):
        return f'Application_Status ID-{self.ApplicationStatus.id} STATUS {self.ApplicationStatus.status}'

##SIGNAL FOR CREATING STATUS WITH EVERY APPLICATION##
def create_status(sender, instance, created, **kwargs):
    if created:
        ApplicationStatus.objects.create(application = instance)
signals.post_save.connect(create_status, sender=Application, weak=False, dispatch_uid='models.create_status')