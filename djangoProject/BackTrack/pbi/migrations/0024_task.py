# Generated by Django 2.2.6 on 2019-11-06 10:36

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pbi', '0023_item_project'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('hour', models.PositiveIntegerField(default=0, editable=False)),
                ('status', models.CharField(choices=[('Completed', 'Completed'), ('In Progress', 'In Progress'), ('Not yet started', 'Not yet started')], default='Not yet started', max_length=200)),
                ('create_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pbi.Item')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pbi.Person')),
            ],
        ),
    ]
