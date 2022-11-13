"""Create new recipe feature tests."""

import json
import pytest
import datetime
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
    parsers
)
from project.recipe import *
from project.ingredient_query import *
from project.recipe_query import *


@scenario('features/Create_New_Recipe.feature', 'Logged in user attempts to create new recipe with a title that they have already created (Alternate Flow)')
def test_logged_in_user_attempts_to_create_new_recipe_with_a_title_that_they_have_already_created_alternate_flow(app):
    pass


@scenario('features/Create_New_Recipe.feature', 'Logged in user attempts to create new recipe with valid recipe information (Normal Flow)')
def test_logged_in_user_attempts_to_create_new_recipe_with_valid_recipe_information_normal_flow(app):
    pass


@scenario('features/Create_New_Recipe.feature', 'Logged out user attempts to create new recipe and with valid recipe information (Error flow)')
def test_logged_out_user_attempts_to_create_new_recipe_and_with_valid_recipe_information_error_flow(app):
    pass


@pytest.fixture
def user_session():
    return None

@pytest.fixture
def create_result():
    return None

@pytest.fixture
def create_partial_arguments():
    return None

@given('"User1" exists in the system')
def user1_exists_in_the_system(postgresql):
    cur = postgresql.cursor()
    cur.execute("INSERT INTO accounts VALUES (999, %s, %s, '', '');", ("User1", "User1"))
    postgresql.commit()

@given(parsers.parse('"User1" has created a recipe with the following information\n{table_data}'))
def user_has_created_a_recipe_with_the_following_information(postgresql, table_data):
    table_data = json.loads(table_data)[1:]
    cur = postgresql.cursor()
    for (id, title, prep_time, cook_time, directions) in table_data:
        cur.execute("INSERT INTO recipes VALUES (%s, %s, %s, %s, %s, %s, NULL);", (id, title, prep_time, cook_time, directions, 999))
    postgresql.commit()

@given(parsers.parse('the recipe with id "{recipe_id}" has the following ingredients\n{table_data}'))
def recipe_has_following_ingredients(postgresql, recipe_id, table_data):
    table_data = json.loads(table_data)[1:]
    cur = postgresql.cursor()
    for (name, quantity) in table_data:
        cur.execute("INSERT INTO ingredients VALUES (DEFAULT, %s, %s, %s);", (name, quantity, recipe_id))
    postgresql.commit()

@given('"User1" is logged into the system', target_fixture="user_session")
def log_in_user(postgresql):
    cur = postgresql.cursor()
    cur.execute("SELECT id FROM accounts WHERE name = 'User1';")
    return cur.fetchone()[0]

@given('User1 is not logged in', target_fixture="user_session")
def user_not_logged_in():
    return None



@when(parsers.parse('the following list of ingredients\n{table_data}'), target_fixture="create_result")
def the_following_list_of_ingredients(postgresql, create_partial_arguments, user_session, table_data):
    table_data = json.loads(table_data)[1:]
    for (i, e) in enumerate(table_data):
        create_partial_arguments['ingredients['+str(i)+'][name]'] = e[0]
        create_partial_arguments['ingredients['+str(i)+'][quantity]'] = e[1]
    try:
        id = create_recipe(create_partial_arguments, user_session)
        return ('ok', id)
    except Exception as e:
        return ('error', e)

@when(parsers.parse('trying to create a recipe with the following information\n{table_data}'), target_fixture="create_partial_arguments")
def trying_to_create_a_recipe_with_the_following_information(table_data):
    table_data = json.loads(table_data)[1]
    keys = ['title', 'prep_time', 'cook_time', 'directions']
    return dict(zip(keys, table_data))


@then('the "Please log in to create a recipe" error message will be issued')
def the_please_log_in_to_create_a_recipe_error_message_will_be_issued(create_result):
    assert create_result[0] == 'error'

@then(parsers.parse('the number of recipes associated with "User1" will be "{recipe_count}"'))
def the_number_of_recipes_associated_with_user1_will_be(postgresql, recipe_count):
    cur = postgresql.cursor()
    cur.execute("SELECT COUNT(*) FROM recipes WHERE author = 999;")
    count = cur.fetchone()[0]
    assert count == int(recipe_count)

@then(parsers.parse('the new recipe shall have "{ingredient_count}" ingredients'))
def check_recipe_ingredient_count(postgresql, create_result, ingredient_count):
    assert create_result[0] == 'ok'
    recipe_id = create_result[1]
    assert len(get_ingredients_of_recipe(recipe_id)) == int(ingredient_count)

    
@then(parsers.parse('the recipe with the following information exists\n{table_data}'))
def the_recipe_with_the_following_information_exists(create_result, table_data):
    table_data = json.loads(table_data)[1]
    keys = [1, 2, 3, 4]
    assert create_result[0] == 'ok'
    recipe_id = create_result[1]
    recipe = search_recipe_by_id(recipe_id)
    assert recipe is not None
    for (val, index) in zip(table_data, keys):
        fetched_val = recipe[index]
        if isinstance(fetched_val, datetime.time):
            fetched_val = fetched_val.strftime("%M:%S")
        assert fetched_val == val
