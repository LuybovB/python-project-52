
{% extends "base.html" %}

{% load i18n %}
{% load django_bootstrap5 %}

{% block content %}
<form method="post">
  {% csrf_token %}
  <label for="status">Статус:</label>
  <select name="status" id="status">
  <option value="">----</option>
  {% for status in statuses %}
    <option value="{{ status.id }}"> {{ status.name }}</option>
  {% endfor %}
</select>
  <input type="submit" value="Сохранить">
</form>

{% endblock content %}


{% extends 'base.html' %}
{% load static %}
{% load i18n %}

{% block title %}
  {% trans 'Создание задачи' %}
{% endblock %}

{% block content %}
  <div class="task-create-container">
    <h2>{% trans 'Создание задачи' %}</h2>
    <form method="post" class="task-create-form">
      {% csrf_token %}
      <div class="form-group">
        <label for="id_name">{% trans 'Имя' %}:</label>
        <input type="text" id="id_name" name="name" class="form-control" placeholder="{% trans 'Введите имя задачи' %}">
      </div>
      <div class="form-group">
        <label for="id_description">{% trans 'Описание' %}:</label>
{% elif field.name == 'description' %}
<label for="id_description">{% trans 'Описание' %}:</label>
        <textarea id="id_description" name="description" class="form-control" placeholder="{% trans 'Введите описание задачи' %}"></textarea>
      </div>
      <div class="form-group">
        <label for="status">{% trans 'Статус' %}:</label>
        <select name="status" id="status" class="form-control">
          <option value="" selected disabled>----</option>
          <option value="" disabled>{% trans 'Выберите статус' %}</option>
          {% for status in statuses %}
            <option value="{{ status.id }}">{{ status.name }}</option>
          {% empty %}
            <option value="" disabled>{% trans 'Нет доступных статусов' %}</option>
          {% endfor %}
        </select>
      </div>
      <div class="form-group">
        <label for="assigned_to">{% trans 'Исполнитель' %}:</label>
        <select name="assigned_to" id="assigned_to" class="form-control">
          <option value="" selected disabled>----</option>
          <option value="" disabled>{% trans 'Выберите исполнителя' %}</option>
          {% for user in users %}
            <option value="{{ user.id }}">{{ user.username }}</option>
          {% empty %}
            <option value="" disabled>{% trans 'Нет доступных исполнителей' %}</option>
          {% endfor %}
        </select>
      </div>
      <div class="form-group">
        <label for="label">{% trans 'Метки' %}:</label>
        <input type="text" id="label" name="label" class="form-control form-control-sm" placeholder="{% trans 'Введите метку' %}">
      </div>
      <button type="submit" class="btn btn-primary">{% trans 'Сохранить' %}</button>
    </form>
  </div>
{% endblock %}

{% block css %}
  <link rel="stylesheet" href="{% static 'css/task-create.css' %}">
{% endblock %}
