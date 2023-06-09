"""rest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the_include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from restapp.views import (
    EmployeeList,
    employee_insert,
    employee_update,
    skills_list,
    skill_autocomplete,
    emp_skills,
    emp_skills_add,
    emp_skills_update,
    emp_domains,
    emp_domains_add,
    emp_domains_update,
    todo_list,
    todo_detail,
    my_view, view_post, view_put, update_task, task_list, add_task, myprofile, create_profile, update_profile,
    delete_profile, comment_list, tasks_by_status, Commentuser_list, commentuser_add,
    commentuser_update, user_list, user_register, update_user, commentuser_delete,
    create_comment,
    forget_password_view, reset_password_view, admin_register, admin_list, delete_admin, update_admin, LoginView,
    LogoutView, myprofile_view, qa_list, qa_detail

)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('employee/', EmployeeList.as_view(), name='employee_list'),
    path('employee/insert/', employee_insert, name='employee_insert'),
    path('employee/update/<int:employee_id>/', employee_update, name='employee_update'),
    path('skills/<str:skill_name>/', skills_list, name='skills_list'),
    path('skill_autocomplete/', skill_autocomplete, name='skill_autocomplete'),

    path('admins/skills/', emp_skills, name='emp_skills'),
    path('admins/skills/add/', emp_skills_add, name='emp_skills'),
    path('admins/skills/update/<int:id>/', emp_skills_update, name='emp_skills_update'),
    path('admins/domains/', emp_domains, name='emp_domains'),
    path('admins/domains/add/', emp_domains_add, name='emp_domains_add'),
    path('admins/domains/update/<int:id>/', emp_domains_update, name='emp_domains_update'),

    path('todos/', todo_list, name='todo_list'),
    path('todos/<int:pk>/', todo_detail, name='todo_detail'),

    path('project/list/', my_view, name='my_view'),
    path('project/insert/', view_post, name='view_post'),
    path('project/update/<int:id>/', view_put, name='view_put'),

    path('myprofile/', myprofile, name='myprofile'),
    path('myprofile/<int:id>/',myprofile_view,name="myprofile_view" ),
    path('myprofile/create/', create_profile, name='create_profile'),
    path('myprofile/update/<int:pk>/', update_profile, name='update_profile'),
    path('myprofile/delete/<int:pk>/', delete_profile, name='delete_profile'),

    path('daily_task/list/', task_list, name='task_list'),
    path('daily_task/insert/', add_task, name='add_task'),
    path('daily_task/update/<int:task_id>/', update_task, name='update_task'),
    path('daily_task/status/', tasks_by_status, name='tasks_by_status'),
    path('task/comments/', comment_list, name='comment_list'),
    path('task/comments/<int:task_id>/', create_comment, name='create_comment'),

    path('comment/list/', Commentuser_list, name='Commentuser_list'),
    path('comment/insert/', commentuser_add, name='commentuser_add'),
    path('comment/update/<int:id>/', commentuser_update, name='commentuser_update'),
    path('comment/delete/<int:id>/', commentuser_delete, name='commentuser_delete'),

    path('user/list/', user_list, name='user_list'),
    path('user/add/', user_register, name='user_register'),
    path('user/update/<int:task_id>/', update_user, name='update_user'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('superuser/', admin_list, name='admin_list'),
    path('superuser/add/', admin_register, name='admin_register'),
    path('superuser/update/<int:pk>/', update_admin, name='update_admin'),
    path('superuser/delete/<int:pk>/', delete_admin, name='delete_admin'),

    path('forgot/password/', forget_password_view, name='forget_password_reset'),
    path('forgot/password/reset/', reset_password_view, name='reset_password_view'),

    path('qa/', qa_list, name='qa-list'),
    path('qa/<int:pk>/', qa_detail, name='qa-detail'),


]
