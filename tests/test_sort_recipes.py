"""Sort recipe by number of likes feature tests."""

import json
import pytest

from pytest_bdd import (
    given,
    scenario,
    then,
    when,
    parsers
)

from project.recipe_query import *


@scenario('features/Sort_Recipe_By_Number_of_Likes.feature', 'Sort list of all recipes (Normal flow)')
def test_sort_list_of_all_recipes_normal_flow(app):
    pass


@scenario('features/Sort_Recipe_By_Number_of_Likes.feature', 'Sort list of recipes by title (Alternate flow)')
def test_sort_list_of_recipes_by_title_alternate_flow(app):
    pass


@scenario('features/Sort_Recipe_By_Number_of_Likes.feature', 'Sort list of tagged recipes (Alternate flow)')
def test_sort_list_of_tagged_recipes_alternate_flow(app):
    pass


@pytest.fixture
def recipe_results():
    return []


@pytest.fixture
def query_params():
    return {'title': "", 'tags': [], 'start': 0}


@given(parsers.parse('the following users exist in the system\n{table_data}'))
def the_following_users_exist_in_the_system(postgresql, table_data):
    """the following users exist in the system
    [
      ["user_id, user_name"],
      [380, "bob"],
      [381, "joe"],
      [382, "tom"],
      [383, "egg"],
      [384, "jon"],
      [385, "tim"]
    ]"""

    table_data=json.loads(table_data)[1:]
    cur=postgresql.cursor()
    for v in table_data:
        cur.execute("INSERT INTO accounts VALUES (%s, %s, %s, %s, '');",v+v)
    postgresql.commit()



@given(parsers.parse('the following recipes exist in the system\n{table_data}'))
def the_following_recipes_exist_in_the_system(postgresql, table_data):
    """the following recipes exist in the system
    [
      [ "recipe_id", "recipe_author", "recipe_title", "recipe_body" ],
      [ 1, 380, "Good recipe",    "This is a good recipe" ],
      [ 2, 381, "A recipe",       "This is a random recipe" ],
      [ 3, 382, "Wow food",       "Insane recipe never seen before" ]
    ]"""
    
    table_data=json.loads(table_data)[1:]
    cur=postgresql.cursor()
    for v in table_data:
        cur.execute("INSERT INTO recipes (id, author, title, directions) VALUES (%s, %s, %s, %s);",v)
    postgresql.commit()



@given(parsers.parse('the following tags exist in the system\n{table_data}'))
def the_following_tags_exist_in_the_system(postgresql, table_data):
    """the following tags exist in the system
    [
      ["tag_id", "tag_name"],
      [90, "vegan"]
    ]"""

    table_data=json.loads(table_data)[1:]
    cur=postgresql.cursor()
    for v in table_data:
        cur.execute("INSERT INTO tags (id, name) VALUES (%s, %s);",v)
    postgresql.commit()



@given(parsers.parse('the following associations between tags and recipes exist in the system\n{table_data}'))
def the_following_associations_between_tags_and_recipes_exist_in_the_system(postgresql, table_data):
    """the following associations between tags and recipes exist in the system
    [
      ["recipe_id", "tag_id"],
      [2, 90],
      [3, 90]
    ]"""
    
    table_data=json.loads(table_data)[1:]
    cur=postgresql.cursor()
    for v in table_data:
        cur.execute("INSERT INTO recipe_tags (recipe, tag) VALUES (%s, %s);",v)
    postgresql.commit()


    

@given(parsers.parse('the following users have liked the following recipes\n{table_data}'))
def the_following_users_have_liked_the_following_recipes(postgresql, table_data):
    """the following users have liked the following recipes
    [
      ["liker_id", "recipe_id"],
      [380, 1],
      [381, 1],
      [383, 2],
      [385, 2],
      [382, 2],
      [381, 2]
    ]"""

    table_data=json.loads(table_data)[1:]
    cur=postgresql.cursor()
    for v in table_data:
        cur.execute("INSERT INTO liked_recipes (liker, recipe) VALUES (%s, %s);",v)
    postgresql.commit()


@given(parsers.parse('the user has filtered based on the "{tag}" tag'), target_fixture="query_params")
def the_user_has_filtered_based_on_the_vegan_tag(tag, query_params):
    """the user has filtered based on the "vegan" tag."""

    return {**query_params, 'tags': [tag]}


@given(parsers.parse('the user has searced for the name "{search_param}"'), target_fixture="query_params")
def the_user_has_searced_for_the_name_recipe(search_param, query_params):
    """the user has searced for the name "recipe"."""


    return {**query_params, 'title': search_param}


@when('the user requests to view the recipes in order of descending number of likes', target_fixture="recipe_results")
def the_user_requests_to_view_the_recipes_in_order_of_descending_number_of_likes(query_params):
    """the user requests to view the recipes in order of descending number of likes."""

    return search_recipes_by_filter(**query_params)


@then(parsers.parse('the system returns the following list of recipe ids\n{table_data}'))
def the_system_returns_the_following_list_of_recipe_ids(table_data, recipe_results):
    """the system returns the following list of recipe ids
    [2, 1, 3]"""
    assert(recipe_results[1]==None)
    res=recipe_results[0]
    table_data=json.loads(table_data)
    assert(len(table_data)==len(res))
    for(recipe_id,recipe)in zip(table_data,res):
        assert(recipe[0]==recipe_id)
    
