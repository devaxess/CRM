import json
from django.contrib.auth.models import User
from django.core.mail import send_mail
from datetime import datetime, timedelta, date
from django.utils import timezone
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth import authenticate, login

from django.utils.crypto import get_random_string
from django.views.decorators.http import require_GET
from rest_framework.decorators import api_view, APIView
from rest_framework import generics, status
from .serializers import EmployeeSerializer, SkillListSerializer, DomainSerializer,  ProjectSerializer, \
     MyProfileSerializer, CommentSerializer,EnquirySerializer, CommentuserSerializer, UserRegistrationSerializer ,\
     QaSerializer , SuperuserSerializer,TodoAdminSerializer, TaskSerializer, LoginSerializer,TodoCommentSerializer
from .models import Employee, empskill, empdomain, Todo, Project,  MyProfile, Comment, Comment_user, Qa,Enquiry,Task,\
    UserProfile, TodoComment




class EmployeeList(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)


class SkillList(generics.ListCreateAPIView):
    queryset = empskill.objects.all()
    serializer_class = SkillListSerializer


@api_view(['GET'])
def employee_list(request):
    employees = Employee.objects.all()
    serializer = EmployeeSerializer(employees, many=True)
    return JsonResponse(serializer.data, safe=False)



@api_view(['POST'])
def employee_insert(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        serializer = EmployeeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)

@api_view(['PUT'])
def employee_update(request, employee_id):
    try:
        employee = Employee.objects.get(id=employee_id)
    except Employee.DoesNotExist:
        return JsonResponse({'error': 'Employee not found'}, status=404)

    serializer = EmployeeSerializer(employee, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=200)
    return JsonResponse(serializer.errors, status=400)


@api_view(['GET'])
def skills_list(request, skill_name):
    employees = Employee.objects.filter(skills__icontains=skill_name)
    serializer = EmployeeSerializer(employees, many=True)
    return JsonResponse(serializer.data, safe=False)



@require_GET
def skill_autocomplete(request):
    try:
        if 'term' in request.GET:
            term = request.GET.get('term')
            employees = Employee.objects.filter(skills__icontains=term).values('skills', 'primary_skill', 'experience').distinct()
            results = []
            for employee in employees:
                results.append({'skills': employee['skills'], 'primary_skill': employee['primary_skill'], 'experience': [employee['experience']]})
            return JsonResponse(results, safe=False)
        else:
            return JsonResponse({'error': 'Invalid request'})
    except Exception as e:
        return JsonResponse({'error': str(e)})

