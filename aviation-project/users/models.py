from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.
# Create your models here.
# class User(AbstractUser):
#     is_user = models.BooleanField(default=False)
#     is_comanyEmployer = models.BooleanField(default=False)

class Skill(models.Model):
    skill_name = models.CharField(max_length = 25, unique = True)

    def __str__(self):
        return f'{self.skill_name} skill entry'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

	# name = models.CharField(max_length=40, blank=True)
	# phoneNumber = models.CharField(max_length=15, blank=True)
	# address = models.CharField(max_length=40, blank=True)
	# company_description = models.TextField()

    def __str__(self):
        return f'{self.user.username} Profile'


class CompanyProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='default.jpg', upload_to='profile_pics')
	banner = models.ImageField(default='boeing_logo.jpg', upload_to='company_logos')
	name = models.CharField('Company Name', max_length=40, blank=True)
	phoneNumber = models.CharField(max_length=15, blank=True)
	address = models.CharField(max_length=200, blank=True)
	company_description = models.CharField('Company\'s Description', max_length=500, blank=True)

	def __str__(self):
		return f'{self.user.username} CompanyProfile'

class Users (models.Model): 
	Email = models.CharField(max_length = 40)
	Username = models.CharField(max_length = 20)
	name = models.CharField(max_length = 40, blank = True)
	address = models.CharField(max_length=200, blank=True)
	phoneNumber = models.CharField(max_length = 15, blank = True)
	nickName = models.CharField(max_length = 20, blank = True)
	password = models.CharField(max_length = 40, blank = True)
	image = models.ImageField(upload_to = 'profile_image', default = 'default.png')
	skills = models.ManyToManyField(Skill)
	
class workExperience (models.Model):
	job = models.CharField(max_length = 40)
	years = models.CharField(max_length = 20)
	company = models.CharField(max_length = 30)
	comment = models.CharField(max_length = 150)
	Username = models.CharField(max_length = 20)
	
class educationExperience (models.Model):
	title = models.CharField(max_length = 40)
	duration = models.CharField(max_length = 20)
	school = models.CharField(max_length = 40)
	major = models.CharField(max_length = 40)
	Username = models.CharField(max_length = 20)

class applicationStatus (models.Model):
	title = models.CharField(max_length=100)
	jobtype = models.CharField(max_length=100)
	description = models.CharField(max_length=100)
	username = models.CharField(max_length = 20)
	STATUS_CHOICE = [('AC', 'Accepted'), ('RJ', 'Rejected'), ('PR', 'Pending')]
	status = models.CharField(max_length=2, choices = STATUS_CHOICE, default = 'PR')

class applicationInfo (models.Model):
	Email = models.CharField(max_length = 40)
	name = models.CharField(max_length = 40, blank = True)
	address = models.CharField(max_length=200, blank=True)
	phoneNumber = models.CharField(max_length = 15, blank = True)