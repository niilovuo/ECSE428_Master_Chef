"""Search recipes by name tests."""

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


@scenario('features/Search_recipes_by_name.feature', 'Search a recipe by name (Normal Flow)')
def test_search_a_recipe_by_name(app):
    pass

@scenario('features/Search_recipes_by_name.feature', 'Search for a term matching multiple recipes (Alternate Flow)')
def test_search_for_a_term_matching_multiple_recipes(app):
    pass

@scenario('features/Search_recipes_by_name.feature', 'Search for recipes with invalid search parameter (Error Flow)')
def test_search_for_recipes_with_invalid_search_parameter(app):
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

@when(parsers.parse('searching for recipes with the query string "{query}"'),
      target_fixture='res')
def searching_for_recipes_with_the_query_string(query):
    return search_recipes_by_filter(query, [], 0)

@then(parsers.parse('the following list of recipes is returned\n{table_data}'))
def the_following_list_of_recipes_is_returned(table_data, res):
    table_data = json.loads(table_data)[1:]
    assert res[1] is None

    res = res[0]
    assert len(res) == len(table_data)
    for (id, author, title, body) in table_data:
        assert (id, title, None, None, body, AccountRepo.select_by_name(author)[0]) in res

