# Generated by Django 4.2.2 on 2023-06-13 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restapp', '0028_rename_current_ctc_qa_c_ctc_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='qa',
            old_name='domain',
            new_name='Domain',
        ),
        migrations.RenameField(
            model_name='qa',
            old_name='email_id',
            new_name='Email_id',
        ),
        migrations.RenameField(
            model_name='qa',
            old_name='experience',
            new_name='Experience',
        ),
        migrations.RenameField(
            model_name='qa',
            old_name='feedback',
            new_name='Feedback',
        ),
        migrations.RenameField(
            model_name='qa',
            old_name='location',
            new_name='Location',
        ),
        migrations.RenameField(
            model_name='qa',
            old_name='name',
            new_name='Name',
        ),
        migrations.RenameField(
            model_name='qa',
            old_name='number',
            new_name='Number',
        ),
        migrations.RenameField(
            model_name='qa',
            old_name='period',
            new_name='Period',
        ),
        migrations.RenameField(
            model_name='qa',
            old_name='relevant_exp',
            new_name='Relevant_exp',
        ),
        migrations.RenameField(
            model_name='qa',
            old_name='skills',
            new_name='Skills',
        ),
    ]
