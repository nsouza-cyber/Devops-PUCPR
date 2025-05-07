import pytest
from app import app, tasks

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def clear_tasks():
    tasks.clear()

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'To-Do List' in response.data

def test_add_task(client):
    response = client.post('/add', data={'task': 'Test Task'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Test Task' in response.data

def test_complete_task(client):
    client.post('/add', data={'task': 'Complete Task'}, follow_redirects=True)
    response = client.get('/complete/0', follow_redirects=True)
    assert response.status_code == 200
    assert b'<s>Complete Task</s>' in response.data

def test_delete_task(client):
    client.post('/add', data={'task': 'Delete Task'}, follow_redirects=True)
    response = client.get('/delete/0', follow_redirects=True)
    assert response.status_code == 200
    assert b'Delete Task' not in response.data
