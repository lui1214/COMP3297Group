# Generated by Django 2.2.5 on 2019-10-26 04:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pbi', '0020_scrummaster'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ScrumMaster',
        ),
        migrations.RemoveField(
            model_name='item',
            name='last_sorted',
        ),
    ]