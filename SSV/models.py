from django.db import models

# Create your models here.

class demo(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)


class Student(models.Model):
    student_id = models.AutoField(primary_key=True, default=None)
    student_name = models.TextField()
    student_semester = models.IntegerField()
    student_email = models.EmailField(default=None)
    student_password = models.CharField(max_length=30, default=None)
    student_approve = models.BooleanField(default=False)
    student_voted = models.BooleanField(default=False)
    student_college_id = models.CharField(default=None, unique=True, max_length=10)

    def __str__(self):
        return str(self.student_id)


class Limit(models.Model):
    limit_id = models.AutoField(primary_key=True)
    limit_semester = models.IntegerField()
    limit_subject = models.IntegerField()

    def __str__(self):
        return str(self.limit_id)


class Subject(models.Model):
    subject_id = models.AutoField(primary_key=True, default=None)
    subject_name = models.TextField()
    subject_semester = models.IntegerField()

    def __str__(self):
        return str(self.subject_id)


class Admin(models.Model):
    admin_username = models.CharField(max_length=30)
    admin_password = models.CharField(max_length=30)

    def __str__(self):
        return str(self.admin_username)


class Voted(models.Model):
    student_id = models.ForeignKey('SSV.Student', on_delete=models.CASCADE, default=None)
    subject_id = models.ForeignKey('SSV.Subject', on_delete=models.CASCADE, default=None)
    semester = models.IntegerField()

    def __str__(self):
        return self.student_id + "," + self.subject_id


class Result(models.Model):
    result_year = models.IntegerField()
    result_subject = models.TextField()
    result_semester = models.IntegerField()
    result_votes = models.IntegerField(default=None)

