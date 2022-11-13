"""Log in to account feature tests."""

from project.account import *
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
    parsers
)

@scenario('features/Login_Account.feature', 'Log in to a non-existing account (Error Flow)')
def test_log_in_to_a_nonexisting_account_error_flow():
    pass


@scenario('features/Login_Account.feature', 'Log in to an existing account with email & password (Normal Flow)')
def test_log_in_to_an_existing_account_with_email__password_alternate_flow():
    pass


@scenario('features/Login_Account.feature', 'Log in to an existing account with incorrect password (Error Flow)')
def test_log_in_to_an_existing_account_with_incorrect_password_error_flow():
    pass

@given(parsers.parse('an account by the email "{email}" does not exist within the system'))
def an_account_by_the_name_acc1_does_not_exist_within_the_system(app, email):
    with app.app_context():
        if search_account_by_email(email):
            _id = search_account_by_email(email)[0]
            delete_account_by_id(_id)

        res = search_account_by_email(email)
        assert res is None


@given(
    parsers.parse('an account by the name "{name}", email "{email}", password "{password}" exists within the system'))
def an_account_by_the_name_acc1_email_abcmailcom_password_123_exists_within_the_system(app, name, email, password):
    with app.app_context():
        if search_account_by_email(email):
            assert True
        else:
            res = db_save_account(name, email, password)
            assert res[1] is None


@given('the user is not logged into the system')
def the_user_is_not_logged_into_the_system(client):
    with client.session_transaction() as session:
        assert not ("id" in session)

@when(parsers.parse('requesting to log in to account with email "{email}" and password "{password}"'))
def requesting_to_log_in_to_account_with_email_abcmailcom_with_password_123(client, email, password):
    payload = {'email': email, 'password': password}
    client.post('/login', data=payload)

@when(parsers.parse('requesting to log in to account with email "{email}" and password "{password}"'))
def requesting_to_log_in_to_account_with_email_abcmailcom_and_password_231(client, email, password):
    payload = {'email': email, 'password': password}
    client.post('/login', data=payload)

# Not supported by API
@then(parsers.parse('a "{message}" message is issued'))
def a_incorrect_username_or_password_message_is_issued():
    pass


@then(parsers.parse('the system updates the state for the user to be logged into account "{name}"'))
def the_system_updates_the_state_for_the_user_to_be_logged_into_account_acc1(client, name):
    with client.session_transaction() as session:
        assert session["id"] == search_account_by_name(name)[0]


@then('the user is not logged into the system')
def the_user_is_not_logged_into_the_system(client):
    with client.session_transaction() as session:
        assert not ("id" in session)
