# Generated by Django 4.2.13 on 2024-06-30 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_manager', '0017_rename_labels_task_label'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='label',
            field=models.ManyToManyField(related_name='label', to='task_manager.label'),
        ),
    ]
