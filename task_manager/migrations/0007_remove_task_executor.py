# Generated by Django 4.2.13 on 2024-06-23 19:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task_manager', '0006_task_created_at_task_executor_task_updated_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='executor',
        ),
    ]
