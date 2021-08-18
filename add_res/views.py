from django.http.response import HttpResponse
from django.shortcuts import redirect, render, HttpResponseRedirect
from . forms import StudentForm, SemesterForm, GradeForm
from . models import Student, Semester, Grade ,Sgpa
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Avg, Sum


def search_student(request):
    if 'q_student' in request.GET:
        q_stu = request.GET['q_student']
        student= Student.objects.filter(enroll_no=q_stu).first()
        if student is not None:
            request.session['enroll_no'] = q_stu
            return HttpResponseRedirect('/add_res/add-Semester/')
        else:
            messages.error(request, 'Student is not registerd with that enroll number. Sorry!')
            return redirect('search_student')
    
    return render(request,  'add/search_stu.html' )



def save_student_form(request):
    student_form = StudentForm(request.POST, prefix='student_form')

    if request.method == 'POST':
        if student_form.is_valid():
            new_stu = student_form.save()
            request.session['enroll_no'] = new_stu.enroll_no
            return HttpResponseRedirect('/add_res/add-Semester/')
    else:
        student_form = StudentForm(prefix="student_form")
    return render(request, 'add/stu_in.html', {'student_form' : student_form})






def save_Semester_form(request, ):
    if request.method == 'POST':
        Semester_form = SemesterForm(request.POST, prefix='Semester_form')
        if Semester_form.is_valid():
            Seme = Semester_form.save(commit=False)
            Seme.student_id = request.session['enroll_no'] 
            request.session['Semester_id'] = Seme.semester
            try:
                Seme.save()
            except IntegrityError :
                messages.error(request, 'result for this semester is already exists!')
                return redirect('save_Semester_form')

            return HttpResponseRedirect('/add_res/add-grade/')
    else:
        Semester_form = SemesterForm(prefix="Semester_form")
    return render(request, 'add/Semester.html', {'Semester_form' : Semester_form})


def save_grade_form(request):
    if request.method == 'POST':
        if 'Save_and_add_another' in request.POST  :
            grade_form = GradeForm(request.POST , prefix='grade_form')
            if grade_form.is_valid():                
                grade = grade_form.save(commit=False)
                grade.student_id = request.session['enroll_no']
                grade.Semester_id = request.session['Semester_id']
                grade.save()
                # try:
                #     grade.save()
                # except IntegrityError as e:
                #     e = 'this subject has been already added!'
                #     return render(request, 'add/grade.html', context={'messages': e})
                return render(request, 'add/grade.html', {'grade_form' : grade_form})
        grade_form = GradeForm(request.POST, prefix='grade_form')
        if grade_form.is_valid() and 'submit' in request.POST:
            grade = grade_form.save(commit=False)
            grade.student_id = request.session['enroll_no']
            grade.Semester_id = request.session['Semester_id']
            try:
                grade.save()
            except IntegrityError:
                messages.error(request, 'this subject has been already added!')
                return redirect('save_grade_form')
            q_sem = request.session['Semester_id']
            q_stu = request.session['enroll_no']
            grades = Grade.objects.filter(student_id = q_stu, Semester_id = q_sem)
            total_credit_hours = grades.aggregate(tc=Sum('credit_th')+Sum('credit_pr'))
            total_CP = grades.aggregate(Sum('credit_point'))
            tcp = total_CP.get('credit_point__sum')
            tch = total_credit_hours.get('tc')
            sgp = tcp/tch
            ohk = Sgpa()
            ohk.sgpa = sgp
            ohk.semester_id = q_sem
            ohk.student_id =  q_stu
            ohk.save()
            return HttpResponse('<h1>OHK great</h1>')
    else:
        grade_form = GradeForm(prefix="grade_form")
    return render(request, 'add/grade.html', {'grade_form' : grade_form})


















