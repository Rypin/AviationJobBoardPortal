from csv import DictReader
from datetime import date, time, datetime, timezone
from users.models import CompanyProfile

from django.core.management import BaseCommand

from postjob.models import Jobtype, Jobform
from pytz import UTC

DATE_FORMAT = '%m/%d/%Y'
TIME_FORMAT = '%H:%M %p'

JOB_TYPES = [
    'FullTime',
    'PartTime',
    'Internship',
    'Contract',
    'Temporary'
]

class Command(BaseCommand):
    help = "loads data from the job_data.csv into the Jobform model"

    def handle(self, *args, **options):
        print('Creating Job types')
        for job_type in JOB_TYPES:
            if(Jobtype.objects.filter(name = job_type)):
                continue
            jtype = Jobtype(name=job_type)
            jtype.save()
        print('Loading Job data for jobs to apply')
        for row in DictReader(open('./job_data.csv')):
            if(Jobform.objects.filter(id = row['ID'])):
                continue
            form = Jobform()
            form.title = row['Title']
            form.description = row['Description']
            form.salary_min = row['Minimum']
            form.salary_max = row['Maximum']
            form.address = row['Address']
            form.geolocation = row['Geolocation']

            raw_postdate = row['Date Posted']
            submit_post = datetime.strptime(raw_postdate, DATE_FORMAT)
            form.postdate = submit_post

            raw_deaddate = row['Date Deadline']
            submit_dead = datetime.strptime(raw_deaddate, DATE_FORMAT)
            form.deadlinedate = submit_dead

            raw_posttime = row['Time Posted']
            submit_posttime = UTC.localize(datetime.strptime(raw_posttime, TIME_FORMAT))
            form.posttime = submit_posttime

            raw_deadtime = row['Time Deadline']
            submit_deadtime = UTC.localize(datetime.strptime(raw_deadtime, TIME_FORMAT))
            form.deadlinetime = submit_deadtime

            raw_type = row['Job Type']
            submit_type = Jobtype.objects.get(name = raw_type)
            form.jobtype_id = submit_type.id

            raw_US_author_required = row['US authorization Required']
            if raw_US_author_required == 'TRUE' or raw_US_author_required == 'true':
                submit_US_author_required = 'True'
            else:
                submit_US_author_required = 'False'
            form.US_author_required = submit_US_author_required


            form.address = row['Address']

            raw_company = row['Company name']
            submit_company = CompanyProfile.objects.get(name=raw_company)
            form.company_id = submit_company.id

            form.save()