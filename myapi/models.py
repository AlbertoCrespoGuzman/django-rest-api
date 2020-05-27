from django.db import models

# Student model will have 3 fields, and will be ordened by last_name and then first_name
class Student(models.Model):
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 20)
    birthday = models.DateField(blank=True)
    
    class Meta:
        ordering =['last_name', 'first_name']


# Course model will have only 1 field for this test (it is enough). 
class Course(models.Model):
    name = models.CharField(max_length = 20,null=False)


# Since we need to record the moment when the student is added to the course, 
# it is necessary use a intermediary table to join students, courses and the join date
# it is important to make unique the inscription of a student in a course
class Membership(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    join_date = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    class Meta:
        unique_together = ('student', 'course',)
