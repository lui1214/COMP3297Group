# Generated by Django 3.0 on 2019-12-06 18:18

from django.db import migrations, models
import pbi.models


class Migration(migrations.Migration):

    dependencies = [
        ('pbi', '0057_auto_20191207_0218'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='Dhash',
            field=models.CharField(default=pbi.models._hash, max_length=200),
        ),
        migrations.AddField(
            model_name='project',
            name='SMhash',
            field=models.CharField(default=pbi.models._hash, max_length=200),
        ),
    ]
