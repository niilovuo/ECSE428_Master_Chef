""" Add Tag to Recipe """

import json
from flask import session
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
    parsers
)

from project.db import TagRepo

@scenario('features/Add_Tag_to_Recipe.feature',
          'Add a tag to recipe without tags (Normal Flow)')
def test_add_a_tag(app):
    pass

@scenario('features/Add_Tag_to_Recipe.feature',
          'Add multiple tags to recipe without tags (Alternate Flow)')
def test_add_many_tags(app):
    pass

@scenario('features/Add_Tag_to_Recipe.feature',
          'Attempt to add an already associated tag (Error Flow)')
def test_add_duplicate_tag(app):
    pass

@scenario('features/Add_Tag_to_Recipe.feature',
          'Attempt to add a tag which does not exist (Error Flow)')
def test_add_inexistent_tag(app):
    pass

@scenario('features/Add_Tag_to_Recipe.feature',
          'Unauthorized user attempts to add a tag (Error Flow)')
def test_unauthorized_add_tag(app):
    pass

@scenario('features/Add_Tag_to_Recipe.feature',
          'Logged out user attempts to add a tag (Error Flow)')
def test_logged_out_user_attempts_to_add_a_tag(app):
    pass

@given('no tags in the database')
def clear_tags(postgresql):
    cur = postgresql.cursor()
    cur.execute("DELETE FROM tags")
    postgresql.commit()

@given(parsers.parse('a user {id:d}, "{name}", "{email}", "{password}"'))
def add_user(id, name, email, password, postgresql):
    cur = postgresql.cursor()
    cur.execute("""
        INSERT INTO accounts VALUES (%s, %s, %s, %s, '')
        """, (id, name, email, password))
    postgresql.commit()

@given(parsers.parse('a recipe {id:d}, "{title}" by user {author_id:d}'))
def add_recipe(id, title, author_id, postgresql):
    cur = postgresql.cursor()
    cur.execute("""
        INSERT INTO recipes VALUES (%s, %s, NULL, NULL, '', %s, NULL)
        """, (id, title, author_id))
    postgresql.commit()

@given(parsers.parse('a tag {id:d}, "{name}"'))
def add_tag(id, name, postgresql):
    cur = postgresql.cursor()
    cur.execute("""
        INSERT INTO tags VALUES (%s, %s)
        """, (id, name))
    postgresql.commit()

@given(parsers.parse('user {id:d} is logged into the system'))
def log_me_in(id, client):
    with client.session_transaction() as session:
        session['id'] = id

@given('the user is not logged into the system')
def skip_login():
    # no one is logged in by default
    pass

@given('there are no tags associated with recipe 1')
def check_no_tags_on_recipe():
    # this is the default
    pass

@given(parsers.parse('tag "{name}" is already associated with recipe {recipe_id:d}'))
def setup_recipe_tag(name, recipe_id, postgresql):
    cur = postgresql.cursor()
    cur.execute("""
        INSERT INTO recipe_tags VALUES (%s, %s)
        """, (recipe_id, TagRepo.select_by_name(name)[0]))
    postgresql.commit()

@given(parsers.parse('tag "{name}" does not exist'))
def check_tag_inexistent(name):
    assert TagRepo.select_by_name(name) is None

@when(parsers.parse('requesting to add "{tag}" tag to recipe {recipe_id:d}'),
      target_fixture='response')
def add_tag_to_recipe(tag, recipe_id, client):
    response = client.post(f"/recipes/{recipe_id}/tags",
                           data={ "tag": tag },
                           follow_redirects=True)
    return response

@then('the operation succeeds')
def check_op_succeeds():
    pass

@then(parsers.parse('the operation fails with "{errmsg}"'))
def check_error_message(errmsg, response):
    assert bytes(errmsg, 'utf-8') in response.data

@then(parsers.parse('the recipe {recipe_id:d} has tag "{name}"'))
def check_recipe_has_tag(recipe_id, name, client):
    response = client.get(f"/api/recipes/{recipe_id}/tags")
    assert response.status_code == 200

    found = False
    for (_, ld_name) in response.json:
        if name == ld_name:
            found = True
            break

    assert found

@then('the user is redirected to the login page')
def check_login_redirect(response):
    assert response.request.path == "/login"

