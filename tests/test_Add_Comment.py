"""Add Comment feature tests."""

from flask import session
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
    parsers
)

@scenario('features/Add_Comment.feature', 'Add a comment to an existing recipe (Normal Flow)')
def test_add_comment_to_recipe(app):
    pass

@scenario('features/Add_Comment.feature', 'Add a blank comment (Error Flow)')
def test_add_blank_comment(app):
    pass

@scenario('features/Add_Comment.feature', 'Add a comment without logging in (Error Flow)')
def test_add_comment_no_login(app):
    pass

@given('there is at least one user registered')
def setup_user_1(postgresql):
    cur = postgresql.cursor()
    cur.execute("INSERT INTO accounts VALUES (1, 'User1', 'user1@mail.com', '1234555', '')")
    postgresql.commit()

@given(parsers.parse('the recipe id {recipe_id:d} exists in the system'))
def setup_recipe(recipe_id, postgresql):
    cur = postgresql.cursor()
    cur.execute("INSERT INTO recipes VALUES (%s, %s, NULL, NULL, '', 1, NULL)", (recipe_id, str(recipe_id)))
    postgresql.commit()

@given(parsers.parse('recipe id {recipe_id:d} has {count:d} comments'))
@then(parsers.parse('recipe id {recipe_id:d} has {count:d} comments'))
def check_number_of_comments(recipe_id, count, client):
    response = client.get(f"/api/recipes/{recipe_id}/comments")
    assert len(response.json) == count

@given('the user is logged into the system')
def log_me_in(client):
    with client.session_transaction() as session:
        session['id'] = 1

@given('the user is not logged into the system')
def dont_log_me_in(client):
    # this is the default
    pass

@when(parsers.re(r'attempting to add comment to recipe id (?P<recipe_id>\d+) with content "(?P<body>.*)"'),
      target_fixture='response')
def do_add_comment(recipe_id, body, client):
    # let's just add body as both the title and the body
    response = client.post("/api/comments/add", json={
        "comment_title": body,
        "comment_body": body,
        "recipe_id": recipe_id,
    })
    return response

@then(parsers.parse('the comment with content "{body}" is associated to the recipe id {recipe_id:d}'))
def check_comment(body, recipe_id, client):
    response = client.get(f"/api/recipes/{recipe_id}/comments")
    assert any((body in x for x in response.json))

@then(parsers.parse('the "{message}" error message is issued'))
def check_errmsg(message, response):
    assert response.status_code != 200
    assert response.data == bytes(message, 'utf-8')
