import rollbar
import os


# Загрузка токена из переменных окружения
ROLLBAR_TOKEN = os.getenv('ROLL_BAR_TOKEN')

# Проверка, что токен был загружен
if ROLLBAR_TOKEN is None:
    raise ValueError('Токен Rollbar не найден. Проверьте настройки переменных окружения.')

# Настройка Rollbar
rollbar.init({
    'access_token': ROLLBAR_TOKEN,
    'environment': 'staging'
})

try:
    # Симуляция ошибки
    raise Exception('Тестовая ошибка для Rollbar')
except Exception as e:
    # Отправка отчета об ошибке в Rollbar
    rollbar.report_exc_info()

# Отправка тестового сообщения
rollbar.report_message('Тестовое сообщение из Django', 'info')

print('Тестирование Rollbar завершено.')
