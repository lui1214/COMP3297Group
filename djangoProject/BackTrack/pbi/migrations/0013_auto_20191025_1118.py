# Generated by Django 2.2.6 on 2019-10-25 03:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pbi', '0012_remove_item_last_modified'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='create_at',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='item',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
