
"""aviation URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from postjob import views as postjob_views
from aviation_job_board.views import home_view, companypage_view, postjob_view, chooseRegister_view, chatRoom_view, postjob_view
from users import views as user_views
from candidate_application_list import views as appList_view
from events_app import views as events_app_views


urlpatterns = [

    ### Home Page ### 
    path('', home_view, name='home'), # [X] No Sidebar Issues

    ### Inbox Page ###
    path('inbox/',chatRoom_view, name='inbox'),

    ### Candidate Application Related Pages ###
    path('candidate_applications_page/', appList_view.applicationList, name='candidate_applications_page'), # [X] No Sidebar Issues

    ### User Profile Related Pages ###
    path('userprofile/', user_views.jobseeker_profile_view, name = 'userProfile-home'), # [X] No Sidebar Issues
    path('about/', user_views.about, name = 'userProfile-about'),
    path('addwork/', user_views.addWorkingExperience, name = 'userProfile-addwork'),
    path('addeducation/', user_views.addEducationExperience, name = 'userProfile-addeducation'),

    ### Login/Logout/Register Related Pages ###
    path('register/', user_views.register, name='register'),
    path('choose_register/', chooseRegister_view, name='choose_register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    ### Password/Pass-Reset Related Pages ###
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),

    ### Job Search Related Pages ###
    path('search/', postjob_views.jobsearch, name='search_page'), # [X] No Sidebar Issues
    path('trysearch/', user_views.trysearch, name='trysearch'),
    path('jobsearch/', postjob_views.jobsearch, name='jobsearch'), # Redundent?
    path('jobsearch/<int:job_id>/', postjob_views.job_detail, name='job_detail'),
    path('applyjob/<int:job_id>', user_views.applyjob, name='applyjob'),
    path('quickapply/<int:job_id>/', user_views.quickApply, name='quick_apply'),
    url(r'^ajax/filterJobtype/$', postjob_views.filterJobtype, name='filter_jobtype'),

    ### Job Post Related Pages ###
    path('postjob/', postjob_views.posting, name='posting'),
    path('jobpost/', postjob_views.posting, name='post_job'),
    path('editJob/<int:pk>', postjob_views.editJob, name='editJob'),

    ### Events Related Pages ###
    path('events/', events_app_views.events_view, name='event_list'), # [X] No Sidebar Issues
    path('postEvent/', events_app_views.addEvent, name='postEvent'),
    path('editEvent/<int:pk>', events_app_views.editEvent, name='editEvent'),

    ### Company Profile Related Pages ###
    path('company/',companypage_view, name='company_page'), 
    path('company_register', user_views.company_register, name='company_register'),
    path('company_profile_creator/', user_views.addCompanyProfile, name='company_profile_creator'),
    path('company_profile', user_views.company_profile, name='company_profile'), # [X] No Sidebar Issues

    ### User Search Page ###
    path('user_search_page', user_views.user_search_page, name='user_search_page'), # [X] No Sidebar Issues

    ### Favoriting Job Related Pages ###
    path('fav/<int:job_id>', user_views.favorite_add, name='favorite_add'),
    url(r'^ajax/load_favoritejobs/$', user_views.loadJobs, name='favoritejobs'),
    
    ### Admin Related Pages ###
    path('admin/', admin.site.urls),
    path('oauth/', include('social_django.urls', namespace='social')),

    ### Misc./Unsorted Pages ###
    path('appStatus/', user_views.applicationStatus_view, name='application_status'),
    path('resume/', user_views.resume, name='resume'),
    path('review/', user_views.review, name='review'),
    path('sendEmailToJobseeker/<int:pk>', user_views.sendEmailToJobseeker, name='sendEmailToJobseeker'),
    path('viewUser/<int:user_id>', user_views.view_jobseeker_profile, name='viewJobseeker'),
    path('uploadProfilePic/', user_views.uploadProfilePic_view, name='uploadProfilePic'),
    path('view-applications/', user_views.viewApplications, name ='company_applications'),
    path('userviewcompany/<int:company_id>',postjob_views.userviewcompany, name='userviewcompany'),
]

if settings.DEBUG:
 urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