# def save_sgpa(request):
#     if request.method == 'POST':
#         if 'submit' in request.POST:
#             q_sem = request.session['Semester_id']
#             q_stu = request.session['enroll_no']
#             grades = Grade.objects.filter(student_id = q_stu, Semester_id = q_sem)
#             total_credit_hours = grades.aggregate(tc=Sum('credit_th')+Sum('credit_pr'))
#             total_CP = grades.aggregate(Sum('credit_point'))
#             tcp = total_CP.get('credit_point__sum')
#             tch = total_credit_hours.get('tc')
#             sgp = tch/tcp
#             Sgpa.sgpa = sgp
#             Sgpa.semester_id = q_sem
#             Sgpa.student_id =  q_stu
#             Sgpa.save()
    








# def save_student_form(request):
#     if request.method == 'POST':
#         student_form = StudentForm( request.POST, prefix="student_form")
#         if student_form.is_valid():
#             student = json(student_form.save())
#             student_id = student
#             request.session['std'] = student_id
#             JsonResponse(student, safe=False)
#             return HttpResponseRedirect('add_res/add-branch/')
#     else:
#         student_form = StudentForm(prefix="student_form")
#     return render(request, 'add/stu_in.html', {'student_form' : student_form})


# def save_course_form(request):
#     if request.method == 'POST':
#         course_form = CourseForm( request.POST, prefix="course_form")
#         if course_form.is_valid():
#             new_course  = course_form.save(commit=False)
#             new_course.student_id = request.session.get('std')
#             course = new_course.save()
#             course_id = course
#             request.session['course'] = course_id
#             return HttpResponseRedirect('add_res/add-grade/')
#     else:
#         course_form = CourseForm(prefix="course_form")
#     return render(request, 'add/course.html', {'course_form': course_form})



# def save_grade_form(request):
#     if request.method == 'POST':
#         grade_form = GradeForm( request.POST, prefix="grade_form")
#         if grade_form.is_valid():
#             new_grade = grade_form.save(commit=False)
#             new_grade.student_id = request.session.get('std')
#             new_grade.course_id = request.session.get('course')
#     else:
#         grade_form = GradeForm(prefix="grade_form")
#     return render(request, 'add/grade.html', {'grade_form': grade_form})











# def save_all_form_at_once(request):
#     if request.method == 'POST':  
#         student_form = StudentForm( request.POST, prefix="student_form")
#         grade_form = GradeForm( request.POST, prefix="grade_form")
#         course_form = CourseForm( request.POST, prefix="course_form")       
#         if student_form.is_valid() and grade_form.is_valid() and course_form.is_valid():
#             student = student_form.save()
#             new_course = course_form.save(commit=False)
#             new_course.student = student
#             new_course.save()
#             new_grade = grade_form.save(commit=False)
#             new_grade.student = student
#             new_grade.course = new_course
#             new_grade.save()
#     else:
#         student_form = StudentForm(prefix="student_form")
#         grade_form = GradeForm(prefix="grade_form")
#         course_form = CourseForm(prefix="course_form")
        
#     return render(request, 'add.html', {'student_form' : student_form, 
#                                         'grade_form' : grade_form,
#                                         'course_form' : course_form })    
















# def save_semester_form(request):
#     if request.method == 'POST':
#         sem = SemesterForm(request.POST)
#         if sem.is_valid():
#             d = sem.cleaned_data['student_semester']
#             o = Semester(student_semester = d)
#             o.save()
#     else:
#         sem = SemesterForm()
        
#     sem = SemesterForm()

#     return render(request, 'add.html', {'form': sem})


# def save_student_form(request):
#     if request.method == 'POST':
#         stu = StudentForm(request.POST)
#         if stu.is_valid():
#             en_no =     stu.cleaned_data['enroll_no']
#             stu_na =    stu.cleaned_data['student_name']
#             stu_bra =   stu.cleaned_data['student_branch']
#             reg =       Student(enroll_no = en_no, student_name = stu_na, 
#                           student_branch = stu_bra )
#             reg.save()
#     else:
#         stu = StudentForm()
        
#     stu = StudentForm()

#     return render(request, 'add.html', {'form': stu})




