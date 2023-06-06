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

    def __str__(self):
        return self.title


# Myprofile
class MyProfile(models.Model):
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


# daily_task
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment by {self.user.username} at {self.created_at}"


# comment sections
class Comment_user(models.Model):
    task = models.TextField()
    time = models.CharField(max_length=10, null=True)
    last_insert = models.DateTimeField(default=timezone.now)


# user register
class UserRegistration(AbstractUser):
    mobile_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set')
