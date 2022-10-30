"""Delete Account feature tests."""

import pytest
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
    parsers
)

from project.db import AccountRepo
from project.account import *

@scenario('features/Delete_Account.feature', 'A logged in user attempts to their delete account (Normal Flow)')
def test_delete_an_account_normal_flow(app):
    pass

@scenario('features/Delete_Account.feature', 'Logged out user attempts to delete account (Error Flow)')
def test_delete_an_account_without_logging_in_error_flow(app):
    pass

@pytest.fixture
def a_user(postgresql):
    cur = postgresql.cursor()
    cur.execute("INSERT INTO accounts VALUES (1, 'User1', 'user1@gmail.com', 'password1') RETURNING id")
    user_id = cur.fetchone()[0]
    postgresql.commit()
    return user_id

@given('the user with id "{user_id}" exist in the system', target_fixture="user_id")
def user_info_exisits_int_the_system(user_id):
    cur = postgresql.cursor()
    cur.execute("INSERT INTO accounts VALUES (1, 'User1', 'user1@gmail.com', 'password1') RETURNING id")
    user_id = cur.fetchone()[0]
    postgresql.commit()
    return user_id

@given('the user with id "{user_id}" is logged into the system', target_fixture="user_id")
def user_is_logged_into_the_system(client, a_user):
    with client.session_transaction() as session:
        session['id'] = a_user
        return a_user

@given('the user with id "{user_id}" is not logged into the system', target_fixture="user_id")
def the_user_is_not_logged_into_the_system(client):
    with client.session_transaction() as session:
        session['id'] = None
        return None

@when('attempting to delete their account')
def attempting_to_delete_comment(user_id):
    res = delete_account_by_id(user_id)
    return res

@then(parsers.parse('the user account with id "{user_id}" does not exist'))
def the_account_deleted_successfully(user_id):
    account_id = search_account_by_id(user_id)
    assert account_id is None

@then('the system will display an error message')
def the_account_not_deleted(user_id):
    res = delete_account_by_id(user_id)
    account_id = search_account_by_id(user_id)
    assert account_id is not None
    assert res is "Unknown error occurred. Please try again later"
