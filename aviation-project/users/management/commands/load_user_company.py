from csv import DictReader
from django.core.management import BaseCommand
from django.contrib.auth.models import User, AbstractUser
from users.models import CompanyProfile


class Command(BaseCommand):
    help = "loads users and company from the user_data.csv and company_data.csv into the user model"

    def handle(self, *args, **options):

        print('Loading user data')
        for row in DictReader(open('./user_data.csv')):
            if(User.objects.filter(id = row['ID'])):
                continue
            form = User()
            form.username = row['username']
            form.password = row['password']
            form.email = row['email']
            form.first_name = row['fname']
            form.last_name = row['lname']
            
        for row in DictReader(open('./company_data.csv')):
            if(user.objects.filter(id = row['ID'])):
                continue
            form = CompanyProfile()
            form.name = row['Name']
            form.phoneNumber = row['phone number']
            form.image = row['image']
            form.address row['address']
            form.company_description['description']
            
            raw_user = row['username']
            submit_user = User.objects.get(username=raw_user)