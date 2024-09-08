from django.shortcuts import render , redirect
from courses.models import Course , Video , UserCourse
from django.shortcuts import HttpResponse
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.utils.decorators import method_decorator


@method_decorator(login_required(login_url='login') , name='dispatch')
class MyCoursesList(ListView):
    template_name = 'courses/my_courses.html'
    context_object_name = 'user_courses'
    def get_queryset(self):
        return UserCourse.objects.filter(user = self.request.user)

def coursePage(request,slug):
    course = Course.objects.get(slug = slug)
    serial_no = request.GET.get('lecture')
    #videos = course.learning_set.all().order_by("serial_no")
    video = Video.objects.filter(course=course,serial_no=serial_no).first()
    
    if video:  # Check if video is not None
        if (video.is_preview is False):
            if request.user.is_authenticated is False:
                return redirect("login")
            else:
                try:
                    user_course = UserCourse.objects.get(user=request.user, course=course)
                except UserCourse.DoesNotExist:  # Explicitly catch the DoesNotExist exception
                    return redirect("check-out", slug=course.slug)
    else:
        # Handle the case where the video does not exist. You might want to redirect or show an error message.
        pass
    context={
        "course" : course,
        "video"  :video,
        
    }
    return render(request, template_name="courses/course_page.html", context= context)