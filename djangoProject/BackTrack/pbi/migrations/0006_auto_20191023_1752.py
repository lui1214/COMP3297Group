# Generated by Django 2.2.6 on 2019-10-23 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pbi', '0005_auto_20191023_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='status',
            field=models.CharField(choices=[('Completed', 'Completed'), ('In Progress', 'In Progress'), ('Not yet started', 'Not yet started')], default='Not yet started', max_length=200),
        ),
    ]
