"""Follow Account feature tests."""

import pytest
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
    parsers
)

from project.followers import follow_account_by_id
from project.account import search_account_by_id

@scenario('features/Follow_Account.feature', 'Follow a user')
def test_follow_a_user(app):
    pass


@scenario('features/Follow_Account.feature', 'Follow a user whose account has been deleted')
def test_follow_a_user_whose_account_has_been_deleted(app):
    pass


@scenario('features/Follow_Account.feature', 'Follow a user without logging in')
def test_follow_a_user_while_not_logged_in(app):
    pass

@given('I have registered in the system', target_fixture="user_id")
def i_have_registered_in_the_system(postgresql):
    cur = postgresql.cursor()
    cur.execute("INSERT INTO accounts VALUES (DEFAULT, 'owner', 'Dummy', 'Dummy', '') RETURNING id")
    user_id = cur.fetchone()[0]
    postgresql.commit()
    return user_id

@given('I log in to my account', target_fixture="user_id")
def i_log_in_to_my_account(user_id, client):
    with client.session_transaction() as session:
        session['id'] = user_id
        return user_id

@given('I did not follow that user before', target_fixture="account_id")
def i_did_not_follow_that_user_before(postgresql):
    cur = postgresql.cursor()
    cur.execute("INSERT INTO accounts VALUES (DEFAULT, 'test', 'test', 'test', '') RETURNING id")
    account_id = cur.fetchone()[0]
    return account_id

@given('this user exists in the system')
def this_user_exists_in_the_system():
    pass

@when('I follow this user', target_fixture='res')
def i_follow_this_user(user_id, account_id):
    res = follow_account_by_id(account_id, user_id)
    return res

@then('the user join my following list')
def the_user_join_my_following_list(postgresql, account_id, user_id, res):
    cur = postgresql.cursor()
    cur.execute("""
                       SELECT * FROM followers WHERE account = %s AND follower = %s
                       """, (account_id, user_id))
    follow = cur.fetchone()
    assert follow is not None
    assert res is None

@given("this user's account has been deleted")
def this_users_account_has_been_deleted(postgresql, account_id):
    cur = postgresql.cursor()
    cur.execute("""
            DELETE FROM accounts WHERE id = %s
            """, (account_id,))
    postgresql.commit()

@then('an error message is prompted "This user does not exist"')
def an_error_message_is_prompted_this_user_does_not_exist(res):
    assert res == "This user does not exist"

@given('I have not logged in to my account', target_fixture='user_id')
def i_have_not_logged_in_to_my_account(client):
    with client.session_transaction() as session:
        session['id'] = None
        return None

@then('an error message is prompted "You must log in before follow a user"')
def an_error_message_is_prompted_you_must_log_in_before_follow_a_user(res):
    assert res == "You must log in before follow a user"
