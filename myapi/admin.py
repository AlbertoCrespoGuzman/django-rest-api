from django.contrib import admin
from .models import Student, Membership, Course


# The 3 models are added to the admin UI
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Membership)