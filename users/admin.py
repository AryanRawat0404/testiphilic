from django.contrib import admin
from .models import Student, Teacher

# Register your models here.
admin.site.register(Student)
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'teacher_id', 'subject')
    search_fields = ('full_name', 'teacher_id')
    list_filter = ('subject',)
    ordering = ('teacher_id',)