from django.shortcuts import render
from rest_framework import viewsets
from .serializers import StudentSerializer, CourseSerializer, MembershipSerializer
from .models import  Student, Course, Membership

# Each viewSet call its serializer
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
 

class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    
    
