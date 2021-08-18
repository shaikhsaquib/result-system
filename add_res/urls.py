from django.urls import path

from . import views 


urlpatterns=[
    # path('', views.save_student_form, name='save_student_form' ),
    path('', views.save_student_form, name='save_student_form' ),
    path('search-student/',views.search_student, name='search_student'),
    path('add-Semester/', views.save_Semester_form, name='save_Semester_form'),
    path('add-grade/', views.save_grade_form, name='save_grade_form'),


]

