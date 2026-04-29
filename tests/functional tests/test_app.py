
import sys
import pytest
from flask import url_for
sys.path.append('C:\\Users\\user\\Documents\\CIT term 2\\Agile project\\second repository\\CIT-Agile-Project') # Adjust the path accordingly
from app import app, db
import random

#make sure you run manage.py before doing the unit test
#run with python -m pytest --cov
#run on cit agile project


from models import Food, Meal, FoodMeal, User
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Home' in response.data
    assert b'Login' in response.data
    assert b'Add New' in response.data
    assert b'Homepage' in response.data
    assert b'Users' in response.data
    assert b'Food' in response.data
    assert b'My Food Tracker' in response.data

def test_login(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Username' in response.data
    assert b'Password' in response.data

#addnew works
def test_wrong(client):
    response = client.get('/dog')
    assert response.status_code == 404

def test_addnew(client):
    response = client.get('/addnew')
    assert response.status_code == 200
    assert b'Add user' in response.data
    assert b'Add food' in response.data

def test_users_list(client):
    response = client.get('/users')
    assert response.status_code == 200
    assert b'Users' in response.data


def test_food_list(client):
    response = client.get('/food')
    assert response.status_code == 200
    assert b'Food' in response.data


def test_add_user(client):
    data = {'name': f"Test User {random.randint(1, 1000)}", 'password': 'password', 'phone': '1234567890', 'height': '170', 'weight': '60', 'gender': 'male', 'age': '25', 'activity_level': '1.2'}
    response = client.post('/adduser', data=data, follow_redirects=True)
    assert response.status_code == 200
  
def test_add_meal(client):
    data = {'name': f"Test User {random.randint(1, 1000)}", 'food_id': '1', 'amount': '2'}
    response = client.post('/users/1/addmeal', data=data, follow_redirects=True)
    assert response.status_code == 200
 
def test_delete_meal(client):
    response = client.post('/users/1/deletemeal/1', follow_redirects=True)
    assert response.status_code == 200

def test_delete_foodmeal(client):
    response = client.post('/users/1/deletefoodmeal/1', follow_redirects=True)
    assert response.status_code == 200

def test_login_post(client):
    data = {'username': 'Test User', 'password': 'password'}
    response = client.post('/loginpost', data=data, follow_redirects=True)
    assert response.status_code == 200


def test_add_food(client):
    data = {'name': f"Test food {random.randint(1, 1000)}", 'calories': '100', 'protein': '10', 'fat': '5', 'carbs': '20'}
    response = client.post('/addfood', data=data, follow_redirects=True)
    assert response.status_code == 200



#post("/api/products/", {"name": "ribeye steak", "price": 25.99})
