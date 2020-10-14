# Job Portal Aviation

Developed By: <br>
+ **Eric Bazan**<br>
+ **Joel Echagarrua**<br>
+ **Dany Franco**<br>
+ **Ryan Pineyro**<br>

Product Owner: Masoud Sadjadi<br>
---
Florida International University<br>
School of Computing and Information Sciences<br>
Senior Project<br>

## Description:
Our project is a job board web application that will cater specifically to the aviation industry. This site allows for two different types of users to
perform certain actions/tasks depending on whether they are a "jobseeker" a person looking for a job, or a "company_owner" a person who own an a business
in the aviation industry. We hope our project will enhance itself as its scales in size with the more users that are on our site adding to the job searching 
and job posting experience.
<br>
<br>
When a user first access our site he is an unauthorized user that can only view the home page and see the features that are available such as searching for jobs
or searching for candidates. If the unauthorized user would like to access these features he first must decide what type of user he wants to belong to a "jobseeker"
or a "company_owner". A jobseeker is recommended for those who want to search and apply for jobs, while a company_owner is for those business owning individuals who
want to post jobs. Jobseekers have the option to register for a new user or log in with their LinkedIn credentials and transfer their name, username, password, and
profile picture from their LinkedIn page. Once a user has been registered they're able to login and have their selected profile page and interface customized to
them and the user group (jobseeker or company_owner) they belong to.
<br>
<br>
If a user decides to go the jobseeker route then they will be provided with the ability to have the site be the best job searching utility for them. Jobseekers
upon logging in are sent to the job search page where they can search for any job, and are presented with many filter and sorting options to enhance their job
searching experience. Once a jobseeker clicks on the job they'd like to view they can see the job as well as the information provided by the company owner that
posted the job. Also, the jobseeker is provided with a few options that inlcude applying for the job, and/or viewing the company profile of the owner of that 
business. In addition, if a jobseeker wants to update/edit their profile they can do so; changing such fields such as their profile pic, adding work experience,
and editing their skills. Lastly, jobseekers are able to submit their resumes and have our third-party API scan and retrieve the skills from their resume.
<br>
<br>
Furthermore,  if a user decides to take the alternative route and become a company owner he can do so, and his profile page will differ from a jobseeker and include
such information such as the company's name, address, phone number, etc. A company owner page will differ from a jobseeker, once a company owner logs in they will
be redirected to their company profile page, here they have the ability to update/edit their company page as they please. Also, company owner have different 
abilities than a jobseeker, they're able to post jobs, and review the application from the jobseekers that applied to their jobs.

## Prerequisites:
You will need to have python installed, and have a working web browser (your preference). Next you will want to install the latest version of Django.
PostgreSQL needs to also be installed with pgAdmin in order to handle the database.

## Installation:
```bash
pip install wheel libsass django-sass-processor django-google-maps django-crispy-forms social-auth-app-django psycopg2-binary pyresparser Pillow nltk django-filter
```

## Usage:
```bash
python manage.py runserver
```

## License
This was a Florida International University Senior Project for Computer Science

## Project Status
May continue working on this project...

## TEST
Eric's Branch
