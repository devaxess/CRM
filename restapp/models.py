import hashlib
from datetime import date
from django.contrib.auth.models import User, AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone


# Employee
class Employee(models.Model):
    name = models.CharField(max_length=100)
    experience = models.FloatField()
    primary_skill = models.CharField(max_length=100)
    skills = models.JSONField(null=True)
    rating = models.FloatField()
    domains = models.CharField(max_length=100, null=True)
    last_insert = models.DateTimeField(default=timezone.now)


# empskill
class empskill(models.Model):
    skills = models.JSONField(null=True)
    last_insert = models.DateTimeField(default=timezone.now)


# empdomain
class empdomain(models.Model):
    domains = models.JSONField(null=True)
    last_insert = models.DateTimeField(default=timezone.now)


# Todo
class Todo(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='assigned_tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_insert = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


# Project
class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    url = models.URLField()
    myprofile_id = models.ForeignKey('MyProfile', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title



# user register

class Users(models.Model):
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=20)
    password = models.CharField(max_length=255)
    # Add other fields as needed

    def save(self, *args, **kwargs):
        self.password = self.hash_password(self.password)
        super(Users, self).save(*args, **kwargs)

    def hash_password(self, raw_password):
        # Hash the password using hashlib
        hash_object = hashlib.sha256(raw_password.encode())
        return hash_object.hexdigest()

    def check_password(self, raw_password):
        hashed_password = self.hash_password(raw_password)
        return self.password == hashed_password

# Myprofile
class MyProfile(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    email_address = models.EmailField()
    role = models.CharField(max_length=100, default='')
    age = models.PositiveIntegerField(null=True)
    specification = models.CharField(max_length=100, null=True)
    job = models.PositiveIntegerField(default=0)
    attachments = models.FileField(upload_to='attachments/')
    job_success_rate = models.FloatField(default=0)
    hours_worked = models.PositiveIntegerField(default=0)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    skills = models.TextField(default='{}')

    def __str__(self):
        return self.name


# daily_task ;
class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField(null=True, default=date.today)
    end_date = models.DateField(null=True, default=date.today)
    status = models.TextField(null=True)
    comments = models.ManyToManyField('Comment', related_name='tasks')

    def __str__(self):
        return self.title


class Comment(models.Model):
    sender_id = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='sent_comments', null=True)
    receiver_id= models.ForeignKey(Users, on_delete=models.CASCADE, related_name='received_comments', null=True)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment by {self.sender_id.username} at {self.created_at}"

    def __str__(self):
        return f"Comment received by {self.receiver_id.username} at {self.created_at}"


# comment sections work_banch
class Comment_user(models.Model):
    task = models.TextField()
    time = models.CharField(max_length=10, null=True)
    last_insert = models.DateTimeField(default=timezone.now)


# user register
class UserRegistration(AbstractUser):
    mobile_number = models.CharField(max_length=20)
    email         = models.EmailField(unique=True)

    groups        = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set')


#QA
class Qa(models.Model):
    candidate_name = models.CharField(max_length=255)
    mobile_number  = models.CharField(max_length=20)
    email_id       = models.EmailField()
    skills         = models.CharField(max_length=255)
    domain         = models.CharField(max_length=255)
    Total_exp      = models.IntegerField()
    relevant_exp   = models.IntegerField()
    location       = models.CharField(max_length=255)
    current_ctc    = models.DecimalField(max_digits=10, decimal_places=2)
    expected_ctc   = models.DecimalField(max_digits=10, decimal_places=2)
    notice_period  = models.IntegerField()
    feedback       = models.TextField()



class Enquiry(models.Model):
    name              = models.CharField(max_length=255)
    location          = models.CharField(max_length=255)
    source_of_enquiry = models.CharField(max_length=255)
    contacted_date    = models.DateField(null=True, blank=True)
    followup_date     = models.DateField(null=True, blank=True)
    contact_number    = models.CharField(max_length=20)
    comments          = models.TextField()
    personal_details  = models.TextField()
    handled_by        = models.CharField(max_length=255)
    office_visit      = models.BooleanField(default=False)
    status            = models.CharField(max_length=255)
    feed_back         = models.TextField()

    def __str__(self):
        return self.name

