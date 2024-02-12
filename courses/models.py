from django.db import models
from django.utils.text import slugify
from django.urls import reverse
import misaka
import shortuuid
from django.contrib.auth import get_user_model

User = get_user_model()

class Course(models.Model):
    name = models.CharField(max_length=255, unique=True)
    course_instructor = models.CharField(max_length=255, blank=False, default='')
    issuing_organization = models.CharField(max_length=256, default='')
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    members = models.ManyToManyField(User, through='CourseMembers')
    course_length_hours = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name) #this line removes the whitespaces in between and repplaces it with underscore to eliminate any issues
        self.description_html = misaka.html(self.description) #this line converts the description from text to an html tag
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('courses:single', kwargs={'slug': self.slug})   

    class Meta:
        ordering = ['name']                              

    
class CourseMembers(models.Model):
    course = models.ForeignKey(Course, related_name='memberships', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_courses', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
    class Meta:
        unique_together = ('course', 'user')


class CourseJoinRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.course.name}"
    

class Certificate(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    issue_date = models.DateTimeField(auto_now_add=True)
    unique_code = models.CharField(max_length=10, unique=True)
    hours = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        # Generate a unique code when saving the instance
        if not self.unique_code:
            self.unique_code = shortuuid.ShortUUID().random(length=10) #generates a 10-Character code

        # Set hours_completed to the length_hours of the associated Course
        if self.course:
            self.hours = self.course.course_length_hours

        super().save(*args, **kwargs)

