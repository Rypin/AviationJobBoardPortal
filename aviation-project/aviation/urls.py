
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
from django.conf import settings
from django.conf.urls.static import static
from postjob import views as postjob_views
from aviation_job_board.views import home_view, companypage_view, postjob_view, chooseRegister_view, chatRoom_view, postjob_view
from users import views as user_views
from events_app.views import events_view
from candidate_application_list import views as appList_view
urlpatterns = [
    path('', home_view, name='home'),
    path('company/',companypage_view, name='company_page'),
    path('inbox/',chatRoom_view, name='inbox'),
    path('admin/', admin.site.urls),
    path('jobpost/', postjob_views.posting, name='post_job'),
    
    # JOB SEARCH PATH
    path('search/', postjob_views.jobsearch, name='search_page'),
    
    # Candate APPLICATION PATH
    path('candidate_applications_page/', appList_view.applicationList, name='candidate_applications_page'),
    
    path('events/', events_view, name='event_list'),
    path('register/', user_views.register, name='register'),
    path('company_register', user_views.company_register, name='company_register'),
    path('company_profile_creator/', user_views.addCompanyProfile, name='company_profile_creator'),
    path('company_profile', user_views.company_profile, name='company_profile'),
    path('user_search_page', user_views.user_search_page, name='user_search_page'),
    path('choose_register/', chooseRegister_view, name='choose_register'),
    path('appStatus/', user_views.applicationStatus_view, name='application_status'),
    path('resume/', user_views.resume, name='resume'),
    path('review/', user_views.review, name='review'),
 #   path('profile/', user_views.jobseeker_profile_view, name='profile'),
    path('choose_register/', chooseRegister_view, name='choose_register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('postjob/', postjob_views.posting, name='posting'),
    path('editJob/<int:pk>', postjob_views.editJob, name='editJob'),
    path('sendEmailToJobseeker/<int:pk>', user_views.sendEmailToJobseeker, name='sendEmailToJobseeker'),
    # JOB SEARCH PATHS
    # path('postjob/', postjob_view, name='posting'),
    path('jobsearch/', postjob_views.jobsearch, name='jobsearch'),
    path('jobsearch/<int:job_id>/', postjob_views.job_detail, name='job_detail'),
    path('view-applications/', user_views.viewApplications, name ='company_applications'),
    
    path('userprofile/', user_views.jobseeker_profile_view, name = 'userProfile-home'),
    path('uploadProfilePic/', user_views.uploadProfilePic_view, name='uploadProfilePic'),
    path('about/', user_views.about, name = 'userProfile-about'),
    # path('signup/', user_views.signup, name = 'userProfile-signup'),
    path('addwork/', user_views.addWorkingExperience, name = 'userProfile-addwork'),
    path('addeducation/', user_views.addEducationExperience, name = 'userProfile-addeducation'),
    # path('signin/', user_views.signin, name = 'userProfile-signin'),
    # path('changepassword/', user_views.changepassword, name = 'userProfile-changepassword'),
    # path('upload/', user_views.upload, name = 'userProfile-upload'),
    path('trysearch/', user_views.trysearch, name='trysearch'),
    path('applyjob/<int:job_id>', user_views.applyjob, name='applyjob'),
    path('userviewcompany/<int:company_id>',postjob_views.userviewcompany, name='userviewcompany'),
]

if settings.DEBUG:
 urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
