# Generated by Django 4.2.2 on 2023-06-15 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restapp', '0041_alter_users_verification_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=255)),
                ('Location', models.CharField(max_length=255)),
            ],
        ),
    ]
