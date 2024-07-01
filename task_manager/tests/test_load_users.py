import pytest
from task_manager.models import CustomUser

@pytest.mark.django_db
def test_load_users():
    # Предполагаем, что фикстуры загружены здесь
    assert CustomUser.objects.count() == 3, "Количество пользователей должно быть 3"
