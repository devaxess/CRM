# Generated by Django 4.2.2 on 2023-06-19 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('restapp', '0046_customuser_delete_userprofile'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CustomUser',
            new_name='UserProfile',
        ),
    ]
