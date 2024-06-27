import rollbar


# Настройка Rollbar
rollbar.init('67cdf733f64e4527a4d20a257338864b', 'staging')

try:
    # Симуляция ошибки
    raise Exception('Тестовая ошибка для Rollbar')
except Exception as e:
    # Отправка отчета об ошибке в Rollbar
    rollbar.report_exc_info()

# Отправка тестового сообщения
rollbar.report_message('Тестовое сообщение из Django', 'info')

print('Тестирование Rollbar завершено.')
