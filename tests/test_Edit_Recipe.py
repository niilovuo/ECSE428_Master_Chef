"""Edit_Recipe.feature feature tests."""

import json
import pytest
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
    parsers
)
from project.recipe import *
from project.ingredient_query import *


@scenario('features/Edit_Recipe.feature', 'Logged in user adds new ingredient to existing recipe')
def test_logged_in_user_adds_new_ingredient_to_existing_recipe(app):
    pass

@scenario('features/Edit_Recipe.feature', 'Logged in user attempts to change recipe title')
def test_logged_in_user_attempts_to_change_recipe_title(app):
    pass

@scenario('features/Edit_Recipe.feature', 'Logged out user attempts to edit recipe')
def test_logged_out_user_attempts_to_edit_recipe(app):
    pass

@pytest.fixture
def user_session():
    return None

@pytest.fixture
def error_message():
    return None

@given('"User1" exists in the system')
def user_exists_in_the_system(postgresql):
    cur = postgresql.cursor()
    cur.execute("INSERT INTO accounts VALUES (999, %s, %s, '', '');", ("User1", "User1")) 

@given(parsers.parse('"User1" has created a recipe with the following information {table_data}'))
def user_has_created_a_recipe_with_the_following_information(postgresql, table_data):
    table_data = json.loads(table_data)[1:]
    cur = postgresql.cursor()
    for (id, title, prep_time, cook_time, directions) in table_data:
        cur.execute("INSERT INTO recipes VALUES (%s, %s, %s, %s, %s, %s, NULL);", (id, title, prep_time, cook_time, directions, 999))
    postgresql.commit()

@given(parsers.parse('the recipe with id "1" has the following ingredients {table_data}'))
def recipe_has_following_ingredients(postgresql, table_data):
    table_data = json.loads(table_data)[1:]
    cur = postgresql.cursor()
    for (name, quantity) in table_data:
        cur.execute("INSERT INTO ingredients VALUES (DEFAULT, %s, %s, %s);", (name, quantity, 1))
    postgresql.commit()

    
@given('"User1" is logged into the system', target_fixture="user_session")
def log_in_user(postgresql):
    cur = postgresql.cursor()
    cur.execute("SELECT id FROM accounts WHERE name = 'User1';")
    return cur.fetchone()[0]
    
@when('attempting to add Ingredient "honey" with quantity "1/4 tsp." to recipe "1"', target_fixture="error_msg")
def edit_recipe_ingredeients(user_session):
    data = {
        "title": "Pancakes",
        "ingredients[0][name]": "eggs",
        "ingredients[0][quantity]": "2",
        "ingredients[1][name]": "butter",
        "ingredients[1][quantity]": "1/4 tbsp",
        "ingredients[2][name]": "wheat flow",
        "ingredients[2][quantity]": "1/2 cup",
        "ingredients[3][name]": "honey",
        "ingredients[3][quantity]": "1/4 tsp."
    }
    try:
        edit_recipe(1, data, user_session)
        return None
    except Exception as e:
        return e
        
@then(parsers.parse('recipe "1" shall have "{ingredient_count}" ingredients'))
def check_recipe_ingredient_count(postgresql, ingredient_count):
    assert len(get_ingredients_of_recipe(1)) == int(ingredient_count)


@when('attempting to change recipe title of recipe "1" to "Pancakes with honey"', target_fixture="error_msg")
def edit_recipe_title(user_session):
    data = {"title": "Pancakes with honey"}
    try:
        edit_recipe(1, data, user_session)
        return None
    except Exception as e:
        return e
    
@then('new recipe title of recipe with id "1" shall be "Pancakes with honey"')
def check_new_title_value(postgresql):
    cur = postgresql.cursor()
    cur.execute("SELECT title FROM recipes WHERE id = %s;", (1,))
    assert cur.fetchone()[0] == "Pancakes with honey"

@given('the user is not logged into the system', target_fixture="user_session")
def user_not_logged_in():
    return None

@then('the "Need to log in to modify this recipe" error message is issued')
def check_error_message(error_message):
    error_message != None
