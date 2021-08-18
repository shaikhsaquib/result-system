

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('enroll_no', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('branch_name', models.CharField(max_length=15)),
                ('graduating_year', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8')], max_length=1)),
                ('roll_no', models.IntegerField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='add_res.student')),
            ],
            options={
                'unique_together': {('semester', 'student')},
            },
        ),
        migrations.CreateModel(
            name='Sgpa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sgpa', models.FloatField(default=0)),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='add_res.semester')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='add_res.student')),
            ],
            options={
                'unique_together': {('sgpa', 'student', 'semester')},
            },
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('subject_code', models.CharField(max_length=7)),
                ('subject_name', models.CharField(max_length=20)),
                ('credit_th', models.IntegerField(default=0)),
                ('credit_pr', models.IntegerField(default=0)),
                ('marks_gain_th', models.IntegerField(default=0)),
                ('marks_gain_pr', models.IntegerField(default=0)),
                ('marks_gain_mt', models.IntegerField(default=0)),
                ('total_marks', models.IntegerField(default=0)),
                ('grade_point', models.FloatField(default=0)),
                ('credit_point', models.FloatField(default=0)),
                ('Semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='add_res.semester')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='add_res.student')),
            ],
            options={
                'unique_together': {('student_id', 'Semester_id', 'subject_code')},
            },
        ),
    ]
