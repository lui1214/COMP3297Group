# Generated by Django 2.2.5 on 2019-11-08 13:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pbi', '0034_task_owner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='owner',
            new_name='person',
        ),
    ]
