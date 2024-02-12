from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'), #login page
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), #logout page
    path('signup/', views.SignUp.as_view(), name='signup'), #sign up page
]
