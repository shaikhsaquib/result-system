from django.db import models
from django.db.models.fields.related import ForeignKey, OneToOneField



SEMESTER_CHOICES = (
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("6", "6"),
    ("7", "7"),
    ("8", "8"),
)


class Student(models.Model):
    enroll_no = models.CharField(primary_key=True,max_length=20)
    name = models.CharField(max_length=20)
    branch_name = models.CharField(max_length=15)
    graduating_year = models.DateField()

    def __str__(self):
        return f'{self.enroll_no} -{self.name} - {self.branch_name} - {self.graduating_year}'

    def __iter__(self):
        return [ self.enroll_no, 
                 self.graduating_year, 
                 self.name, 
                 self.branch_name ] 



class Semester(models.Model):
    semester = models.CharField(max_length=1, choices=SEMESTER_CHOICES)
    roll_no = models.IntegerField(null=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        unique_together=['semester' ,'student']


    def __str__(self):
        return f'{self.semester}-{self.student_id}'


  
class Grade(models.Model):
    id =                models.AutoField(primary_key=True)
    student =           models.ForeignKey(Student, on_delete=models.CASCADE)
    Semester =          models.ForeignKey(Semester, on_delete=models.CASCADE)
    subject_code =      models.CharField(max_length=7 )
    subject_name =      models.CharField(max_length=20)
    credit_th =         models.IntegerField(default=0)
    credit_pr =         models.IntegerField(default=0)
    marks_gain_th =     models.IntegerField(default=0)
    marks_gain_pr =     models.IntegerField(default=0)
    marks_gain_mt =     models.IntegerField(default=0)

    #calculated on database side
    total_marks =       models.IntegerField(default=0)  
    grade_point =       models.FloatField(default=0)  
    credit_point =      models.FloatField(default=0)

    def update_and_save(self):
        total_marks = self.marks_gain_th + self.marks_gain_pr + self.marks_gain_mt
        credit_point = (((self.marks_gain_th + self.marks_gain_pr + self.marks_gain_mt) / 10) * (self.credit_th + self.credit_pr))
        grade_point = (float((self.marks_gain_th + self.marks_gain_pr + self.marks_gain_mt) / 10))
        return total_marks, credit_point, grade_point
    def save(self, *args, **kwargs):
        self.total_marks, self.credit_point, self.grade_point = self.update_and_save()
        super().save(*args, **kwargs)
    
    class Meta:
         unique_together = ['student_id','Semester_id', 'subject_code']
    
    def __str__(self):
        return f'{self.student}-{self.Semester}-{self.subject_code}-{self.subject_name}-{self.credit_th}-{self.credit_pr}-{self.marks_gain_th}-{self.marks_gain_pr}-{self.marks_gain_mt}-{self.total_marks}{self.grade_point}-{self.credit_point}'





class Sgpa(models.Model):
    sgpa = models.FloatField(default=0)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['sgpa', 'student', 'semester' ]

    def __str__(self):
        return f'{self.sgpa}'





















# # SEMESTER_CHOICES = (
# #     ("1", "1"),
# #     ("2", "2"),
# #     ("3", "3"),
# #     ("4", "4"),
# #     ("5", "5"),
# #     ("6", "6"),
# #     ("7", "7"),
# #     ("8", "8"),
# # )

# # class Semester(models.Model):
# #     student_semester = models.CharField(max_length=10 ,choices = SEMESTER_CHOICES, default = '1')
# #     stu_roll =  models.IntegerField(default=0, null=False,unique= True)
# #     student_branch =   models.CharField(max_length=10)
# #     cours = models.ForeignKey('Semester', on_delete=models.CASCADE)
# #     student = models.OneToOneField('Student', on_delete=models.CASCADE)  

# #     def __str__(self):
# #         return 'roll no =' + str(self.stu_roll) + ' sem = ' + self.student_semester
# #     class Meta:
# #         unique_together = ['stu_roll','student_semester','student_branch' ]

# # class Student(models.Model):
# #     enroll_no =        models.CharField(max_length=255,primary_key = True, null=False)
# #     student_name =     models.CharField(max_length=10)

    
# #     class Meta:
# #         unique_together =['enroll_no','student_name']
    
# #     def __str__(self):
# #         return self.student_name + "-" + self.enroll_no[10:]


# # class Semester(models.Model):
# #    Semester_code =       models.CharField(max_length=10)
# #    sub_name =          models.CharField(max_length=10)
# #    student =           models.ForeignKey(Student, on_delete=models.CASCADE)
# #    sem =               models.ForeignKey(Semester, on_delete=models.CASCADE)   



# #    def __str__(self):
# #     return self.Semester_code + '-' + self.sub_name

# #    class Meta:
# #         unique_together = ['Semester_code', 'sub_name', 'student']

  
# class Grade(models.Model):
#     id =                models.AutoField(primary_key=True)
#     student =           models.ForeignKey(Student, on_delete=models.CASCADE)
#     Semester =            models.ForeignKey(Semester, on_delete=models.CASCADE)
#     sem =               models.ForeignKey(Semester, on_delete=models.CASCADE)   
#     credit_th =         models.IntegerField(default=0)
#     credit_pr =         models.IntegerField(default=0)
#     marks_gain_th =     models.IntegerField(default=0)
#     marks_gain_pr =     models.IntegerField(default=0)
#     marks_gain_mt =     models.IntegerField(default=0)

#     #calculated on database side
#     total_marks =       models.IntegerField(default=0)  
#     grade_point =       models.FloatField(default=0)  
#     credit_point =      models.FloatField(default=0)


#     # these are the coulumn sum idk how to take care of these{actually idk anything}    
#     # TotalCP = models.FloatField(default=0)
#     # Sgpa=models.FloatField(default=0)
#     # TotalCredit = models.IntegerField(default=0)

#     def update_and_save(self):
#         total_marks = self.marks_gain_th + self.marks_gain_pr + self.marks_gain_mt
#         credit_point = (((self.marks_gain_th + self.marks_gain_pr + self.marks_gain_mt) / 10) * (self.credit_th + self.credit_pr))
#         grade_point = (float((self.marks_gain_th + self.marks_gain_pr + self.marks_gain_mt) / 10))
#         return total_marks, credit_point, grade_point
#     def save(self, *args, **kwargs):
#         self.total_marks, self.credit_point, self.grade_point = self.update_and_save()
#         super().save(*args, **kwargs)
    
#     class Meta:
#          unique_together = ['student','Semester', 'sem']
    
#     def __str__(self):
#         return str(self.student)
                              
    





 