# # def save_course_form(request):
# #     if request.method == 'POST':
# #         co = CourseForm(request.POST)
# #         if  co.is_valid():
# #             co_code =   co.cleaned_data['course_code']
# #             sub_na =    co.cleaned_data['sub_name']
# # #             reg =       Course(course_code = co_code, sub_name = sub_na)
# # #             reg.save()
# # #     else:
# # #         co = CourseForm()

# # #     return render(request, 'add.html')


# # # def save_grade_form(request):
# # #     if request.method == 'POST':
# # #         gd_form = GradeForm(request.POST) 
# # #         if gd.is_valid():
# # #             gd.save()
# # #         #     rn = gd.cleaned_data['roll_no']
            
# # #         #     reg = Grade(credit_th=ct, credit_pr=cp, marks_gain_th=mgt,
# # #         #                 marks_gain_pr=mgp, marks_gain_mt=mgt)
# # #         #     reg.save()



# # #     else:
# # #         gd = GradeForm()

# # #     return render(request, 'add.html')


# # # def save_semester_form(request):
# # #     if request.method == 'POST':
# # #         sf = SemesterForm(request.POST)
# # #         if sf.is_valid():
# # #             sf.save()
# # #     else:
# # #         sf = SemesterForm()
    
# # #     return render(request, 'add.html')

# # # def save_semester_form(request):
# # #     form = SemesterForm()
# # #     return render(request, 'add.html' , {'form' : form})

# # def some_view(request):
# #     if request.method == 'POST':
# #         form1 = GeneralForm(request.POST, prefix='form1')
# #         form2 = GeneralForm(request.POST, prefix='form2')
# #         if all([form1.is_valid(), form2.is_valid()]):
# #             pass # Do stuff with the forms
# #     else:
# #         form1 = GeneralForm(prefix='form1')
# #         form2 = GeneralForm(prefix='form2')
# #     return render_to_response('some_template.html', {
# #         'student_form': student_form,
# #         'form2': form2,
#     })         
            
            
            
            # new_course = form4.save()
            # new_sem = form3.save()
            # new_stu = student_form.save(commit=False)
            # if Student.semester_id is None:
            #     Student.semester_id = new_sem.id
            #     new_stu.save()
            # new_grade = form2.save(commit=False)
            # if (Grade.Sem_Info_id , Grade.Subject_Info_id , Grade.Student_Name_id) is None:
            #     Grade.Student_Name_id = new_sem.id
            #     Grade.Subject_Info_id = new_course.id
            #     Grade.Student_Name_id = new_stu.id
            #     new_grade.save()
            
            
            # new_grades = form2.save(commit=False)
            # # if Grade.Sem_Info_id or Grade.Subject_Info_id or Grade.Student_Name_id is None:
            # #     Grade.Student_Name_id = new_sem.id
            # #     Grade.Subject_Info_id = new_course.id
            # #     Grade.Student_Name_id = new_stu.id
            # #     Grade.save()
            # if Grade.Sem_Info_id is None:
            #     Grade.Sem_Info_id = new_sem.id
            #     new_grades.save()
            # elif Grade.Subject_Info_id is None:
            #     Grade.Subject_Info_id = new_course.id
            #     new_grades.save()
            # elif Grade.Student_Name_id is None:
            #     Grade.Student_Name_id = new_stu.id
            #     new_grades.save()
            # else:
            #     new_grades.save()
      





    

# # if request.method == 'POST':
#     form1 = Form1( request.POST,prefix="form1")
#     form2 = Form2( request.POST,prefix="form2")
    
#     if not form1.is_valid():
#        #save them into context
#        context['form1']= form1
    
#     if not form2.is_valid():
#        #save them into context
#        context['form2']= form2

#     if form1.is_valid() and  form2.is_valid(): 
#        #that's mean both form is valid and saved successfully 
#        return redirect('page')
#     else:
#         return render('/page', context)


# else:
#     form1 = Form1(prefix="form1")
#     form2 = Form2(prefix="form2")
