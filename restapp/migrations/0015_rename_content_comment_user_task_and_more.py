# Generated by Django 4.1.7 on 2023-05-30 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restapp', '0014_customuser'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment_user',
            old_name='content',
            new_name='task',
        ),
        migrations.RemoveField(
            model_name='comment_user',
            name='timestamp',
        ),
        migrations.AddField(
            model_name='comment_user',
            name='time',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
