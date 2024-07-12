import pytest
from main import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_main(client):
    response = client.get('/')
    text_data = response.get_data(as_text=True)
    assert response.status_code == 200
    assert text_data == 'hola'
    

def test_get_books(client):
    response = client.get('/book')
    json_data = response.get_json()
    assert response.status_code == 200
    assert isinstance(json_data, list)
    

def test_create_book(client):
    new_book = {
        'isbn': '1234567890',
        'title': 'Test Book',
        'author': 'Test Author',
        'quantity': 10,
        'current_price': 9.99
    }
    response = client.post('/book', json=new_book)
    json_data = response.get_json()
    assert response.status_code == 201
    assert json_data['message'] == 'Book created successfully'
    assert json_data['book']['title'] == new_book['title']


