import hashlib
from datetime import date
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone



# user register
class Users(models.Model):
    name          = models.CharField(max_length=20 , null=True)
    email         = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=20)
    password      = models.CharField(max_length=255)
    verification_code = models.CharField(max_length=6, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.password = self.hash_password(self.password)
        super().save(*args, **kwargs)

    def hash_password(self, raw_password):
        hash_object = hashlib.sha256(raw_password.encode())
        return hash_object.hexdigest()

    def check_password(self, raw_password):
        hashed_password = self.hash_password(raw_password)
        return self.password == hashed_password



# Employee
class Employee(models.Model):
    name        = models.CharField(max_length=100)
    experience  = models.FloatField()
    primary_skill = models.CharField(max_length=100)
    skills      = models.JSONField(null=True)
    rating      = models.FloatField()
    domains     = models.CharField(max_length=100, null=True)
    last_insert = models.DateTimeField(default=timezone.now)



# empskill
class empskill(models.Model):
    skills      = models.JSONField(null=True)
    last_insert = models.DateTimeField(default=timezone.now)



# empdomain
class empdomain(models.Model):
    domains     = models.JSONField(null=True)
    last_insert = models.DateTimeField(default=timezone.now)



class Comment(models.Model):
    sender_id    = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='sent_comments', null=True)
    receiver_id  = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='received_comments', null=True)
    content      = models.TextField()
    created_at   = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment by {self.sender_id.username} at {self.created_at}"

    def __str__(self):
        return f"Comment received by {self.receiver_id.username} at {self.created_at}"



#daily_task
class Task(models.Model):
    title       = models.CharField(max_length=255)
    description = models.TextField()
    start_date  = models.DateField(null=True, default=date.today)
    end_date    = models.DateField(null=True, default=date.today)
    status      = models.TextField(null=True)
    comments    = models.ManyToManyField('Comment', related_name='tasks')

    def __str__(self):
        return self.title



# TODO
class Todo(models.Model):
    STATUS_CHOICES = (
        ('completed', 'Completed'),
        ('review', 'Review'),
        ('inprogress', 'In Progress'),
    )

    PRIORITY_CHOICES = (
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    )

    create_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    assign_user = models.ForeignKey(Users, related_name='assigned_tasks', on_delete=models.CASCADE, null=True)
    team = models.CharField(max_length=200, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='inprogress')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    attachments = models.FileField(upload_to='attachments/', blank=True, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title



# Project
class Project(models.Model):
    title       = models.CharField(max_length=100)
    description = models.TextField()
    url         = models.URLField()
    myprofile_id = models.ForeignKey('MyProfile', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title



# Myprofile
class MyProfile(models.Model):
    user_id       = models.ForeignKey(Users, on_delete=models.CASCADE,null=True)
    name          = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    email_address = models.EmailField()
    role          = models.CharField(max_length=100, default='')
    age           = models.PositiveIntegerField(null=True)
    specification = models.CharField(max_length=100, null=True)
    job           = models.PositiveIntegerField(default=0)
    attachments   = models.FileField(upload_to='attachments/')
    job_success_rate = models.FloatField(default=0)
    hours_worked  = models.PositiveIntegerField(default=0)
    hourly_rate   = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_earned  = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    skills        = models.TextField(default='{}')

    def __str__(self):
        return self.name



# comment sections work_bench
class Comment_user(models.Model):
    task        = models.TextField(null=True)
    time        = models.CharField(max_length=10, null=True)
    findDate    = models.TextField()
    last_insert = models.DateTimeField(default=timezone.now)



#QA
class Qa(models.Model):
    Name           = models.CharField(max_length=255)
    Number         = models.CharField(max_length=20)
    Emailid       = models.EmailField()
    Skills         = models.CharField(max_length=255)
    Domain         = models.CharField(max_length=255)
    Experience     = models.IntegerField()
    Relevantexperience    = models.IntegerField()
    Location       = models.CharField(max_length=255)
    Currentctc     = models.DecimalField(max_digits=10, decimal_places=2)
    Expectedctc          = models.DecimalField(max_digits=10, decimal_places=2)
    Period         = models.IntegerField()
    Feedback       = models.TextField()



#Enquiry
class Enquiry(models.Model):
    Name              = models.CharField(max_length=255)
    Location          = models.CharField(max_length=255)
    Sourceofenquiry = models.CharField(max_length=255)
    Contacteddate    = models.DateField(null=True, blank=True)
    Followupdate     = models.DateField(null=True, blank=True)
    Number           = models.CharField(max_length=20)
    Comments          = models.TextField()
    Personaldetails  = models.TextField()
    Handledby        = models.CharField(max_length=255)
    Officevisit      = models.BooleanField(default=False)
    Status            = models.CharField(max_length=255)
    Feedback         = models.TextField()

    def __str__(self):
        return self.name


