from project.account import *
from werkzeug.security import check_password_hash

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



def test_save_new_account(monkeypatch):
    monkeypatch.setattr("project.db.AccountRepo.insert_row", lambda x, y, z: 0)
    (id, err) = db_save_account("bob", "bob@gmail.com", "Abcd1234")

    assert err is None

def test_save_dup_name(monkeypatch):
    monkeypatch.setattr("project.db.AccountRepo.insert_row", lambda x, y, z: 1 // 0)
    monkeypatch.setattr("project.db.AccountRepo.select_by_name",
                        lambda x: ("bob", "bob@gmail.com", "aBCD1234"))

    (id, err) = db_save_account("bob", "bob@outlook.com", "abCD1234")

    assert id is None
    assert err == "This account name is already in use"

def test_save_dup_email(monkeypatch):
    monkeypatch.setattr("project.db.AccountRepo.insert_row", lambda x, y, z: 1 // 0)
    monkeypatch.setattr("project.db.AccountRepo.select_by_name", lambda x: None)
    monkeypatch.setattr("project.db.AccountRepo.select_by_email",
                        lambda x: ("bob", "bob@gmail.com", "abcd1234"))

    (id, err) = db_save_account("bobby", "bob@gmail.com", "aBCd1234")

    assert id is None
    assert err == "This email is already bound to an account"

