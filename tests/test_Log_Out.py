"""Log out from account feature tests."""
from project.account import *
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
    parsers
)

@scenario('features/Log_Out.feature', 'Log out of account while logged out (Error flow)')
def test_log_out_of_account_while_logged_out_error_flow():
    pass


@scenario('features/Log_Out.feature', 'Log out of account while logged in (Normal flow)')
def test_log_out_of_account_while_logged_in_normal_flow():
    pass


@given(parsers.parse('account with email "{email}" and password "{password}" exists in the system'))
def account_with_email_testtestcom_and_password_kul32_exists_in_the_system(app, email, password):
    with app.app_context():
        if search_account_by_email(email):
            assert True
        else:
            res = db_save_account("Dummy", email, password)
            assert res[1] is None


@given(parsers.parse('user with email "{email}" and password "{password}" is logged into the system'))
def user_with_email_testtestcom_and_password_kul32_is_logged_into_the_system(client, email, password):
    payload = {'email': email, 'password': password}
    client.post('/login', data=payload)
    with client.session_transaction() as session:
        assert "id" in session


@given('the user is not logged into the system')
def the_user_is_not_logged_into_the_system(client):
    with client.session_transaction() as session:
        if "id" in session:
            session.pop('id', None)
        assert not ("id" in session)


@when('a log out operation is requested')
def a_log_out_operation_is_requested(client):
    client.get('/logout')


@then('the system retains the state for the user as logged out')
def the_system_retains_the_state_for_the_user_as_logged_out(client):
    with client.session_transaction() as session:
        assert not ("id" in session)


@then('the system updates the state for the user "test@test.com" to logged out')
def the_system_updates_the_state_for_the_user_testtestcom_to_logged_out(client):
    with client.session_transaction() as session:
        assert not ("id" in session)
