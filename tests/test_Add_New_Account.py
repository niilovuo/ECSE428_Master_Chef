"""Add New Account feature tests."""

import json
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
    parsers
)
from project.db import AccountRepo
from project.account import *
from werkzeug.security import check_password_hash


@scenario('features/Add_New_Account.feature', 'A user creates another account (Error Flow)')
def test_a_user_creates_another_account_error_flow(app):
    pass


@scenario('features/Add_New_Account.feature', 'New user creates an account (Normal Flow)')
def test_new_user_creates_an_account_normal_flow(app):
    pass


@scenario('features/Add_New_Account.feature', 'New user creates an account with used account name (Error Flow)')
def test_new_user_creates_an_account_with_used_account_name_error_flow(app):
    pass

@given(parsers.parse('the following accounts exist in the system\n{table_data}'))
def the_following_accounts_exist_in_the_system(table_data):
    table_data = json.loads(table_data)
    for (name, password, email) in table_data[1:]:
        db_save_account(name, email, password)

@given('the user is not logged into the system')
def the_user_is_not_logged_into_the_system():
    pass


@when(parsers.parse('attempting to create an account "{name}", with email "{email}" and password "{password}"'), target_fixture="res")
def attempting_to_create_an_account__with_email__and_password_(name, email, password):
    res = add_new_account(name, email, password)
    return res


@then('the operation should succeed')
def the_operation_should_succeed(res):
    assert res is None


@then(parsers.parse('the "{msg}" error message is issued'))
def the_this_account_name_is_already_in_use_error_message_is_issued(res, msg):
    assert res == msg


@then(parsers.parse('the account name "{name}" is associated with the email "{email}"'))
def the_account_name__is_associated_with_the_email_(name, email):
    assert AccountRepo.select_by_name(name)[2] == email


@then(parsers.parse('the account name "{name}" is associated with the password "{password}"'))
def the_account_name__is_associated_with_the_password_(name, password):
    assert check_password_hash(AccountRepo.select_by_name(name)[3], password)

