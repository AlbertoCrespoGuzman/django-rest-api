from django.urls import include, path
from rest_framework import routers
from . import views

# The API will have 3 models, students, courses and membership.  
# So, I use route because it is easy, fast and robust to expose endpoints /students, /courses and /memberships if order to add, edit and delete them  
# endpoint /students , we can add, edit and delete students
# endpoint /courses, we can add, edit and delete courses
# endpoint /memberships, we can add registered users to a course and remove the student from the course
router = routers.DefaultRouter()
router.register(r'students', views.StudentViewSet)
router.register(r'courses', views.CourseViewSet)
router.register(r'memberships', views.MembershipViewSet)


urlpatterns = [ 
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]