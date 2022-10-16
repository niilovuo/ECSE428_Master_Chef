"""View List of All Recipes."""

import json
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
    parsers
)
from project.db import AccountRepo, RecipeRepo
from project.recipe_query import *


@scenario('features/View_List_of_All_recipes.feature', 'User Requests List of Recipes (Normal Flow)')
def test_user_requests_list_of_recipes(app):
    pass

@scenario('features/View_List_of_All_recipes.feature', 'User Requests List of Recipes When There Are No Recipes (Alternative Flow)')
def test_user_requests_list_of_recipes_when_there_are_no_recipes(app):
    pass

@given(parsers.parse('the following recipes exist in the system\n{table_data}'))
def the_following_recipes_exist_in_the_system(table_data, postgresql):
    table_data = json.loads(table_data)[1:]
    cur = postgresql.cursor()
    for (id, author, title, body) in table_data:
        cur.execute("""
            INSERT INTO accounts VALUES (DEFAULT, %s, %s, '')
            """, (author, author))
        cur.execute("""
            INSERT INTO recipes VALUES
            (DEFAULT, %s, NULL, NULL, %s, %s)
            """, (title, body, id))
    postgresql.commit()

@when(parsers.parse('a user requests the list of all recipes'),
      target_fixture='res')
def a_user_requests_the_list_of_all_recipes():
    return search_recipes_by_filter("", [], 0)

@then(parsers.parse('the following list of recipes is returned\n{table_data}'))
def the_following_list_of_recipes_is_returned(table_data, res):
    table_data = json.loads(table_data)[1:]
    assert res[1] is None

    res = res[0]
    assert len(res) == len(table_data)
    for (id, author, title, body) in table_data:
        assert (id, title, None, None, body, AccountRepo.select_by_name(author)[0]) in res

