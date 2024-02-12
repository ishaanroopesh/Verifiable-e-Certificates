from django.urls import path
from . import views
from .views import change_approval_status

app_name = 'courses'

urlpatterns = [
    path('', views.ListGroups.as_view(), name='all'),
    path('create/', views.CreateGroup.as_view(), name='create'),
    path('<slug>/', views.SingleGroup.as_view(), name='single'),
    path('join/<slug>/', views.JoinGroup.as_view(), name='join'),
    path('leave/<slug>/', views.LeaveGroup.as_view(), name='leave'),
    path('<slug:course_slug>/change_approval/<str:username>/', change_approval_status, name='change_approval_status'),
    path('certificates/<str:username>/', views.CertificatesListView.as_view(), name='my_certificates'),
    path('certificate/<slug:unique_code>/', views.CertificateDetailView.as_view(), name='certificate_detail'),
]