# Generated by Django 4.2.13 on 2024-06-25 11:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task_manager', '0016_label_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='labels',
            new_name='label',
        ),
    ]