"""View Shopping List feature tests."""
import json

import pytest
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
    parsers
)
from flask import session
from project.db import IngredientRepo, ShoppingItemsRepo
from project.shopping_list import get_shopping_list_of_account



@scenario('features/View_Shopping_List.feature', 'View a shopping list containing entries while logged in (Normal Flow)')
def test_view_a_shopping_list_containing_entries_while_logged_in_normal_flow(app):
    pass


@scenario('features/View_Shopping_List.feature', 'View a shopping list containing no entries while logged in (Error Flow)')
def test_view_a_shopping_list_containing_no_entries_while_logged_in_error_flow(app):
    pass


@scenario('features/View_Shopping_List.feature', 'View a shopping list containing no entries while not logged in (Error Flow)')
def test_view_a_shopping_list_containing_no_entries_while_not_logged_in_error_flow(app):
    pass


@given(parsers.parse("user '{name}' is logged into the system"), target_fixture="user_id")
def user_name_is_logged_into_the_system(name, postgresql, client):
    cur = postgresql.cursor()
    cur.execute("""
        INSERT INTO accounts VALUES (DEFAULT, %s, '', '', '')
        RETURNING id""", (name,))
    user_id = cur.fetchone()[0]
    postgresql.commit()
    with client.session_transaction() as session:
        session['id'] = user_id
        return user_id


@given('the user is not logged into the system', target_fixture="user_id")
def the_user_is_not_logged_into_the_system(client):
    with client.session_transaction() as session:
        session['id'] = None
        return None


@given(parsers.parse("the following entries exist in the shopping list for user 'abc'\n{table}"))
def the_following_entries_exist_in_the_shopping_list_for_user_abc(postgresql, user_id, table):
    cur = postgresql.cursor()
    cur.execute("""
        INSERT INTO recipes VALUES (DEFAULT, 'go', NULL, NULL, 'go', %s, NULL)
        RETURNING id""", (user_id,))
    recipe_id = cur.fetchone()[0]
    postgresql.commit()
    table_data = json.loads(table)
    for _ in table_data[1:]:
        ingredient_id = IngredientRepo.insert_row(_[0], _[1], recipe_id)
        ShoppingItemsRepo.insert_row(user_id, ingredient_id)


@given("the no entries exist in the shopping list for user 'abc'")
def the_no_entries_exist_in_the_shopping_list_for_user_abc():
    pass


@when("user 'abc' requests to view their shopping list", target_fixture="res")
def user_user_name_requests_to_view_their_shopping_list(user_id):
    res = get_shopping_list_of_account(user_id)
    return res


@when("the user requests to view their shopping list", target_fixture="res")
def the_user_requests_to_view_their_shopping_list(user_id):
    res = get_shopping_list_of_account(user_id)
    return res


@then(parsers.parse("the system returns the following list\n{table}"))
def the_system_returns_the_following_list(res, table):
    table_data = json.loads(table)[1:]
    data = res[0]
    error = res[1]
    assert len(data) == len(table_data)
    assert error is None
    for (name, quantity) in data:
        assert [name, quantity] in table_data


@then(parsers.parse('the system issues a message "{error}"'))
def the_system_issues_a_message_error(res, error):
    assert res[1] == error
