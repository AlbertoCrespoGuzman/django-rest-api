import datetime
import json

from django.core import serializers
from django.core.exceptions import ValidationError
from django.test import SimpleTestCase, TestCase
from django.urls import resolve, reverse
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APIClient
from django.db import IntegrityError

from .models import Student, Course, Membership
from .serializers import StudentSerializer, CourseSerializer, MembershipSerializer


class TestStudent(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.student_1 = Student.objects.create(first_name='alberto', last_name='crespo', birthday=datetime.datetime(2020, 5, 17))
        

    def test_student_list(self):
        response = self.client.get(reverse('student-list'))
        serializer = StudentSerializer(Student.objects.all(), many=True)
        result_expected = JSONRenderer().render(serializer.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEquals(response.content, result_expected)

    def test_add_student_details(self):
        student = {
            'first_name': 'Juan',
            'last_name': 'Perico',
            'birthday': datetime.datetime(1990, 5,5).strftime('%Y-%m-%d')
        }
        response = self.client.post(reverse('student-list'), 
                        data=json.dumps(student),
                        content_type='application/json')
                        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        student_invalid = {
            'first_name': 'Juan invalid',
            'last_name': 'Perico invalid',
            'birthday': ''
        }
        response = self.client.post(reverse('student-list'), 
                        data=json.dumps(student_invalid),
                        content_type='application/json')
                        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_student_detail(self):
        student = Student.objects.all().first()

        if student:

            response = self.client.get(reverse('student-detail', args=[student.id]))

            serializer = StudentSerializer(Student.objects.get(id=student.id))
            result_expected = JSONRenderer().render(serializer.data)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            
            self.assertEquals(response.content, result_expected)

    def test_student_form_fields_validation(self):
        with self.assertRaises(ValidationError):
            Student.objects.create(first_name='', last_name='', birthday='')



class TestCourse(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.course_1 = Course.objects.create(name='maths')
        

    def test_course_list(self):
        response = self.client.get(reverse('course-list'))
        serializer = CourseSerializer(Course.objects.all(), many=True)
        result_expected = JSONRenderer().render(serializer.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEquals(response.content, result_expected)

    def test_add_course_details(self):
        course = {
            'name': 'Philosophy'
        }
        response = self.client.post(reverse('course-list'), 
                        data=json.dumps(course),
                        content_type='application/json')
                        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        course_invalid = {
            'name': ''
        }
        response = self.client.post(reverse('course-list'), 
                        data=json.dumps(course_invalid),
                        content_type='application/json')
                        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_course_detail(self):
        course = Course.objects.all().first()

        if course:

            response = self.client.get(reverse('course-detail', args=[course.id]))

            serializer = CourseSerializer(Course.objects.get(id=course.id))
            result_expected = JSONRenderer().render(serializer.data)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            
            self.assertEquals(response.content, result_expected)

    def test_course_form_fields_validation(self):
        course = Course(name='')
        with self.assertRaises(ValidationError):
            course.full_clean()


class TestMembership(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.student_1 = Student.objects.create(first_name='zzz', last_name='zzz', birthday=datetime.date(1986,10,10))
        self.course_1 = Course.objects.create(name='Maths')
        

    def test_membership_list(self):
        response = self.client.get(reverse('membership-list'))
        serializer = MembershipSerializer(Membership.objects.all(), many=True)
        result_expected = JSONRenderer().render(serializer.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEquals(response.content, result_expected)


    def test_membership_detail(self):
        membership = Membership.objects.all().first()

        if membership:

            response = self.client.get(reverse('membership-detail', args=[membership.id]))

            serializer = CourseSerializer(Course.objects.get(id=membership.id))
            result_expected = JSONRenderer().render(serializer.data)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            
            self.assertEquals(response.content, result_expected)

    def test_membership_form_fields_validation(self):
        membership = Membership()
        with self.assertRaises(ValidationError):
            membership.full_clean()

    def test_add_registered_students_to_a_course(self):
        membership = {
            'student': self.student_1.id,
            'course': self.course_1.id
        }
        
        response = self.client.post(reverse('membership-list'),
                                    data=json.dumps(membership),
                                    content_type='application/json')

        # Adding student_1 in course_1                            
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # checking that student_1 can not be added twice in the same course 
        response = self.client.post(reverse('membership-list'),
                                    data=json.dumps(membership),
                                    content_type='application/json')
                                    
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_remove_a_student_from_a_course(self):
        #adding membership between student_1 and course_1
        membership = {
            'student': self.student_1.id,
            'course': self.course_1.id
        }
        
        response = self.client.post(reverse('membership-list'),
                                    data=json.dumps(membership),
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #deleting it
        response = self.client.delete(reverse('membership-detail', kwargs={'pk': 1 }))
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestCourseAllOrdered(TestCase):
    def setUp(self):
        self.student_1 = Student.objects.create(first_name='zzz', last_name='zzz', birthday=datetime.date(1986,10,10))
        self.student_2 = Student.objects.create(first_name='aaa', last_name='zzz', birthday=datetime.date(1986,10,11))
        self.student_3 = Student.objects.create(first_name='aaa', last_name='aaa', birthday=datetime.date(1986,10,12))
        self.student_4 = Student.objects.create(first_name='zzz', last_name='aaa', birthday=datetime.date(1986,10,13))
        self.student_5 = Student.objects.create(first_name='bbb', last_name='bbb', birthday=datetime.date(1986,10,14))
        self.student_6 = Student.objects.create(first_name='aaa', last_name='bbb', birthday=datetime.date(1986,10,15))
        self.student_7 = Student.objects.create(first_name='bbb', last_name='bbb', birthday=datetime.date(1986,10,16))

        self.course_1 = Course.objects.create(name='Maths')

        self.membership_1_1 = Membership.objects.create(student=self.student_1, course=self.course_1)
        self.membership_2_1 = Membership.objects.create(student=self.student_2, course=self.course_1)
        self.membership_3_1 = Membership.objects.create(student=self.student_3, course=self.course_1)
        self.membership_4_1 = Membership.objects.create(student=self.student_4, course=self.course_1)
        #attention: Adding student_7 in course_1 (same first_name and last_name that student_5) in order to check that join_date orders too
        self.membership_7_1 = Membership.objects.create(student=self.student_7, course=self.course_1)
        self.membership_6_1 = Membership.objects.create(student=self.student_6, course=self.course_1)
        #finally adding student_5
        self.membership_5_1 = Membership.objects.create(student=self.student_5, course=self.course_1)
        

    def test_get_course_1_ordered_by_student_last_name_first_name_and_join_date(self):
        response = self.client.get(reverse('course-detail', kwargs={'pk': self.course_1.id}))

        # we expect retrieve the students list from the course_1 order by last_name, then first_name and then join_date:
        ''' So the expected list will be:
        student_3
        student_4
        student_6
        student_7
        student_5
        student_2
        student_1
        '''
        # checking the order is really the expected
        students_order_expected = [3, 4, 6, 7, 5, 2, 1]

        list_students_id_from_course_1 = []
        for student in json.loads(response.content)['students']:
            list_students_id_from_course_1.append(student['id'])

        self.assertEqual(list_students_id_from_course_1, students_order_expected)
        
        