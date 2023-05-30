from django.contrib import admin
from .models import Employee, empskill, empdomain, Todo, Project, MyProfile, Comment

# Register your models here.

admin.site.register(Employee)
admin.site.register(empskill)
admin.site.register(empdomain)
admin.site.register(Todo)
admin.site.register(Project)
admin.site.register(MyProfile)
admin.site.register(Comment)
