# Generated by Django 4.1.7 on 2023-06-06 07:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restapp', '0018_userregistration_delete_customuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='myprofile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='restapp.myprofile'),
        ),
    ]
