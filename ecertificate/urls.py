"""
URL configuration for ecertificate project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls), #links to the admin page
    path('', views.HomePage.as_view(), name='home'), #The default home page of the website
    path('test/', views.TestPage.as_view(), name='test'), #The webpage the user is rerouted to after logging in
    path('thanks/', views.ThanksPage.as_view(), name='thanks'), #the webpage displayed once the user logs out from the website
    path('about/', views.AboutPage.as_view(), name="about"), #about details
    path('accounts/', include('accounts.urls', namespace='accounts')), #connects the urls of the accounts app to this file
    path('accounts/', include('django.contrib.auth.urls')), #specifying that the urls must be authenticated
    path('courses/', include('courses.urls', namespace='courses')), #connects the ursl of the courses app to this file
]
