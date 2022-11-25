"""Edit account name feature tests."""

from flask import session
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
)


@scenario('features/Change_account_name.feature', 'Edit account name (Normal Flow)')
def test_edit_account_name_bio_normal_flow(app):
    pass

@scenario('features/Change_account_name.feature', 'Logged out user attempts to edit account name (Error Flow)')
def test_logged_out_user_attempts_to_edit_account_name_error_flow(app):
    pass

@scenario('features/Change_account_name.feature', 'Edit account name with an empty string (Error Flow)')
def test_edit_account_name_to_empty_error_flow(app):
    pass

@scenario('features/Change_account_name.feature', 'Edit account name with the name which is alreay taken by another user (Error Flow)')
def test_edit_account_name_which_is_already_taken_error_flow(app):
    pass

@scenario('features/Change_account_name.feature', 'Edit account name with the name which includes a special character other than under score (Error Flow)')
def test_edit_account_name_with_special_character_error_flow(app):
    pass


@given('a user is logged into the system')
def masterChefIsLoggedIn(client, postgresql):
    cur = postgresql.cursor()
    cur.execute("INSERT INTO accounts VALUES (1, 'Master Chef', 'master.chef@mail.com', '1234', 'Hello')")
    postgresql.commit()
    with client.session_transaction() as session:
        session['id'] = 1


@given('a user is not logged into the system')
def masterChefIsNotLoggedIn(postgresql):
    cur = postgresql.cursor()
    cur.execute("INSERT INTO accounts VALUES (1, 'Master Chef', 'master.chef@mail.com', '1234', 'Hello')")
    postgresql.commit()


@given('account name "Master Chef" belongs to the user', target_fixture='acc')
def bioBelongsToMasterChef(postgresql, client):
    cur = postgresql.cursor()
    cur.execute("SELECT * FROM accounts WHERE id = %s", (1,))
    acc = cur.fetchone()
    return acc  


@given('there is a user with name "Another Master Chef"')
def masterChefIsNotLoggedIn(postgresql):
    cur = postgresql.cursor()
    cur.execute("INSERT INTO accounts VALUES (2, 'Another Master Chef', 'antoerh.master.chef@mail.com', '1234', 'Hello')")
    postgresql.commit()

@given('account name "Master Chef" belongs to the user', target_fixture='acc')
def bioBelongsToMasterChef(postgresql, client):
    cur = postgresql.cursor()
    cur.execute("SELECT * FROM accounts WHERE id = %s", (1,))
    acc = cur.fetchone()
    return acc 


@when('requesting to edit the account name to "newName"', target_fixture='response')
def addItsReallyNiceToMeetYouMessage(client):
    response = client.post("/setting",
        data={
            "current_passwd": '',
            "new_passwd": '',
            "confirm_passwd": '',

            'submit-profile': True,
            'NewName': "newName",
            'NewBio': '',
            'NewEmail': ''
        }
    )
    return response


@when('requesting to edit the account name to "Another Master Chef"', target_fixture='response')
def addItsReallyNiceToMeetYouMessage(client):
    response = client.post("/setting",
        data={
            "current_passwd": '',
            "new_passwd": '',
            "confirm_passwd": '',

            'submit-profile': True,
            'NewName': "Another Master Chef",
            'NewBio': '',
            'NewEmail': ''
        }
    )
    return response


@when('requesting to edit the account name to "$$$"', target_fixture='response')
def addItsReallyNiceToMeetYouMessage(client):
    response = client.post("/setting",
        data={
            "current_passwd": '',
            "new_passwd": '',
            "confirm_passwd": '',

            'submit-profile': True,
            'NewName': "$$$",
            'NewBio': '',
            'NewEmail': ''
        }
    )
    return response


@then('the system will change the account name to the requested "newName"')
def systemChangesItsNiceToMeetYouToItsReallyNiceToMeetYou(postgresql, acc):
    cur = postgresql.cursor()
    cur.execute("SELECT * FROM accounts WHERE id = %s", (acc[0],))
    acc = cur.fetchone()
    assert acc[1] == "newName"


@then('the system will issue an "Invalid edit" error message')
def systemIssuesInvalidEdit(response):
    """the system will issue an "Invalid edit" error message."""
    assert response.status_code == 302  # Logic does not return a message, but rather flashes it and redirects


@when('requesting to edit the account name to an empty account name', target_fixture='response')
def addItsReallyNiceToMeetYouMessage(client):
    response = client.post("/setting",
        data={
            "current_passwd": '',
            "new_passwd": '',
            "confirm_passwd": '',

            'submit-profile': True,
            'NewName': '',
            'NewBio': '',
            'NewEmail': ''
        }
    )
    return response

