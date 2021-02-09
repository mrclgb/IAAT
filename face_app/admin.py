from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Student)
admin.site.register(Face)
admin.site.register(Encoding)
admin.site.register(Attendance)
admin.site.register(ClassCourse)
admin.site.register(StudentEnrollClass)
admin.site.register(ClassDay)

# admin.site.enable_nav_sidebar = False