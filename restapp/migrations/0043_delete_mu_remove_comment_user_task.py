# Generated by Django 4.2.2 on 2023-06-16 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restapp', '0042_mu'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Mu',
        ),
        migrations.RemoveField(
            model_name='comment_user',
            name='task',
        ),
    ]
