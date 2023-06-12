from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Employee, empskill, empdomain, Todo, Project, MyProfile, Task, Comment, Comment_user, Users, Qa


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


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'admin', 'user', 'title', 'description', 'completed', 'created_at', 'last_insert']


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
        fields = ['id', 'sender','receiver', 'content', 'created_at']

class TaskSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'status', 'comments']


class CommentuserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment_user
        fields = ['id', 'task', 'time', 'last_insert']


# user
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = ['id',  'email', 'mobile_number',
                  'password', ]

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
            'candidate_name',
            'mobile_number',
            'email_id',
            'skills',
            'domain',
            'Total_exp',
            'relevant_exp',
            'location',
            'current_ctc',
            'expected_ctc',
            'notice_period',
            'feedback',
        ]