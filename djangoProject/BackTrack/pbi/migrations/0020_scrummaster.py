# Generated by Django 2.2.6 on 2019-10-25 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pbi', '0019_auto_20191025_1605'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScrumMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
    ]