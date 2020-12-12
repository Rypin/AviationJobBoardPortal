# Job Portal Aviation

Developed By:
<br>Summer 2020 & Fall 2020:<br>
+ **Eric Bazan**<br>
+ **Joel Echagarrua**<br>
+ **Dany Franco**<br>
+ **Ryan Pineyro**<br>
+ Summer 2020:
+ **Carlos Debasa**<br>
+ **Sebastian Rodriguez**<br>
+ **Malachi Williams**<br>
+ **Tinghui Zhang**<br>

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
posted the job. Also, the jobseeker is provided with a few options that include applying for the job, and/or viewing the company profile of the owner of that 
business. In addition, if a jobseeker wants to update/edit their profile they can do so; changing such fields such as their profile pic, adding work experience,
and editing their skills. In addition, jobseekers are able to submit their resumes and have our third-party API scan and retrieve the skills from their resume. Another feature available for jobseekers is that they are able to go to the events page, and browse through all the events that company owners have posted. In the events page, a jobseeker is able to sort the events by name, date posted, and day of the event, and they have pagination available to them that allows them to pick how many events per page they'd like to see. Also, the events page has an RSVP feature that allows them to click on the RSVP button and then allows them to filter for these RSVP-ed events, so they're able to see the events they'll most likely attend. Moving on, we have also implemented a favoriting jobs feature that allows jobseekers to be able to favorite a job and have it shown for them in the side-dashboard. The favorited jobs in the side-dashboard are able to be clicked on and it will take you to the job search page and display that job and its detail. In continuation, there's a feature that allows a jobseekers to subscribe to a company profile, and once subscribed the jobseeker is then able to get email notifications every time a company their subscribed to posts either a job or event. Lastly, we have implemented a quicker way to create a jobseeker profile. This is done, by having a jobseeker upon registration submit a resume where the resume parser will fill in the fields for the profile and collect the jobseeker's skills.
<br>
<br>
Furthermore,  if a user decides to take the alternative route and become a company owner he can do so, and his profile page will differ from a jobseeker and include
such information such as the company's name, address, phone number, etc. A company owner page will differ from a jobseeker, once a company owner logs in they will
be redirected to their company profile page, here they have the ability to update/edit their company page as they please. Also, company owner have different 
abilities than a jobseeker, they're able to post, view, edit, and delete jobs and events, search for jobseekers based on their skills, and review the application from the jobseekers that applied to their jobs. To begin with, company owners in their profile page are able to edit/update their company profile, and make any changes they want to either the company's info, logo, banner, and even the account's username and password. Also, in the company profile page, a company owner has the ability to post jobs and events once they fill out the job form and event form. Once a company has posted jobs and/or events, the company owner is able to edit the jobs and events, or delete them entirely. A company owner is also able to access the user search page, here they are able to look for jobseekers by filtering all the jobseekers in the site by their name and/or skills. Once a company owner finds the jobseeker(s) they're looking for they're able to message them on that site. This is done by sending an email to the jobseeker where the subject contains who the company owner is contacting them, and the body of the email contains the message, and the company owner's email to contact them back. Lastly, the other page available to company owners is the candidate's application page where the company owner can smoothly browse jobseeker's application, take notes on the application, and changes the application status of the jobseeker's application.

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
