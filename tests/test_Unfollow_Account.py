"""Unfollow Account feature tests."""


import pytest
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
    parsers
)

from project.followers import unfollow_account_by_id


@given('I am registered in the system', target_fixture="user_id")
def i_am_registered_in_the_system(postgresql):
    cur = postgresql.cursor()
    cur.execute("INSERT INTO accounts VALUES (DEFAULT, 'owner', 'Dummy', 'Dummy', '') RETURNING id")
    user_id = cur.fetchone()[0]
    postgresql.commit()
    return user_id


@scenario('features/Unfollow_Account.feature', 'Unfollow a user (Normal Flow)')
def test_unfollow_a_user_normal_flow(app):
    pass


@scenario('features/Unfollow_Account.feature', 'Unfollow a user whose account has been deleted (Error Flow)')
def test_unfollow_a_user_whose_account_has_been_deleted_error_flow(app):
    pass


@scenario('features/Unfollow_Account.feature', 'Unfollow a user while not logged in (Error Flow)')
def test_unfollow_a_user_while_not_logged_in_error_flow(app):
    pass


@given("I'm logged in to my account", target_fixture="user_id")
def i_am_logged_in_to_my_account(user_id, client):
    with client.session_transaction() as session:
        session['id'] = user_id
        return user_id


@given("I'm not logged in to my account", target_fixture="user_id")
def i_am_not_logged_in_to_my_account(client):
    with client.session_transaction() as session:
        session['id'] = None
        return None


@given("I followed a user before", target_fixture="account_id")
def i_followed_a_user_before(postgresql, user_id):
    cur = postgresql.cursor()
    cur.execute("INSERT INTO accounts VALUES (DEFAULT, 'test', 'test', 'test', '') RETURNING id")
    account_id = cur.fetchone()[0]
    cur.execute("""INSERT INTO followers VALUES (%s, %s)""", (account_id, user_id))
    postgresql.commit()
    return account_id


@given("this user exists in the system")
def this_user_exists_in_the_system():
    pass


@given("this user's account has been deleted")
def this_users_account_has_been_deleted(postgresql, account_id):
    cur = postgresql.cursor()
    cur.execute("""
            DELETE FROM accounts WHERE id = %s
            """, (account_id,))
    postgresql.commit()


@when("I unfollow this user", target_fixture="res")
def i_unfollow_this_user(user_id, account_id):
    res = unfollow_account_by_id(account_id, user_id)
    return res


@then("the user no longer in my following list")
def the_user_no_longer_in_my_following_list(postgresql, account_id, user_id, res):
    cur = postgresql.cursor()
    cur.execute("""
                   SELECT * FROM followers WHERE account = %s AND follower = %s
                   """, (account_id, user_id))
    follow = cur.fetchone()
    assert follow is None
    assert res is None


@then(parsers.parse('an error message is prompted "{error}"'))
def an_error_message_is_prompted(error, res):
    assert res == error
