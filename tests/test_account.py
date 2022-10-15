from project.account import *
from werkzeug.security import check_password_hash

def gen_scenario_helper():
    entries = [
        # id acc     email               passwd
        (0, "Test",  "test1@gmail.com", "Test1"),
        (1, "Test2", "test2@gmail.com", "Test2")
    ]

    def insert_row(name, email, password):
        for entry in entries:
            if entry[1] == name or entry[2] == email:
                raise Exception("Bad")

        id = len(entries)
        entries.append((id, name, email, password))
        return id

    def select_by_name(name):
        for entry in entries:
            if entry[1] == name:
                return entry
        return None

    def select_by_email(email):
        for entry in entries:
            if entry[2] == email:
                return entry
        return None

    return (insert_row, select_by_name, select_by_email)

def test_scenario_New_user_creates_an_account(monkeypatch):
    """
    Given the user is not logged into the system
    When attempting to create an account "newAccount1", with email "newAccount1@gmail.com" and password "newAccount1"
    Then the account name shall exist in the system
    And the system will remember my email
    And the system will remember my password
    """

    (insert_row, select_by_name, select_by_email) = gen_scenario_helper()
    monkeypatch.setattr("project.db.AccountRepo.insert_row", insert_row)
    monkeypatch.setattr("project.db.AccountRepo.select_by_name", select_by_name)
    monkeypatch.setattr("project.db.AccountRepo.select_by_email", select_by_email)

    err = add_new_account("newAccount1", "newAccount1@gmail.com", "newAccount1")
    assert err is None

    res = select_by_name("newAccount1")
    assert res[1] == "newAccount1"
    assert res[2] == "newAccount1@gmail.com"
    assert check_password_hash(res[3], "newAccount1")

def test_scenario_New_user_creates_an_account_with_used_account_name(monkeypatch):
    """
    Given the user is not logged into the system
    When attempting to create an account "Test", with email "newAccount2@gmail.com" and password "newAccount2"
    Then the "This account name is already in use" error message is issued
    And the account name "Test" is associated with the email "test1@gmail.com"
    """

    (insert_row, select_by_name, select_by_email) = gen_scenario_helper()
    monkeypatch.setattr("project.db.AccountRepo.insert_row", insert_row)
    monkeypatch.setattr("project.db.AccountRepo.select_by_name", select_by_name)
    monkeypatch.setattr("project.db.AccountRepo.select_by_email", select_by_email)

    err = add_new_account("Test", "newAccount2@gmail.com", "newAccount2")
    assert err == "This account name is already in use"

    res = select_by_name("Test")
    assert res[2] == "test1@gmail.com"

def test_scenario_A_user_creates_another_account(monkeypatch):
    """
    Given the user is not logged into the system
    When attempting to create an account "newAccount3", with email "test1@gmail.com" and password "newAccount3"
    Then the "This email is already bound to an account" error message is issued
    And the account name "Test" is associated with the email "test1@gmail.com"
    """

    (insert_row, select_by_name, select_by_email) = gen_scenario_helper()
    monkeypatch.setattr("project.db.AccountRepo.insert_row", insert_row)
    monkeypatch.setattr("project.db.AccountRepo.select_by_name", select_by_name)
    monkeypatch.setattr("project.db.AccountRepo.select_by_email", select_by_email)

    err = add_new_account("newAccount3", "test1@gmail.com", "newAccount3")
    assert err == "This email is already bound to an account"

    res = select_by_name("Test")
    assert res[2] == "test1@gmail.com"


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

