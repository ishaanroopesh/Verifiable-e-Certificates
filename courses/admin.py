# admin.py

from django.contrib import admin
from .models import Course, CourseMembers, CourseJoinRequest, Certificate

class CourseMemberInline(admin.TabularInline):
    model = CourseMembers

class CourseJoinRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'is_approved']

class CertificateAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'issue_date', 'unique_code', 'hours']

admin.site.register(CourseJoinRequest, CourseJoinRequestAdmin)
admin.site.register(Course, inlines=[CourseMemberInline])
admin.site.register(Certificate, CertificateAdmin)