@api_view(['GET'])
def emp_skills(request):
    if request.method == 'GET':
        skills = empskill.objects.all()
        serializer = SkillListSerializer(skills, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def emp_skills_add(request):
    if request.method == 'POST':
        serializer = SkillListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@api_view(['PUT'])
def emp_skills_update(request, id):
    try:
        skills = empskill.objects.get(id=id)
    except empskill.DoesNotExist:
        return JsonResponse({'error': 'Skills not found'}, status=404)

    serializer = SkillListSerializer(skills, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=200)
    return JsonResponse(serializer.errors, status=400)



@api_view(['GET'])
def emp_domains(request):
    if request.method == 'GET':
        domains = empdomain.objects.all()
        serializer = DomainSerializer(domains, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def emp_domains_add(request):
    if request.method == 'POST':
        serializer = DomainSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@api_view(['PUT'])
def emp_domains_update(request, id):
    try:
        domain = empdomain.objects.get(id=id)
    except empdomain.DoesNotExist:
        return JsonResponse({'error': 'Domain not found'}, status=404)

    serializer = DomainSerializer(domain, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=200)
    return JsonResponse(serializer.errors, status=400)


@api_view(['GET', 'POST'])
def todo_list(request):
    if request.method == 'GET':
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        serializer = TodoSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def todo_detail(request, pk):
    try:
        todo = Todo.objects.get(pk=pk)
    except Todo.DoesNotExist:
        return JsonResponse({'error': 'Todo not found'}, status=404)

    if request.method == 'GET':
        serializer = TodoSerializer(todo)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        serializer = TodoSerializer(todo, data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        todo.delete()
        return JsonResponse({'message': 'Todo deleted successfully'}, status=204)

def my_view(request):
    if request.method == 'GET':
        links = Project.objects.all()
        serializer = ProjectSerializer(links, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def view_post(request):
    if request.method == 'POST':
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@api_view(['PUT'])
def view_put(request, id):
    try:
        project = Project.objects.get(id=id)
    except Project.DoesNotExist:
        return JsonResponse({'error': 'Project not found'}, status=404)

    serializer = ProjectSerializer(project, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=200)
    return JsonResponse(serializer.errors, status=400)


# Myprofile

@api_view(['GET'])
def myprofile(request):
    profile = MyProfile.objects.all()
    serializer = MyProfileSerializer(profile, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def myprofile_view(request, id):
    profile = MyProfile.objects.get(id=id)
    serializer = MyProfileSerializer(profile)
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def create_profile(request):
    serializer = MyProfileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)


@api_view(['PUT'])
def update_profile(request, pk):
    try:
        profile = MyProfile.objects.get(pk=pk)
    except MyProfile.DoesNotExist:
        return JsonResponse({'error': 'Profile not found'}, status=404)

    serializer = MyProfileSerializer(profile, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=200)
    return JsonResponse(serializer.errors, status=400)


@api_view(['DELETE'])
def delete_profile(request, pk):
    try:
        profile = MyProfile.objects.get(pk=pk)
    except MyProfile.DoesNotExist:
        return JsonResponse({'error': 'Profile not found'}, status=404)
    profile.delete()
    return JsonResponse(status=204)



#daily_task   and  Comment

@api_view(['GET'])
def task_list(request):
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)

        for task_data in serializer.data:
            task_id = task_data['id']
            comments = Comment.objects.filter(tasks=task_id)
            comment_serializer = CommentSerializer(comments, many=True)
            task_data['comments'] = comment_serializer.data

        return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def add_task(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        task = serializer.save()

        comments_data = request.data.get('comments', [])
        for comment_data in comments_data:
            comment_data['task'] = task.id
            comment_serializer = CommentSerializer(data=comment_data)
            if comment_serializer.is_valid():
                comment_serializer.save()
            else:
                task.delete()
                return JsonResponse(comment_serializer.errors, status=400)

        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)



@api_view(['PUT'])
def update_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Task not found'}, status=404)

    serializer = TaskSerializer(task, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({'status': 'success', 'message': 'Task updated successfully'})
    else:
        return JsonResponse({'status': 'error', 'message': serializer.errors}, status=400)


@api_view(['GET'])
def tasks_by_status(request):
    status = request.GET.get('status')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if not status:
        return JsonResponse({'error': 'Status is missing'}, status=400)

    valid_statuses = ["in progress", "completed", "review"]
    if status not in valid_statuses:
        return JsonResponse({'error': 'Invalid status'}, status=400)

    tasks = Task.objects.filter(status=status)

    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            tasks = tasks.filter(start_date__lte=end_date, end_date__gte=start_date)
        except ValueError:
            return JsonResponse({'error': 'Invalid date format'}, status=400)

    serializer = TaskSerializer(tasks, many=True)
    return JsonResponse(serializer.data, safe=False)



@api_view(['GET'])
def comment_list(request):
    if request.method == 'GET':
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return JsonResponse(serializer.data, safe=False)

class CommentCreateView(APIView):
    def post(self, request, task_id):
        # Retrieve the Task instance
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        sender_id = request.user.id
        sender_id = UserProfile.objects.get(id=sender_id)

        receiver_id = request.data.get('receiver_id')
        content = request.data.get('content')

        comment = Comment(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content,
            created_at=timezone.now()
        )

        comment.save()
        task.comments.add(comment)

        return Response({'message': 'Comment added successfully'}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def comment_detail(request, id):
    try:
        comment = Comment.objects.get(pk=id)
    except Comment.DoesNotExist:
        return JsonResponse({'error': 'Comment not found'}, status=404)

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        comment.delete()
        return JsonResponse({}, status=204)



#comment workbench
@api_view(['GET'])
def Commentuser_list(request):
    if request.method == 'GET':
        today = date.today()
        yesterday = today - timedelta(days=1)

        user_list = Comment_user.objects.filter(
            Q(findDate__contains=today.strftime("%Y-%m-%d")) |
            Q(findDate__contains=yesterday.strftime("%Y-%m-%d"))
        )
        serializer = CommentuserSerializer(user_list, many=True)
        return JsonResponse(serializer.data, safe=False)



@api_view(['GET'])
def filter_commentuser(request):
    start_date_str = request.GET.get('startDate')
    end_date_str = request.GET.get('endDate')

    start_date = datetime.strptime(start_date_str, "%d/%m/%Y").date()
    end_date = datetime.strptime(end_date_str, "%d/%m/%Y").date()

    filtered_comment_users = Comment_user.objects.filter(findDate__range=(start_date, end_date))

    # Serialize the filtered comment users if needed
    serializer = CommentuserSerializer(filtered_comment_users, many=True)
    return JsonResponse(serializer.data,  safe=False, status=200)


@api_view(['POST'])
def commentuser_add(request):
    serializer = CommentuserSerializer(data=request.data)
    if serializer.is_valid():
        hours = request.data.get('hours')
        minutes = request.data.get('minutes')
        period = request.data.get('period')
        time = f"{hours}:{minutes} {period}"

        find_date_str = request.data.get('findDate')
        find_date = datetime.strptime(find_date_str, "%a %b %d %Y %H:%M:%S GMT%z")

        serializer.validated_data['time'] = time
        serializer.validated_data['findDate'] = find_date
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)


@api_view(['PUT'])
def commentuser_update(request, id):
    try:
        user_update = Comment_user.objects.get(id=id)
    except Comment_user.DoesNotExist:
        return JsonResponse({'error': 'Comment not found'}, status=404)

    serializer = CommentuserSerializer(user_update, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=200)
    return JsonResponse(serializer.errors, status=400)


@api_view(['DELETE'])
def commentuser_delete(request, id):
    try:
        user_delete = Comment_user.objects.get(id=id)
    except Comment_user.DoesNotExist:
        return JsonResponse({'error': 'Comment not found'}, status=404)

    user_delete.delete()
    return JsonResponse({}, status=204)



#User_auth
@api_view(['GET'])
def user_list(request, id=None):
    if id is not None:
        try:
            user = UserProfile.objects.get(id=id)
        except UserProfile.DoesNotExist:
            return JsonResponse({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserRegistrationSerializer(user)
        return JsonResponse(serializer.data)

    registrations = UserProfile.objects.all()
    serializer = UserRegistrationSerializer(registrations, many=True)
    return JsonResponse(serializer.data, safe=False)



@api_view(['POST'])
def user_register(request):
    if request.method == 'POST':
        email = request.data.get("email")
        password = request.data.get("password")
        confirm_password = request.data.get("confirm_password")

        if password != confirm_password:
            return JsonResponse({"message": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

        if UserProfile.objects.filter(email=email).exists():
            return JsonResponse({"message": "Email already taken"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "User registration successful"}, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['PUT'])
def update_user(request, task_id):
    try:
        user = UserProfile.objects.get(id=task_id)
    except UserProfile.DoesNotExist:
        return JsonResponse({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        email = request.data.get("email")

        if email != user.email and UserProfile.objects.filter(email=email).exists():
            return JsonResponse({"message": "Email already taken"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserRegistrationSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



#Super or admin  User section

@api_view(['GET'])
def superuser_list(request):
    superusers = UserProfile.objects.filter(is_superuser=True)
    serializer = SuperuserSerializer(superusers, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def superuser_register(request):
    email = request.data.get('email')
    password = request.data.get('password')
    confirm_password = request.data.get('confirm_password')

    if password != confirm_password:
        return JsonResponse({"message": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

    if UserProfile.objects.filter(email=email).exists():
        return JsonResponse({"message": "Email already taken"}, status=status.HTTP_400_BAD_REQUEST)

    data = request.data.copy()
    data["is_superuser"] = True

    serializer = SuperuserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({"message": "Superuser registration successful"}, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def superuser_edit(request, user_id):
    try:
        user = UserProfile.objects.get(id=user_id)
    except UserProfile.DoesNotExist:
        return JsonResponse({'message': 'Superuser not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = SuperuserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#user login and logout
class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = UserProfile.objects.get(email=email)
        except UserProfile.DoesNotExist:
            return JsonResponse({'message': 'Email not Found'}, status=status.HTTP_401_UNAUTHORIZED)

        if user.check_password(password):
                if user.is_superuser:
                    # Superuser login
                    return JsonResponse({"message": "Superuser login successful", "id": user.id}, status=status.HTTP_200_OK)
                else:
                    # Normal user login
                    return JsonResponse({"message": "User login successful", "id": user.id}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'message': 'Wrong password'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        return JsonResponse({'message': 'Logout successful'}, status=status.HTTP_200_OK)



#forgot and reset password
@api_view(['POST'])
def forget_password_view(request):
    email = request.data.get('email')
    try:
        user = UserProfile.objects.get(email=email)
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    verification_code = get_random_string(length=6, allowed_chars='0123456789')

    user.verification_code = verification_code
    user.save()

    send_mail(
        'Password Reset Verification Code',
        f'Your verification code is: {verification_code}',
        'from@example.com',
        [email],
        fail_silently=False,
    )

    return JsonResponse({'message': 'Verification code sent'}, status=200)


@api_view(['POST'])
def verify_verification_code(request):
    email = request.data.get('email')
    verification_code = request.data.get('verification_code')

    if not email or not verification_code:
        return JsonResponse({'error': 'Invalid request data'}, status=400)

    try:
        user = UserProfile.objects.get(email=email)
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    print(f"Stored Verification Code: {user.verification_code}")
    print(f"Received Verification Code: {verification_code}")
    print(f"Type of Stored Verification Code: {type(user.verification_code)}")
    print(f"Type of Received Verification Code: {type(verification_code)}")

    if str(user.verification_code) != str(verification_code):
        return JsonResponse({'error': 'Invalid verification code'}, status=400)

    return JsonResponse({'message': 'Verification code matched'}, status=200)


@api_view(['POST'])
def reset_password_view(request):
    email = request.data.get('email')
    verification_code = request.data.get('verification_code')
    new_password = request.data.get('new_password')

    try:
        user = UserProfile.objects.get(email=email)
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    if user.verification_code != verification_code:
        return JsonResponse({'error': 'Invalid verification code'}, status=400)

    user.password = user.hash_password(new_password)
    user.save()

    return JsonResponse({'message': 'Password reset successful'}, status=200)



#QA list
@api_view(['GET', 'POST'])
def qa_list(request):
    if request.method == 'GET':
        registrations = Qa.objects.all()
        serializer = QaSerializer(registrations, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        serializer = QaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def qa_detail(request, pk):
    try:
        registration = Qa.objects.get(pk=pk)
    except Qa.DoesNotExist:
        return JsonResponse({"message": "Registration not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = QaSerializer(registration)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        serializer = QaSerializer(registration, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        registration.delete()
        return JsonResponse(status=status.HTTP_204_NO_CONTENT)



# Enquiry list
@api_view(['GET', 'POST'])
def enquiry_list(request):
    if request.method == 'GET':
        registrations = Enquiry.objects.all()
        serializer = EnquirySerializer(registrations, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        serializer = EnquirySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def enquiry_detail(request, pk):
    try:
        registration = Enquiry.objects.get(pk=pk)
    except Enquiry.DoesNotExist:
        return JsonResponse({"message": "Registration not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EnquirySerializer(registration)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        serializer = EnquirySerializer(registration, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        registration.delete()
        return JsonResponse(status=status.HTTP_204_NO_CONTENT)



#TODO task new
@api_view(['GET'])
def todo_list(request):
    registrations = Todo.objects.all()
    serializer = TodoAdminSerializer(registrations, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view([ 'POST'])
def create_todo(request):
    serializer = TodoAdminSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)


@api_view(['GET'])
def user_task(request, pk):
    todos = Todo.objects.filter(assign_user=pk)
    user_tasks = []

    for todo in todos:
        create_user_name = todo.create_user.username if todo.create_user else None
        assign_user_name = todo.assign_user.username if todo.assign_user else None

        task_data = {
            'task_id': todo.id,
            'team': todo.team,
            'title': todo.title,
            'description': todo.description,
            'status': todo.status,
            'priority': todo.priority,
            'startdate': todo.start_date,
            'enddate': todo.end_date,
            'created_at': todo.created_at,
            'last_updated': todo.last_updated
        }

        user_data = {
            'create_user_name': create_user_name,
            'create_user': todo.create_user_id,
            'assign_id': todo.assign_user_id,
            'tasks_details': [task_data]
        }

        # Check if the user already exists in the user_tasks list
        existing_user = next((user for user in user_tasks if user['create_user'] == todo.create_user_id), None)
        if existing_user:
            existing_user['tasks_details'].append(task_data)
        else:
            user_tasks.append(user_data)

    return JsonResponse(user_tasks, safe=False)

@api_view(['PUT'])
def update_todo(request, task_id):
    try:
        task = Todo.objects.get(id=task_id)
    except Todo.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Task not found'}, status=404)

    serializer = TodoAdminSerializer(task, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({'status': 'success', 'message': 'Task updated successfully'})
    else:
        return JsonResponse({'status': 'error', 'message': serializer.errors}, status=400)


@api_view(['DELETE'])
def delete_todo(request, id):
    try:
        todo = Todo.objects.get(id=id)
    except Todo.DoesNotExist:
        return JsonResponse({'error': 'Todo task not found'}, status=404)

    todo.delete()
    return JsonResponse({}, status=204)



# Todo filter
@api_view(['GET'])
def status_list(request, pk):
    status = request.GET.get('status')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if not status:
        return JsonResponse({'error': 'Status is missing'}, status=400)

    valid_statuses = ["inprogress", "completed", "review"]
    if status not in valid_statuses:
        return JsonResponse({'error': 'Invalid status'}, status=400)

    tasks = Todo.objects.filter(assign_user=pk, status=status)

    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            tasks = tasks.filter(start_date__lte=end_date, end_date__gte=start_date)
        except ValueError:
            return JsonResponse({'error': 'Invalid date format'}, status=400)

    serializer = TodoAdminSerializer(tasks, many=True)
    return JsonResponse(serializer.data, safe=False)



#Todo comments
@api_view(['GET', 'POST'])
def todo_comments(request, todo_id):
    if request.method == 'GET':
        comments = TodoComment.objects.filter(todo_id=todo_id)

        serialized_comments = []
        for comment in comments:
            sender_name = comment.sender.username if comment.sender else None
            receiver_name = comment.receiver.username if comment.receiver else None
            serialized_comment = {
                'id': comment.id,
                'todo': comment.todo_id,
                'sender': comment.sender_id,
                'sender_name': sender_name,
                'receiver': comment.receiver_id,
                'receiver_name': receiver_name,
                'content': comment.content,
                'created_at': comment.created_at
            }
            serialized_comments.append(serialized_comment)
        return JsonResponse(serialized_comments, safe=False)

    elif request.method == 'POST':
        request.data['todo'] = todo_id
        serializer = TodoCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return JsonResponse({"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)




@api_view(['GET', 'PUT', 'DELETE'])
def todo_comment_detail(request, todo_id, comment_id):
    try:
        comment = TodoComment.objects.get(todo_id=todo_id, id=comment_id)
    except TodoComment.DoesNotExist:
        return JsonResponse({"message": "Todo comment not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TodoCommentSerializer(comment)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        serializer = TodoCommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        comment.delete()
        return JsonResponse({"message": "Todo comment deleted"}, status=status.HTTP_204_NO_CONTENT)

    return JsonResponse({"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
