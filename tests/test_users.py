import pytest
from flask import url_for


def test_login_page(test_client):
    response = test_client.get(url_for('auth.login'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Sign In' in response.data
    assert b'Register' in response.data

def test_home_page_posts(test_client, init_db):
    response = test_client.post(url_for('auth.login'), data=dict(
                                username='susan', password='dog'),
                                follow_redirects=True)
    assert response.status_code == 200
    response = test_client.post(url_for('main.index'), data=dict(
                                post='test post'), follow_redirects=True)
    assert b'Your post is now live!' in response.data
    assert b'test post' in response.data

def test_valid_login_logout(test_client, init_db):
    response = test_client.post(url_for('auth.login'), data=dict(
                                        username='susan', password='dog'),
                                        follow_redirects=True)
    assert response.status_code == 200
    assert b'Hello, susan!' in response.data
    assert b'What are you grateful for?' in response.data
    assert b'Profile' in response.data
    assert b'Logout' in response.data
    assert b'Login' not in response.data
    assert b'Register' not in response.data

    response = test_client.get(url_for('auth.logout'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Profile' not in response.data
    assert b'Logout' not in response.data
    assert b'Login' in response.data
    print(response.data)
    assert b'See what other people are saying:' in response.data

def test_invalid_login(test_client, init_db):
    response = test_client.post(url_for('auth.login'), data=dict(
                                        username='susan', password='cat'),
                                        follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid username or password' in response.data
    assert b'Login' in response.data

def test_invalid_registration(test_client, init_db):
    response = test_client.post(url_for('auth.register'), data=dict(
                                username='jimmy', email='jimmy@example.com',
                                password='bird', password2='bird2'),
                                follow_redirects=True)
    assert response.status_code == 200
    print(response.data)
    assert b'Field must be equal to password.' in response.data

    response = test_client.post(url_for('auth.register'), data=dict(
                                username='jimmy', email='jimmy123',
                                password='bird', password2='bird'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid email address.' in response.data

    response = test_client.post(url_for('auth.register'), data=dict(
                                username='susan', email='jimmy@example.com',
                                password='bird', password2='bird'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Please use a different username.' in response.data

def test_valid_registration(test_client, init_db):
    response = test_client.post(url_for('auth.register'), data=dict(
                                username='jimmy', email='jimmy@example.com',
                                password='bird', password2='bird'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Congratulations, you are now a registered user!' in response.data
    assert b'Login' in response.data

    response = test_client.post(url_for('auth.login'), data=dict(
                                        username='jimmy', password='bird'),
                                        follow_redirects=True)
    assert response.status_code == 200
    assert b'Hello, jimmy!' in response.data
