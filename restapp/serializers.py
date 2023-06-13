from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Employee, empskill, empdomain, Todo, Project, MyProfile, Task, Comment, Comment_user, Users, Qa, \
    Enquiry


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
        fields = ['id', 'sender_id','receiver_id', 'content', 'created_at']

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
            'name',
            'number',
            'email_id',
            'skills',
            'domain',
            'experience',
            'relevant_exp',
            'location',
            'c_ctc',
            'e_ctc',
            'period',
            'feedback',
        ]

class EnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquiry
        fields = [
            'id',
            'name',
            'location',
            'source_of_enquiry',
            'contacted_date',
            'followup_date',
            'contact_number',
            'comments',
            'personal_details',
            'handled_by',
            'office_visit',
            'status',
            'feed_back',
        ]
