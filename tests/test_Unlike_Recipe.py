"""Unlike Recipe feature tests."""

import pytest
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
    parsers
)

from project.likes import *;
from project.recipe import delete_recipe_by_id
from project.recipe_query import search_recipe_by_id


@given('I have registered in the system', target_fixture="user_id")
def i_have_registered_in_the_system(postgresql):
    cur = postgresql.cursor()
    cur.execute("INSERT INTO accounts VALUES (DEFAULT, 'owner', 'Dummy', 'Dummy', '') RETURNING id")
    user_id = cur.fetchone()[0]
    postgresql.commit()
    return user_id


@scenario('features/Unlike_Recipe.feature', 'unlike a recipe')
def test_unlike_a_recipe(app):
    pass

@scenario('features/Unlike_Recipe.feature', 'unlike a recipe which has been deleted')
def test_unlike_a_recipe_which_has_been_deleted(app):
    pass

@scenario('features/Unlike_Recipe.feature', 'unlike a recipe without logging in')
def test_unlike_a_recipe_without_logging_in(app):
    pass

@given('I log in to my account', target_fixture="user_id")
def i_log_in_to_my_account(user_id, client):
    with client.session_transaction() as session:
        session['id'] = user_id
        return user_id

@given('I liked a recipe before', target_fixture="recipe_id")
def i_liked_a_recipe_before(postgresql, user_id):
    cur = postgresql.cursor()
    if user_id is not None:
        cur.execute("INSERT INTO recipes VALUES (%s, %s, %s, %s, %s, %s, NULL);", (666, "Recipe 666", None, None, "Recipe 666 directions", user_id))
    else:
        cur.execute("INSERT INTO accounts VALUES (777, %s, %s, '', '');", ("User777", "User777"))
        cur.execute("INSERT INTO recipes VALUES (%s, %s, %s, %s, %s, %s, NULL);", (666, "Recipe 666", None, None, "Recipe 666 directions", 777))

    recipe_id = 666
    like_recipe(recipe_id, user_id)
    return recipe_id

@given('this recipe exists in the system')
def this_recipe_exist_in_the_system(recipe_id):
    recipe = search_recipe_by_id(recipe_id)
    assert recipe is not None

@when('I unlike this recipe', target_fixture="res")
def i_unlike_this_recipe(user_id, recipe_id):
    res = unlike_recipe(recipe_id, user_id)
    return res

@then('the recipe disappears from my list of liked recipes')
def the_recipe_disappears_from_my_list_of_liked_recipes(user_id, recipe_id):
    user_like = did_user_like(recipe_id, user_id)
    assert user_like is False

@given('this recipe has been deleted', target_fixture='res')
def this_recipe_has_been_deleted(recipe_id, user_id):
    res = delete_recipe_by_id(recipe_id, user_id, user_id)
    return res

@then('an error message is prompted "This recipe does not exist"')
def an_error_message_is_prompted_this_recipe_does_not_exist(res):
    assert res == "This recipe does not exist"

@given('I have not logged in to my account', target_fixture='user_id')
def i_have_not_logged_in_to_my_account(client):
    with client.session_transaction() as session:
        session['id'] = None
        return None

@then('an error message is prompted "Please log in first"')
def an_error_message_is_prompted_please_log_in_first(res):
    assert res == "Please log in first"

