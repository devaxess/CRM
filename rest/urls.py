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
    my_view, view_post, view_put, myprofile, create_profile, update_profile,
    delete_profile, Commentuser_list, commentuser_add,
    commentuser_update, user_list, user_register, update_user, commentuser_delete,
    forget_password_view, reset_password_view,
    LogoutView, myprofile_view, qa_list, qa_detail, comment_detail, CommentCreateView, enquiry_list, enquiry_detail,
    status_list, todo_list, update_task, delete_todo, create_todo, user_task, verify_verification_code, comment_list,
    tasks_by_status, add_task, task_list, update_todo, filter_commentuser, superuser_register, superuser_list,
    superuser_edit,  LoginView
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

    path('project/list/', my_view, name='my_view'),
    path('project/insert/', view_post, name='view_post'),
    path('project/update/<int:id>/', view_put, name='view_put'),


#myprofile
    path('myprofile/', myprofile, name='myprofile'),
    path('myprofile/<int:id>/',myprofile_view,name="myprofile_view" ),
    path('myprofile/create/', create_profile, name='create_profile'),
    path('myprofile/update/<int:pk>/', update_profile, name='update_profile'),
    path('myprofile/delete/<int:pk>/', delete_profile, name='delete_profile'),


#daily_task and comments
    path('daily_task/list/', task_list, name='task_list'),
    path('daily_task/insert/', add_task, name='add_task'),
    path('daily_task/update/<int:task_id>/', update_task, name='update_task'),
    path('daily_task/status/', tasks_by_status, name='tasks_by_status'),



#todo
    path('todo/list/', todo_list, name='todo_list'),
    path('todo/list/<int:pk>/', user_task, name='user_task'),
    path('todo/insert/', create_todo, name='create_todo'),
    path('todo/update/<int:task_id>/', update_todo, name='update_task'),
    path('todo/delete/<int:id>/', delete_todo, name='delete_todo'),
    path('todo/filterlist/<int:pk>/', status_list, name='status_list'),

    path('todo/comments/', comment_list, name='comment_list'),
    path('todo/comments/insert/<int:task_id>/', CommentCreateView.as_view(), name='comment-create'),
    path('todo/comments/<int:id>/', comment_detail, name=' comment_detail'),


#workbanch_comment
    path('comment/list/', Commentuser_list, name='Commentuser_list'),
    path('comment/list/filter/', filter_commentuser, name='filter_commentuser'),

    path('comment/insert/', commentuser_add, name='commentuser_add'),
    path('comment/update/<int:id>/', commentuser_update, name='commentuser_update'),
    path('comment/delete/<int:id>/', commentuser_delete, name='commentuser_delete'),


#user
    path('user/list/', user_list, name='user_list'),
    path('user/list/<int:id>/', user_list, name='user_list'),
    path('user/insert/', user_register, name='user_register'),
    path('user/update/<int:task_id>/', update_user, name='update_user'),

    path('login/',LoginView.as_view(), name='login_view'),
    path('logout/', LogoutView.as_view(), name='logout'),


#super_users
    path('superuser/', superuser_list, name='superuser_list'),
    path('superuser/insert/', superuser_register, name='superuser_register'),
    path('superuser/update/<int:pk>/', superuser_edit, name='superuser_edit'),


#user forgot , verification and reset
    path('forgot/password/', forget_password_view, name='forget_password_reset'),
    path('verify_verification_code/', verify_verification_code, name='verify_verification_code'),
    path('forgot/password/reset/', reset_password_view, name='reset_password_view'),

#QA info
    path('qa/', qa_list, name='qa-list'),
    path('qa/<int:pk>/', qa_detail, name='qa-detail'),


#candidate info
    path('enquiry/', enquiry_list, name='enquiry_list'),
    path('enquiry/<int:pk>/', enquiry_detail, name='enquiry_detail'),

]
