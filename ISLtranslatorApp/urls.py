"""
URL configuration for ISLtranslator project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path

from ISLtranslatorApp.views import *

urlpatterns = [
    path('',LoginPage.as_view(),name='LoginPage'),
    # //////////////////////// ADMIN //////////////////////////////////////////////////////
    
    path('AddManageUser',AddManageUser.as_view(),name='AddManageUSer'),
    path('deleteuser_delete/<int:id>',deleteuser_delete.as_view(),name='deleteuser_delete'),
    path('ViewComplaint',ViewComplaint.as_view(),name='ViewComplaint'),
    path('SendReply/<int:id>',SendReply.as_view(),name='SendReply'),
    path('ViewFeedback',ViewFeedback.as_view(),name='ViewFeedback'),
    path('AdminDash',AdminDash.as_view(),name='AdminDash'),
    
    # ////////////////////////////// USER ////////////////////////////////////////////////
    
    path('reg',reg.as_view(),name='reg'),
    path('complaint',complaint.as_view(),name='complaint'),
    path('feedback',feedback.as_view(),name='feedback'),
    path('viewcompuser',viewcompuser.as_view(),name='viewcompuser'),
    path('userdash',userdash.as_view(),name='userdash'), 
    path('changepassword/',change_password.as_view(), name='change_password'),
    path('detections',detections.as_view(),name='detections'),
    path('forgotpassword/',forgot_password.as_view(), name='forgotpassword'),
    path('sign_animation',StartSignAnimationView.as_view(),name='sign_animation'),   
    path('isl/', isl_page.as_view(), name='isl_page'),
    path('video_feed/', video_feed.as_view(), name='video_feed'),
    ]