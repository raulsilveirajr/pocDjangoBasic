# FILE: todos/tests.py
from datetime import date

import pytest
from django.urls import reverse
from django.test import Client

from todos.models import Todo

@pytest.mark.django_db
def test_todo_list():
  client = Client()
  response = client.get(reverse('todo_list'))
  assert response.status_code == 200

@pytest.mark.django_db
def test_create_view_creates_todo():
    client = Client()
    response = client.post(reverse('todo_create'), {'title': 'New Todo', 'deadline': '2023-12-31'})
    assert response.status_code == 302
    assert Todo.objects.filter(title='New Todo').exists()

@pytest.mark.django_db
def test_create_view_redirects_to_todo_list():
    client = Client()
    response = client.post(reverse('todo_create'), {'title': 'New Todo', 'deadline': '2023-12-31'})
    assert response.status_code == 302
    assert response.url == reverse('todo_list')

@pytest.mark.django_db
def test_create_view_handles_invalid_data():
    client = Client()
    response = client.post(reverse('todo_create'), {'title': '', 'deadline': ''})
    assert response.status_code == 200
    assert 'This field is required.' in response.content.decode()

@pytest.mark.django_db
def test_todo_complete_not_found():
  client = Client()
  response = client.get(reverse('todo_complete', args=[1]))
  assert response.status_code == 404

@pytest.mark.django_db
def test_todo_complete_completes_todo():
    client = Client()
    todo = Todo.objects.create(title='Test Todo', deadline='2023-12-31', finished_at='2023-12-31')
    response = client.get(reverse('todo_complete', args=[todo.id]))
    assert response.status_code == 302
    assert Todo.objects.get(id=todo.id).finished_at == date.today()

@pytest.mark.django_db
def test_todo_update_not_found():
  client = Client()
  response = client.get(reverse('todo_update', args=[1]))
  assert response.status_code == 404

@pytest.mark.django_db
def test_todo_update_updates_todo():
    client = Client()
    todo = Todo.objects.create(title='Test Todo', deadline='2023-12-31')
    response = client.post(reverse('todo_update', args=[todo.id]), {'title': 'Updated Todo', 'deadline': '2023-12-31'})
    assert response.status_code == 302
    assert Todo.objects.get(id=todo.id).title == 'Updated Todo'

@pytest.mark.django_db
def test_todo_delete_not_found():
  client = Client()
  response = client.get(reverse('todo_delete', args=[1]))
  assert response.status_code == 404

@pytest.mark.django_db
def test_todo_delete_deletes_todo():
    client = Client()
    todo = Todo.objects.create(title='Test Todo', deadline='2023-12-31')
    response = client.post(reverse('todo_delete', args=[todo.id]))
    assert response.status_code == 302
    assert not Todo.objects.filter(id=todo.id).exists()

# Add a test to check used templates

@pytest.mark.django_db
def test_todo_list_template():
    client = Client()
    response = client.get(reverse('todo_list'))
    assert response.status_code == 200
    assert 'todos/todo_list.html' in [t.name for t in response.templates]

# Add a test for the TodoCreateView that checks if the template used is todos/todo_form.html.
@pytest.mark.django_db
def test_todo_create_template():
    client = Client()
    response = client.get(reverse('todo_create'))
    assert response.status_code == 200
    assert 'todos/todo_form.html' in [t.name for t in response.templates]

# Add a test for the TodoUpdateView that checks if the template used is todos/todo_form.html.
@pytest.mark.django_db
def test_todo_update_template():
    client = Client()
    todo = Todo.objects.create(title='Test Todo', deadline='2023-12-31')
    response = client.get(reverse('todo_update', args=[todo.id]))
    assert response.status_code == 200
    assert 'todos/todo_form.html' in [t.name for t in response.templates]

# Add a test for the TodoDeleteView that checks if the template used is todos/todo_confirm_delete.html.
@pytest.mark.django_db
def test_todo_delete_template():
    client = Client()
    todo = Todo.objects.create(title='Test Todo', deadline='2023-12-31')
    response = client.get(reverse('todo_delete', args=[todo.id]))
    assert response.status_code == 200
    assert 'todos/todo_confirm_delete.html' in [t.name for t in response.templates]
