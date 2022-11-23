"""Add ingredient to shopping list feature tests."""

import json
from project.account import *
from project.ingredient_query import *
from project.db import *
from project.shopping_list import get_shopping_list_of_account
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
    parsers
)


@scenario('features/Add_Ingredient_To_Shopping_List.feature',
          'Attempt add duplicate ingredient to shopping list (Error Flow)')
def test_attempt_add_duplicate_ingredient_to_shopping_list_error_flow():
    """Attempt add duplicate ingredient to shopping list (Error Flow)."""


@scenario('features/Add_Ingredient_To_Shopping_List.feature', 'Attempt to add item while not logged in (Error Flow)')
def test_attempt_to_add_item_while_not_logged_in_error_flow():
    """Attempt to add item while not logged in (Error Flow)."""


@scenario('features/Add_Ingredient_To_Shopping_List.feature', 'Logged in user adds ingredient (Normal Flow)')
def test_logged_in_user_adds_ingredient_normal_flow():
    """Logged in user adds ingredient (Normal Flow)."""


@given(parsers.parse('user "{username}" with password "{password}" exists in the system'))
def user_abc_with_password_123_exists_in_the_system(app, username, password):
    with app.app_context():
        if search_account_by_name(username):
            assert True
        else:
            res = db_save_account(username, "dummy@dummy.com", password)
            assert res[1] is None


@given(parsers.parse('the recipe "{recipe_title}" exists in the system'))
def the_recipe_stew_exists_in_the_system(app, recipe_title):
    with app.app_context():
        recipe_id = RecipeRepo.insert_recipe(recipe_title, 1, None, None, "", [])
        assert recipe_id is not None


@given(parsers.parse('the recipe "stew" has the following ingredients\n{table_data}'))
def the_recipe_stew_has_the_following_ingredients(postgresql, app, table_data):
    with app.app_context():
        table_data = json.loads(table_data)[1:]
        cur = postgresql.cursor()
        for (ingredient_id, name, quantity) in table_data:
            cur.execute("INSERT INTO ingredients VALUES (%s, %s, %s, %s);", (ingredient_id, name, quantity, 1))
        postgresql.commit()
        cur.close()

        ingredients = get_ingredients_of_recipe(1)
        assert len(ingredients) == len(table_data)


@given(parsers.parse('the following entries exist in the shopping list for user "{username}"\n{table_data}'))
def the_following_entries_exist_in_the_shopping_list_for_user_abc(app, postgresql, username, table_data):
    with app.app_context():
        user_id = search_account_by_name(username)[0]

        table_data = json.loads(table_data)[1:]
        cur = postgresql.cursor()
        for (ingredient_id, name, quantity) in table_data:
            cur.execute("INSERT INTO shopping_items VALUES (%s, %s);", (user_id, ingredient_id))
        postgresql.commit()
        cur.close()

        (shopping_list, err) = get_shopping_list_of_account(user_id)
        assert len(shopping_list) == len(table_data)


@given('the user is not logged into the system')
def the_user_is_not_logged_into_the_system(client):
    with client.session_transaction() as session:
        if "id" in session:
            client.get('/logout')
        assert not ("id" in session)


@given(parsers.parse('user "{name}" is logged into the system'))
def user_abc_is_logged_into_the_system(client, name):
    user = search_account_by_name(name)
    payload = {'email': user[2], 'password': 123}
    client.post('/login', data=payload)
    with client.session_transaction() as session:
        assert session["id"] == user[0]


@when(parsers.parse('attempting to add the ingredient with id "{ingredient_id}"'), target_fixture="response")
def attempting_to_add_the_ingredient_with_id(client, ingredient_id):
    return client.post(f'/api/shopping_list/add_ingredient/{ingredient_id}')


@then(parsers.parse('the user "{username}" has the following ingredients in their shopping list\n{table_data}'))
def the_user_abc_has_the_following_ingredients_in_their_shopping_list(app, username, table_data):
    with app.app_context():
        table_data = json.loads(table_data)[1:]
        user_id = search_account_by_name(username)[0]
        (shopping_list, err) = get_shopping_list_of_account(user_id)
        assert len(shopping_list) == len(table_data)


@then(parsers.parse('the "{message}" error message is issued'))
def the_error_message_is_issued(message, response):
    assert message in response.data.decode("utf-8")
