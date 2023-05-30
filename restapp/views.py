import json
from datetime import datetime
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from rest_framework.decorators import api_view
from rest_framework import generics, status
from .serializers import EmployeeSerializer, SkillListSerializer, DomainSerializer, TodoSerializer, ProjectSerializer, \
    TaskSerializer, MyProfileSerializer, CommentSerializer, CommentuserSerializer, UserRegistrationSerializer
from .models import Employee, empskill, empdomain, Todo, Project, Task, MyProfile, Comment, Comment_user, CustomUser



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


#Myprofile
@api_view(['GET'])
def myprofile(request):
    profile = MyProfile.objects.first()
    serializer = MyProfileSerializer(profile)
    return JsonResponse(serializer.data)

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


#Task and Comment

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



@api_view(['GET', 'POST'])
def comment_list(request):
    if request.method == 'GET':
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def comment_detail(request, pk):
    try:
        comment = Comment.objects.get(pk=pk)
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


#comment sections
@api_view(['GET'])
def Commentuser_list(request):
    if request.method == 'GET':
        user_list = Comment_user.objects.all()
        serializer = CommentuserSerializer(user_list, many=True)
        return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def commentuser_add(request):
    if request.method == 'POST':
        serializer = CommentuserSerializer(data=request.data)
        if serializer.is_valid():
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


#User_auth
@api_view(['GET'])
def user_list(request):
    if request.method == 'GET':
        registrations = CustomUser.objects.all()
        serializer = UserRegistrationSerializer(registrations, many=True)
        return JsonResponse(serializer.data, safe=False)
    return JsonResponse({"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def user_register(request):
    if request.method == 'POST':
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        confirm_password = request.data.get("confirm_password")

        if password != confirm_password:
            return JsonResponse({"message": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"message": "Username already taken"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
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
        user = CustomUser.objects.get(id=task_id)
    except CustomUser.DoesNotExist:
        return JsonResponse({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserRegistrationSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#User_login api

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = CustomUser(request, username=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            return JsonResponse({'access_token': str(access_token)}, status=200)
        else:
            return JsonResponse({'message': 'Invalid email or password'}, status=401)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)


#Super or admin  User section
@api_view(['GET'])
def admin_list(request):
    if request.method == 'GET':
        registrations = User.objects.all()
        serializer = SuperuserSerializer(registrations, many=True)
        return JsonResponse(serializer.data, safe=False)
    return JsonResponse({"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def admin_register(request):
    if request.method == 'POST':
        username = request.data.get("username")
        email = request.data.get("email")

        if User.objects.filter(username=username).exists():
            return JsonResponse({"message": "Username already taken"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return JsonResponse({"message": "Email already taken"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = SuperuserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "User registration successful"}, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)