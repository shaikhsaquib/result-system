from django.contrib import admin

from . models import Grade, Student, Semester, Sgpa

# Register your models here.

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ['semester','roll_no']

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display=['id','subject_code','subject_name','credit_th','credit_pr','marks_gain_th','marks_gain_pr','marks_gain_mt']
    exclude=['total_marks','credit_point','grade_point']


@admin.register(Student)
class StudnetAdmin(admin.ModelAdmin):
    list_display=['enroll_no','name','branch_name','graduating_year']


@admin.register(Sgpa)
class SgpaAdmin(admin.ModelAdmin):
    list_display = ['semester','sgpa', 'student']