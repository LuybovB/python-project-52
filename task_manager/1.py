document.addEventListener('DOMContentLoaded', function() {
  // Моковые данные для тестирования
  const mockUsers = [
    { id: 1, username: 'Исполнитель1' },
    { id: 2, username: 'Исполнитель2' },
    // Добавьте столько пользователей, сколько нужно для тестирования
  ];

  function populateExecutorDropdown() {
    const executorElement = document.getElementById('executor');
    if (executorElement) {
      // Очищаем существующие опции
      executorElement.innerHTML = '';
      // Добавляем плейсхолдер
      const placeholderOption = new Option('---------', '', true, true);
      placeholderOption.disabled = true;
      executorElement.appendChild(placeholderOption);
      // Добавляем моковые данные в выпадающий список
      mockUsers.forEach(user => {
        const option = new Option(user.username, user.id);
        executorElement.appendChild(option);
      });
      console.log('Исполнитель содержит опции');
    } else {
      console.log('Элемент исполнителя не загружен');
    }
  }

  setTimeout(() => {
    populateExecutorDropdown();
  }, 2000); // ждем 2 секунды для полной загрузки всех элементов
});
