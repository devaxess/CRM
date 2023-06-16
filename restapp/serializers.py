from datetime import datetime

import pytz
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Employee, empskill, empdomain, Todo, Project, MyProfile, Comment, Comment_user, Users, Qa, \
    Enquiry,Task



class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'skills', 'primary_skill', 'experience', 'domains', 'rating', 'last_insert']



class SkillListSerializer(serializers.ModelSerializer):
    class Meta:
        model = empskill
        fields = ['id', 'skills', 'last_insert']


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = empdomain
        fields = ['id', 'domains', 'last_insert']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'sender_id','receiver_id', 'content', 'created_at']



class TodoAdminSerializer(serializers.ModelSerializer):
    create_user_name = serializers.SerializerMethodField()
    def get_create_user_name(self, obj):
        return obj.create_user.username

    class Meta:
        model = Todo
        fields = ['id', 'create_user','create_user_name', 'assign_user', 'team', 'title', 'description', 'status', 'priority', 'attachments', 'start_date', 'end_date', 'created_at', 'last_updated']



class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'url']


class MyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyProfile
        fields = ['id', 'name', 'date_of_birth', 'email_address', 'role', 'age', 'specification', 'total_earned', 'skills',
                  'job', 'attachments', 'job_success_rate', 'hours_worked', 'hourly_rate','user_id']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'sender_id','receiver_id', 'content', 'created_at']



#daily_task
class TaskSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'status', 'comments']


class CommentuserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment_user
        fields = ['id','task', 'time', 'findDate', 'last_insert']



# user
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = ['id', 'name', 'email', 'mobile_number',
                  'password',]



class SuperuserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id','username', 'email', 'password', 'is_superuser']

    def create(self, validated_data):
        user = User.objects.create_superuser(**validated_data)
        return user



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()



class QaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qa
        fields = [
            'id',
            'Name',
            'Number',
            'Emailid',
            'Skills',
            'Domain',
            'Experience',
            'Relevantexperience',
            'Location',
            'Currentctc',
            'Expectedctc',
            'Period',
            'Feedback',
        ]



class EnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquiry
        fields = [
            'id',
            'Name',
            'Location',
            'Sourceofenquiry',
            'Contacteddate',
            'Followupdate',
            'Number',
            'Comments',
            'Personaldetails',
            'Handledby',
            'Officevisit',
            'Status',
            'Feedback',
        ]











