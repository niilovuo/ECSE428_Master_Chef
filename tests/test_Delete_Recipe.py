"""Delete Recipe feature tests."""


import pytest
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
    parsers
)

from project.db import RecipeRepo
from project.recipe import *

@scenario('features/Delete_Recipe.feature', 'A recipe author deletes a recipe they created (Normal Flow)')
def test_a_recipe_author_deletes_a_recipe_they_created_normal_flow(app):
    pass

@scenario('features/Delete_Recipe.feature', 'Unauthorized user attempts to remove a recipe (Error Flow)')
def test_unauthorized_user_attempts_to_remove_a_recipe_error_flow(app):
    pass

@scenario('features/Delete_Recipe.feature', 'Logged out user attempts to remove a recipe (Error Flow)')
def test_logged_out_user_attempts_to_remove_a_recipe_error_flow(app):
    pass

@given('the following accounts exist in the system')
def the_following_accounts_exists_in_the_system(postgresql):
    cur = postgresql.cursor()
    cur.execute("INSERT INTO accounts VALUES (1, %s, %s, '');", ("User", "User"))
    cur.execute("INSERT INTO accounts VALUES (2, %s, %s, '');", ("User1", "User1"))
    cur.execute("INSERT INTO accounts VALUES (3, %s, %s, '');", ("User2", "User2"))

@given('the recipe "Recipe1" exists in the system and belongs to "User1"')
def the_recipe_exists_in_the_system_and_belongs_to_user(postgresql):
    cur = postgresql.cursor()
    cur.execute("INSERT INTO recipes VALUES (%s, %s, %s, %s, %s, %s);", (1, "Recipe 1", "", "", "Recipe 1 directions", 1))
    cur.execute("INSERT INTO recipes VALUES (%s, %s, %s, %s, %s, %s);", (2, "Recipe 2", "", "", "Recipe 2 directions", 1))
    return None

@given('"User1" is logged into the system', target_fixture="user_session")
def user_is_logged_into_the_system(postgresql):
    cur = postgresql.cursor()
    cur.execute("SELECT id FROM accounts WHERE name = 'User1';")
    return cur.fetchone()[0]

@when('attempting to delete "recipe1"')
def attempt_to_delete_recipe():
    recipe_id = 1
    user_id = 1
    author_id = 1
    res = delete_recipe(recipe_id, user_id, author_id)
    return res

@then('"recipe1" does not exist in the system')
def recipe_does_not_exist_in_the_system():
    recipe_id = 1
    recipe = RecipeRepo.select_by_id(recipe_id)
    assert recipe is None

@then('"User1" has no associated recipes')
def user_has_no_associated_recipe():
    author_id = 1
    author_recipes = RecipeRepo.select_by_author(author_id)
    assert author_recipes is None


@then('the following recipes exist in the system')
def recipes_in_system(postgresql):
    cur = postgresql.cursor()
    cur.execute("SELECT * FROM recipes")

@given('"User2" is logged into the system')
def user_is_logged_into_the_system(postgresql):
    cur = postgresql.cursor()
    cur.execute("SELECT id FROM accounts WHERE name = 'User2';")
    return cur.fetchone()[0]

@when('attempting to delete "recipe1"')
def attempt_to_delete_recipe():
    recipe_id = 1
    user_id = 2
    author_id = 1
    res = delete_recipe(recipe_id, user_id, author_id)
    return res

@then('the "Only the author of this recipe can modify the recipe" error message is issued')
def only_recipe_author_can_modify():
    recipe_id = 1
    user_id = 2
    author_id = 1
    res = delete_recipe(recipe_id, user_id, author_id)
    assert res is "Only the author of this recipe can modify the recipe"

@then('the following recipes exist in the system')
def recipes_in_system(postgresql):
    cur = postgresql.cursor()
    cur.execute("SELECT * FROM recipes")

@given('the user is not logged into the system')
def user_is_not_logged_into_the_system():
    return None

@when('attempting to delete "recipe1"')
def not_logged_in_user_attempts_to_delete_recipe():
    recipe_id = 1
    author_id = 1
    user_id = None
    res = delete_recipe(recipe_id, user_id, author_id)
    return res

@then('a  "You need to log in to delete this recipe" error message is issued')
def error_issue():
    recipe_id = 1
    author_id = 1
    user_id = None
    res = delete_recipe(recipe_id, user_id, author_id)
    assert res is "You need to log in to delete this recipe"

@then('the following recipes exist in the system')
def recipes_in_system(postgresql):
    cur = postgresql.cursor()
    cur.execute("SELECT * FROM recipes")