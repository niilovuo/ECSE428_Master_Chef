"""Log in to account feature tests."""

from pytest_bdd import (
    given,
    scenario,
    then,
    when,
)


@scenario('features\Login_Account.feature', 'Log in to a non-existing account (Error Flow)')
def test_log_in_to_a_nonexisting_account_error_flow():
    """Log in to a non-existing account (Error Flow)."""
    pass


@scenario('features\Login_Account.feature', 'Log in to an existing account with email & password (Alternate Flow)')
def test_log_in_to_an_existing_account_with_email__password_alternate_flow():
    """Log in to an existing account with email & password (Alternate Flow)."""


@scenario('features\Login_Account.feature', 'Log in to an existing account with incorrect password (Error Flow)')
def test_log_in_to_an_existing_account_with_incorrect_password_error_flow():
    """Log in to an existing account with incorrect password (Error Flow)."""


@scenario('features\Login_Account.feature', 'Log in to an existing account with username & password (Normal Flow)')
def test_log_in_to_an_existing_account_with_username__password_normal_flow():
    pass

@given('an account by the name "acc1" does not exist within the system')
def an_account_by_the_name_acc1_does_not_exist_within_the_system():
    """an account by the name "acc1" does not exist within the system."""
    raise NotImplementedError


@given('an account by the name "acc1", email "abc@mail.com", password "123" exists within the system')
def an_account_by_the_name_acc1_email_abcmailcom_password_123_exists_within_the_system():
    """an account by the name "acc1", email "abc@mail.com", password "123" exists within the system."""
    raise NotImplementedError


@given('the user is not logged into the system')
def the_user_is_not_logged_into_the_system():
    """the user is not logged into the system."""
    raise NotImplementedError


@when('requesting to log in to account called "acc1" with password "123"')
def requesting_to_log_in_to_account_called_acc1_with_password_123():
    """requesting to log in to account called "acc1" with password "123"."""
    raise NotImplementedError


@when('requesting to log in to account with email "abc@mail.com" with password "123"')
def requesting_to_log_in_to_account_with_email_abcmailcom_with_password_123():
    """requesting to log in to account with email "abc@mail.com" with password "123"."""
    raise NotImplementedError

    raise NotImplementedError


@then('a "Incorrect username or password" message is issued')
def a_incorrect_username_or_password_message_is_issued():
    """a "Incorrect username or password" message is issued."""
    raise NotImplementedError


@then('the system updates the state for the user to be logged into account "acc1"')
def the_system_updates_the_state_for_the_user_to_be_logged_into_account_acc1():
    """the system updates the state for the user to be logged into account "acc1"."""
    raise NotImplementedError


@then('the user is not logged into the system')
def the_user_is_not_logged_into_the_system():
    """the user is not logged into the system."""
    raise NotImplementedError
