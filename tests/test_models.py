import pytest


def test_new_user(new_user):
    assert new_user.email == 'john@example.com'
    assert new_user.password_hash != 'cat'
    assert new_user.check_password('cat')

def test_set_password(new_user):
    new_user.set_password('dog')
    assert not new_user.check_password('cat')
    assert new_user.password_hash != 'dog'
    assert new_user.check_password('dog')

def test_avatar(new_user):
    assert new_user.avatar(128) == 'https://www.gravatar.com/avatar/' \
                                   'd4c74594d841139328695756648b6bd6' \
                                   '?d=identicon&s=128'
