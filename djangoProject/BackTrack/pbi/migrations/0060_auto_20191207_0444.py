# Generated by Django 3.0 on 2019-12-06 20:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pbi', '0059_auto_20191207_0301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sprint',
            name='number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sprint',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pbi.Project'),
        ),
    ]
