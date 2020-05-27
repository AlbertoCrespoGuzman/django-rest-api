
from rest_framework import serializers

from .models import Student, Course, Membership

# Student serializer        
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

# Membership Serializer will add the user details (first_name, last_name and birthday) to the output
class MembershipSerializer(serializers.ModelSerializer):

    student_first_name = serializers.ReadOnlyField(source='student.first_name')
    student_last_name = serializers.ReadOnlyField(source='student.last_name')
    student_birthday = serializers.ReadOnlyField(source='student.birthday')

    class Meta:
        model = Membership
        fields = '__all__'

# Course Serializer needs to order the students by last_name, first_name and then the join_date
# Because students is nested we need to use SerializerMethodField to retrieve them sorted.
# 1)Ordering by student will be enough because in the Student Model we are already ordering by last_name and then by first_name
# 2)After the QuerySet is specified, we need to retrieve the students from the MembershipSerializer
class CourseSerializer(serializers.ModelSerializer):
    students = serializers.SerializerMethodField()

    def get_students(self, instance):
        queryset = instance.membership_set.all().order_by('student', '-join_date')
        return MembershipSerializer(queryset, many=True, required=False, read_only=False).data
    class Meta: 
        model = Course
        fields = ('name', 'id', 'students')