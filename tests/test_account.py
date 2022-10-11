from project.account import *

def test_normalize_valid_info():
    ((n, e, p), err) = normalize_account_info("bob", "bob@gmail.com", "Abcd1234")

    assert n == "bob"
    assert e == "bob@gmail.com"
    assert p == "Abcd1234"
    assert err is None

def test_normalize_blank_name():
    (r, err) = normalize_account_info("  ", "bob@gmail.com", "Abcd1234")

    assert r is None
    assert err == "The account name cannot be blank"

def test_normalize_name_with_symbols():
    (r, err) = normalize_account_info("b@b", "bob@gmail.com", "Abcd1234")

    assert r is None
    assert err == "The account name must be alphanumeric or underscore"

def test_normalize_malformed_email():
    (r, err) = normalize_account_info("bob", "bobgmail.com", "Abcd1234")

    assert r is None
    assert err == "The email is malformed"

def test_normalize_blank_password():
    (r, err) = normalize_account_info("bob", "bob@gmail.com", "     ")

    assert r is None
    assert err == "The password cannot be blank"

def test_normalize_short_password():
    (r, err) = normalize_account_info("bob", "bob@gmail.com", "q")

    assert r is None
    assert err == "The password must be at least 4 characters"

def test_normalize_password_with_spaces():
    (r, err) = normalize_account_info("bob", "bob@gmail.com", "q w e r t y")

    assert r is None
    assert err == "The password cannot contain spaces"

