# Generated by Django 3.0 on 2019-12-06 13:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pbi', '0052_auto_20191206_1145'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='project',
        ),
        migrations.AddField(
            model_name='project',
            name='person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pbi.Person'),
        ),
    ]
