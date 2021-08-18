from django import forms
from . models import Student, Semester, Grade

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['enroll_no','name','graduating_year','branch_name']

class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ['semester','roll_no']


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['subject_code','subject_name','credit_th','credit_pr','marks_gain_th','marks_gain_pr','marks_gain_mt']




