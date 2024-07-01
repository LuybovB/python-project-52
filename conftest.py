import os
import pytest

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager.settings')

import django
django.setup()

@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass