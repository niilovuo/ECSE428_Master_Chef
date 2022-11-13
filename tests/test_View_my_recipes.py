""" View my recipes """

import json
from flask import session
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
    parsers
)

from project.db import AccountRepo

@scenario('features/View_my_recipes.feature',
          'Author views their recipes while logged in (Normal Flow)')
def test_author_views_their_recipes_while_logged_in(app):
    pass

@scenario('features/View_my_recipes.feature',
          'Logged out user attempts to view their recipes (Error Flow)')
def test_logged_out_user_attempts_to_view_their_recipes(app):
    pass

@given(parsers.parse('the following accounts exist in the system:{table}'))
def setup_accounts(table, postgresql):
    table = json.loads(table)[1:]
    cur = postgresql.cursor()
    for (id, name, password, email) in table:
        cur.execute("""
            INSERT INTO accounts VALUES (%s, %s, %s, %s, '')
            """, (id, name, email, password))
    postgresql.commit()

@given(parsers.parse('the following recipes exist in the system:{table}'))
def setup_recipes(table, postgresql):
    table = json.loads(table)[1:]
    cur = postgresql.cursor()
    for (id, author, title, _) in table:
        cur.execute("""
            INSERT INTO recipes VALUES (%s, %s, NULL, NULL, '', %s, NULL)
            """, (id, title, AccountRepo.select_by_name(author)[0]))
    postgresql.commit()

@given(parsers.parse('"{name}" is logged into the system'))
def log_me_in(name, client):
    with client.session_transaction() as session:
        session['id'] = AccountRepo.select_by_name(name)[0]

@given('the user is not logged into the system')
def skip_login():
    # no one is logged in by default
    pass

@when('attempting to view my recipes', target_fixture='response')
def load_my_recipes(client):
    response = client.get("/profile", follow_redirects=True)
    assert response.status_code == 200
    return response

@then(parsers.parse('the following list of recipes is returned:{table}'))
def check_recipes(table, response):
    table = json.loads(table)[1:]
    if table:
        for (id, _, _, _) in table:
            m = bytes(f'"id": {id}', 'utf-8')
            assert m in response.data
    else:
        assert b'"id": ' not in response.data

@then('the system asks to login')
def check_redirect_to_login(response):
    assert response.request.path == "/login"

