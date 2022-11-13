"""Search recipes by tag tests."""

import json
import pytest
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
    parsers
)
from project.db import AccountRepo
from project.recipe_query import *
from project.tag_query import *

@scenario('features/Search_recipes_by_name.feature', 'Search a recipe by name (Normal Flow)')
def test_search_a_recipe_by_name(app):
    pass

@scenario('features/Search_recipes_by_name.feature', 'Search for a term matching multiple recipes (Alternate Flow)')
def test_search_for_a_term_matching_multiple_recipes(app):
    pass

@scenario('features/Search_recipes_by_name.feature', 'Search for recipes with invalid search parameter (Error Flow)')
def test_search_for_recipes_with_invalid_search_parameter(app):
    pass

@scenario('features/View_List_of_All_recipes.feature', 'User Requests List of Recipes (Normal Flow)')
def test_user_requests_list_of_recipes(app):
    pass

@scenario('features/View_List_of_All_recipes.feature', 'User Requests List of Recipes When There Are No Recipes (Alternative Flow)')
def test_user_requests_list_of_recipes_when_there_are_no_recipes(app):
    pass

@scenario('features/Search_recipes_by_tag.feature', 'Query all possible tags (Normal Flow)')
def test_query_all_possible_tags(app):
    pass

@scenario('features/Search_recipes_by_tag.feature', 'Filter recipes by tag (Normal Flow)')
def test_filter_recipe_by_tag(app):
    pass

@scenario('features/Search_recipes_by_tag.feature', 'Filter a recipe with multiple tags (Alternate Flow)')
def test_filter_a_recipe_with_multiple_tags(app):
    pass

@scenario('features/Search_recipes_by_tag.feature', 'Filter a recipe by tags and search for title (Alternate Flow)')
def test_filter_a_recipe_by_tags_and_search_for_title(app):
    pass

@scenario('features/Search_recipes_by_tag.feature', 'Filter a recipe with invalid tag (Error Flow)')
def test_filter_a_recipe_with_invalid_tag(app):
    pass

@scenario('features/Search_recipes_by_tag.feature', 'Filter a recipe with multiple tags, one of which is invalid (Error Flow)')
def test_filter_a_recipe_with_multiple_tags__one_of_which_is_invalid(app):
    pass

@given('no tags at all')
def clear_out_all_tags(postgresql):
    cur = postgresql.cursor()
    cur.execute("DELETE FROM tags;")
    postgresql.commit()

@given(parsers.parse('the following recipes exist in the system\n{table_data}'))
def the_following_recipes_exist_in_the_system(table_data, postgresql):
    table_data = json.loads(table_data)[1:]
    cur = postgresql.cursor()
    for (id, author, title, body) in table_data:
        cur.execute("""
            INSERT INTO accounts VALUES (DEFAULT, %s, %s, '', '')
            """, (author, author))
        cur.execute("""
            INSERT INTO recipes VALUES
            (DEFAULT, %s, NULL, NULL, %s, %s, NULL)
            """, (title, body, id))
    postgresql.commit()

@given(parsers.parse('the following tags exist in the system\n{table_data}'))
def the_following_tags_exist_in_the_system(table_data, postgresql):
    table_data = json.loads(table_data)[1:]
    cur = postgresql.cursor()
    for (_, name) in table_data:
        cur.execute("INSERT INTO tags VALUES (DEFAULT, %s)", (name,))
    postgresql.commit()

@given(parsers.parse('the following associations between recipes and tags exist in the system\n{table_data}'))
def the_following_associations_between_recipes_and_tags_exist_in_the_system(table_data, postgresql):
    table_data = json.loads(table_data)[1:]
    cur = postgresql.cursor()
    for (recipe, tag) in table_data:
        cur.execute("INSERT INTO recipe_tags VALUES (%s, %s)", (recipe, tag))
    postgresql.commit()

@pytest.fixture
def query_string():
    return ""

@pytest.fixture
def query_tags():
    return []

@given(parsers.parse('the query string "{query}"'), target_fixture='query_string')
def the_query_string(query):
    return query

@given(parsers.parse('the query tag "{tag}"'), target_fixture='query_tags')
def the_query_tag(tag, query_tags):
    return query_tags + [tag]

@when('the user requests the list of all possible tags', target_fixture='res')
def the_user_reqeusts_the_list_of_all_possible_tags():
    return get_all_tags()

@when('a user requests the list of recipes', target_fixture='res')
def a_user_requests_the_list_of_all_recipes(query_string, query_tags):
    return search_recipes_by_filter(query_string, query_tags, 0)

@then(parsers.parse('the system returns the following list of tags\n{table_data}'))
def the_system_returns_the_following_list_of_tags(table_data, res):
    table_data = json.loads(table_data)[1:]
    assert len(res) == len(table_data)
    for (id, name) in table_data:
        assert (id, name) in res

@then(parsers.parse('the following list of recipes is returned\n{table_data}'))
def the_following_list_of_recipes_is_returned(table_data, res):
    table_data = json.loads(table_data)[1:]
    assert res[1] is None

    res = res[0]
    assert len(res) == len(table_data)
    for (id, author, title, body) in table_data:
        assert (id, title, None, None, body, AccountRepo.select_by_name(author)[0], None, 0) in res

@then(parsers.parse('the "{errmsg}" error message is issued'))
def the__error_message_is_issued(errmsg, res):
    assert res[0] is None
    assert res[1] == errmsg

