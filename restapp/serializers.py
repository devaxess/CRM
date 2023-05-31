from rest_framework import serializers
from .models import Employee, empskill, empdomain, Todo, Project, MyProfile, Task, Comment, Comment_user, CustomUser


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
        fields = ['name', 'date_of_birth', 'email_address', 'role', 'age', 'specification', 'total_earned', 'skills',
                  'job', 'attachments', 'job_success_rate', 'hours_worked', 'hourly_rate']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at']

    def get_user(self, obj):
        return obj.user.username if obj.user else None


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
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'country_code', 'mobile_number', 'country_name',
                  'password', 'date_joined']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password'],
            country_code=validated_data['country_code'],
            mobile_number=validated_data['mobile_number'],
            country_name=validated_data['country_name']
        )
        return user
