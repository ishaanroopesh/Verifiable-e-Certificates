from typing import Any
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, Http404
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import base64

from courses.models import Course, CourseMembers, CourseJoinRequest, Certificate
from . import models

class CreateGroup(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    fields = ('name', 'issuing_organization', 'course_instructor', 'description', 'course_length_hours')
    model = Course

    def test_func(self):
        return self.request.user.is_superuser #ensures that only a superuser can create a course

class SingleGroup(generic.DetailView):
    model = Course

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = context['object']
        students = CourseMembers.objects.filter(course=course) #obtains students in the particular course
        join_requests = {student.user_id: student.user.coursejoinrequest_set.filter(course=course).first() for student in students}
        context['students_with_requests'] = [(student, join_requests.get(student.user_id)) for student in students] #creates a list of students for the course for the context dictionary key with the student and approval details in a tuple as the key. 
        return context
    
class CertificateDetailView(generic.DetailView):
    model = Certificate
    template_name = 'courses/_certificate.html'
    context_object_name = 'certificate'

    def get_object(self, queryset=None):
        if 'unique_code' in self.kwargs: #validation statement to check if the unique code matches any in the database
            return get_object_or_404(Certificate, unique_code=self.kwargs['unique_code'])
        else:
            return None

    def generate_certificate_image(self, certificate):
        template_path = 'static/ecertificate/images/ecertificate_template.jpeg'  
        certificate_img = Image.open(template_path)

        # Creating a drawing object
        draw = ImageDraw.Draw(certificate_img)

        # Choosing a font and size
        font_path = 'static/ecertificate/fonts/Roboto-Regular.ttf'  
        font_size = 40
        fonttitle = ImageFont.truetype(font_path, font_size-5)
        fontname = ImageFont.truetype(font_path, font_size)
        fontsub = ImageFont.truetype(font_path, font_size-20)
        fontinstruct = ImageFont.truetype(font_path, font_size-10) 
        

        lentitle = len(certificate.course.name)
        lenname = len(certificate.student.username)
        leninstructor = len(certificate.course.course_instructor)
        lenorgan = len(certificate.course.issuing_organization)

        # Set the position to overlay the text
        text_position = (100, 100)

        # Adding details to the image
        draw.text((text_position[0]+240-(lenname*2), text_position[1] + 350), f"{' '.join(certificate.student.username.split('_'))}", fill="#50030A", font=fontname) #username

        if(lentitle < 30):
            draw.text((text_position[0]+125-(lentitle*1.5), text_position[1] + 475), f"{certificate.course.name}", fill="#50030A", font=fonttitle) #course name
        else: #for longer course names
            words = certificate.course.name.split()
            draw.text((text_position[0]+125-len(' '.join(words[:int(len(words)/2)+1]))*2, text_position[1] + 475), f"{' '.join(words[:int(len(words)/2)])}", fill="#50030A", font=fonttitle)
            draw.text((text_position[0]+125-len(' '.join(words[:int(len(words)/2)+1]))*2, text_position[1] + 510), f"{' '.join(words[int(len(words)/2):])}", fill="#50030A", font=fonttitle)

        draw.text((text_position[0]+260-(lenorgan*2), text_position[1] + 575), f"{certificate.course.issuing_organization}", fill="#50030A", font=fontinstruct) #Issuing organization

        draw.text((text_position[0]+270, text_position[1] + 625), f"{certificate.unique_code}", fill="#50030A", font=fontsub) #unique code

        draw.text((text_position[0]+500, text_position[1] + 900), f"Date {' /'.join(str(certificate.issue_date)[:10].split('-')[::-1])}", fill="#50030A", font=fontsub) #date

        draw.text((text_position[0]+500, text_position[1] + 930), f"{certificate.hours} Hours", fill="#50030A", font=fontsub) #length of course

        draw.text((text_position[0]+85-leninstructor, text_position[1] + 910), f"{certificate.course.course_instructor}", fill="#50030A", font=fontinstruct) #instructor name

        # Saving the generated image to a BytesIO buffer
        image_buffer = BytesIO()
        certificate_img.save(image_buffer, format='PNG') 
        image_buffer.seek(0)

        return image_buffer

    def render_to_response(self, context, **response_kwargs):
        certificate = context['certificate']

        # Generate the certificate image using the local function
        certificate_image = self.generate_certificate_image(certificate)

        # Pass the image URL to the template
        context['certificate_image_url'] = f"data:image/jpeg;base64,{base64.b64encode(certificate_image.getvalue()).decode()}"

        return super().render_to_response(context, **response_kwargs)


class ListGroups(generic.ListView):
    model = Course

class CertificatesListView(generic.ListView):
    template_name = 'courses/certificates_list.html'
    context_object_name = 'certificates'

    def get_queryset(self):
        # Retrieve the certificates associated with the current user
        user_certificates = Certificate.objects.filter(student=self.request.user)
        return user_certificates

class JoinGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('courses:single', kwargs={'slug':self.kwargs.get('slug')})
    
    def get(self, request, *args, **kwargs):
        course = get_object_or_404(Course, slug=self.kwargs.get('slug'))

        try:
            CourseMembers.objects.create(user=self.request.user, course=course)
            CourseJoinRequest.objects.create(user=self.request.user, course=course)
        except:
            messages.warning(self.request, "Warning already a member!")
        else:
            messages.success(self.request, "You are now a member!")

        return super().get(request, *args, **kwargs)

class LeaveGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('courses:single', kwargs={'slug':self.kwargs.get('slug')})
    
    def get(self, request, *args, **kwargs):

        try:
            membership = models.CourseMembers.objects.filter(user=self.request.user, course__slug=self.kwargs.get('slug')).get()
        except models.CourseMembers.DoesNotExist:
            messages.warning(self.request, "Sorry you are not in this group!")
        else:
            membership.delete()
            messages.success(self.request, 'You have left the group')
        return super().get(request, *args, **kwargs)



def create_certificate(student, course):
    # Creating a certificate for the student and course
    Certificate.objects.create(student=student, course=course)

def view_certificate(request, certificate_id):
    certificate = get_object_or_404(Certificate, id=certificate_id)
    return render(request, 'courses/view_certificate.html', {'certificate': certificate})

    
def change_approval_status(request, course_slug, username):
    if not request.user.is_superuser:
        return HttpResponse("Permission denied")

    try:
        course_join_request = CourseJoinRequest.objects.get(course__slug=course_slug, user__username=username)
    except CourseJoinRequest.DoesNotExist:
        raise Http404(f"CourseJoinRequest does not exist for course_slug={course_slug} and username={username}")

    if request.method == 'POST':
        # Toggle the approval status
        course_join_request.is_approved = not course_join_request.is_approved
        course_join_request.save()

        if course_join_request.is_approved:
            create_certificate(course_join_request.user, course_join_request.course)

    return redirect('courses:single', slug=course_slug)

