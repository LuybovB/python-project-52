from django.db import connection
import os
import django
from django.apps import apps
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager.settings')
django.setup()

# Теперь вы можете использовать Django components, такие как модели и т.д.

print(connection.introspection.table_names())

models = apps.get_models()
print([model.__name__ for model in models])

