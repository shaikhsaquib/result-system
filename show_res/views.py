from django.contrib import messages
from django.shortcuts import redirect, render 
from django.db.models import Avg, Sum
from add_res.views import *
from add_res.models import Student, Semester, Grade

def sh(request):
    return render(request, 'show/s.html')

def show_enrolled_stu_result(request):
        if 'en_no' in request.GET:
            en_no = request.GET['en_no']
            q_stu = Student.objects.filter(enroll_no = en_no).first()
            if q_stu is not None:
                if 'sem' in request.GET:
                    sem = request.GET['sem']
                    q_sem = Semester.objects.filter(semester = sem, student_id = en_no).first()
                    if q_sem is not None : 
                        grades = Grade.objects.filter(student_id = en_no, Semester_id = sem)
                        # print(type(grades))
                        # print(type(grades.none()))
                        total_credit_hours = grades.aggregate(tc=Sum('credit_th')+Sum('credit_pr'))
                        total_CP = grades.aggregate(Sum('credit_point'))
                        tcp = total_CP.get('credit_point__sum')
                        tch = total_credit_hours.get('tc')
                        # sem = request.GET['sem']
                        if sem == '1' :
                            gpa = tcp/tch
                            ogpa = gpa
                            # print(ogpa)
                            # print(gpa)
                            context = {'grades' : grades, 'q_sem' : q_sem, 'q_stu' : q_stu , 'sgpa' : gpa, 'tch' : tch, 'tcp': tcp, 'ogpa' : ogpa}
                            return render(request, 'show/marksheet.html', context=context)
                        if sem != '1':
                            # for i in range(1, int(sem)+1): [:int(sem)]  this will limit
                            sgpas = Sgpa.objects.filter(student_id = en_no)[:int(sem)]  
                            gpa = tcp/tch
                            ogp = sgpas.aggregate(og = Sum('sgpa')/int(sem))
                            ogpa = ogp.get('og')
                            context = {'grades' : grades, 'q_sem' : q_sem, 'q_stu' : q_stu , 'sgpa' : gpa, 'tch' : tch, 'tcp': tcp, 'ogpa' : ogpa}
                            return render(request, 'show/marksheet.html', context=context)
                        try:
                            sgpa = tcp/tch

                        except ZeroDivisionError as e :
                            e = 'divided by zero'
                            context = {'grades' : grades, 'q_sem' : q_sem, 'q_stu' : q_stu , 'sgpa' : e, 'tch' : tch, 'tcp': tcp}
                            return render(request, 'show/marksheet.html', context=context)

                        if not grades:
                            messages.error(request, 'student registered with "{0}" but for sem "{1}" marks not added! change the semester! '.format(en_no, sem))
                            return redirect('show_enrolled_stu_result')
                        else:
                            context = {'grades' : grades, 'q_sem' : q_sem, 'q_stu' : q_stu , 'sgpa' : sgpa, 'tch' : tch, 'tcp': tcp}
                            return render(request, 'show/marksheet.html', context=context)
                        
            else:
                messages.error(request, 'No student registered with "{0}"'.format(en_no))
                return redirect('show_enrolled_stu_result')

        return render(request, 'show/search_res.html')

