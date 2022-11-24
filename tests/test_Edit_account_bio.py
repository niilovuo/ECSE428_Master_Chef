"""Edit account bio feature tests."""

from flask import session
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
)


@scenario('features/Edit_account_bio.feature', 'Add an account bio (Normal Flow)')
def test_add_an_account_bio_normal_flow(app):
    """Add an account bio (Normal Flow)."""
    pass


@scenario('features/Edit_account_bio.feature', 'Edit an account bio (Alternate Flow)')
def test_edit_an_account_bio_alternate_flow(app):
    """Edit an account bio (Alternate Flow)."""
    pass


@scenario('features/Edit_account_bio.feature', 'Logged out user attempts to edit an account bio (Error Flow)')
def test_logged_out_user_attempts_to_edit_an_account_bio_error_flow(app):
    """Logged out user attempts to edit an account bio (Error Flow)."""
    pass


@given('a "It\'s nice to meet you" message in the bio')
def itsNiceToMeetYouInBio(postgresql):
    """a "It's nice to meet you" message in the bio."""
    cur = postgresql.cursor()
    cur.execute("UPDATE accounts SET bio = %s WHERE id = %s;", ("It's nice to meet you", 1))
    postgresql.commit()


@given('a default "Hello" in bio')
def defaultHelloInBio(postgresql):
    """a default "Hello" in bio."""
    pass  # Default


@given('a user of Master Chef is logged into the system')
def masterChefIsLoggedIn(client, postgresql):
    """a user of Master Chef is logged into the system."""
    cur = postgresql.cursor()
    cur.execute("INSERT INTO accounts VALUES (1, 'Master Chef', 'gordon.ramsay@mail.com', '1234', 'Hello')")
    cur.execute("INSERT INTO accounts VALUES (2, 'Not Master Chef', 'jamie.oliver@mail.com', '1234', 'Hello')")
    postgresql.commit()
    with client.session_transaction() as session:
        session['id'] = 1


@given('a user of Master Chef is not logged into the system')
def masterChefIsNotLoggedIn(postgresql):
    """a user of Master Chef is not logged into the system."""
    # Still create Master Chef & Not Master Chef User
    cur = postgresql.cursor()
    cur.execute("INSERT INTO accounts VALUES (1, 'Master Chef', 'gordon.ramsay@mail.com', '1234', 'Hello')")
    cur.execute("INSERT INTO accounts VALUES (2, 'Not Master Chef', 'jamie.oliver@mail.com', '1234', 'Hello')")
    postgresql.commit()


@given('bio belongs to the Master Chef user', target_fixture='acc')
def bioBelongsToMasterChef(postgresql, client):
    """bio belongs to the Master Chef user."""
    cur = postgresql.cursor()
    cur.execute("SELECT * FROM accounts WHERE id = %s", (1,))
    acc = cur.fetchone()
    return acc  # Retrieve correct account


@when('requesting to add a "It\'s nice to meet you" message', target_fixture='response')
def addItsNiceToMeetYouMessage(client):
    """requesting to add a "It's nice to meet you" message."""
    response = client.post("/setting",
        data={
            "current_passwd": '',
            "new_passwd": '',
            "confirm_passwd": '',

           'submit-profile': True,
           'NewName': '',
           'NewBio': "It's nice to meet you",
           'NewEmail': ''
        }
    )
    return response


@when('requesting to edit a bio', target_fixture='response')
def requestToEditBio(client):
    """requesting to edit a bio."""
    response = client.post("/setting",
        data={
            "current_passwd": '',
            "new_passwd": '',
            "confirm_passwd": '',

           'submit-profile': True,
           'NewName': '',
           'NewBio': "edit",
           'NewEmail': ''
        }
    )
    return response


@when('requesting to edit a bio to "It\'s really nice to meet you" message', target_fixture='response')
def addItsReallyNiceToMeetYouMessage(client):
    response = client.post("/setting",
        data={
            "current_passwd": '',
            "new_passwd": '',
            "confirm_passwd": '',

            'submit-profile': True,
            'NewName': '',
            'NewBio': "It's really nice to meet you",
            'NewEmail': ''
        }
    )
    return response


@when('user confirms the changes to be saved')
def userConfirmsChangesSaved():
    """user confirms the changes to be saved."""
    pass  # Frontend detail


@then('the system will change the "It\'s nice to meet you" message to the requested "It\'s really nice to meet you"')
def systemChangesItsNiceToMeetYouToItsReallyNiceToMeetYou(postgresql, acc):
    """the system will change the "It's nice to meet you" message to the requested "It's really nice to meet you"."""
    cur = postgresql.cursor()
    cur.execute("SELECT * FROM accounts WHERE id = %s", (acc[0],))
    acc = cur.fetchone()
    assert acc[4] == "It's really nice to meet you"


@then('the system will change the default message to the requested "It\'s nice to meet you"')
def systemChangesHelloToItsReallyNiceToMeetYou(postgresql, acc):
    """the system will change the default message to the requested "It's nice to meet you"."""
    cur = postgresql.cursor()
    cur.execute("SELECT * FROM accounts WHERE id = %s", (acc[0],))
    acc = cur.fetchone()
    assert acc[4] == "It's nice to meet you"


@then('the system will issue an "Invalid edit" error message')
def systemIssuesInvalidEdit(response):
    """the system will issue an "Invalid edit" error message."""
    assert response.status_code == 302  # Logic does not return a message, but rather flashes it and redirects
