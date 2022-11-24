import json
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
    parsers
)
from project.ingredient_query import *
from project.recipe_query import *
from project.tag_query import *

@scenario('features/Query_recipe_info.feature', 'Search for tags')
def test_search_for_tags(app, postgresql):
    pass

@scenario('features/Query_recipe_info.feature', 'Search for ingredients')
def test_search_for_ingredients(app, postgresql):
    pass

@given('a user')
def a_user(postgresql):
    cur = postgresql.cursor()
    cur.execute("INSERT INTO accounts VALUES (DEFAULT, 'Dummy', 'Dummy', 'Dummy', '')")
    postgresql.commit()

@given('no tags at all')
def clear_out_all_tags(postgresql):
    cur = postgresql.cursor()
    cur.execute("DELETE FROM tags;")
    postgresql.commit()

@given(parsers.parse('a recipe named "{name}"'), target_fixture="recipe_id")
def a_recipe_named(name, postgresql):
    cur = postgresql.cursor()
    cur.execute("""
        INSERT INTO recipes VALUES (DEFAULT, %s, NULL, NULL, 'go', 1, NULL)
        RETURNING id""", (name,))
    recipe_id = cur.fetchone()[0]
    postgresql.commit()
    return recipe_id

@given(parsers.parse('with a tag named "{name}"'))
def with_a_tag_named(name, recipe_id, postgresql):
    cur = postgresql.cursor()
    cur.execute("INSERT INTO tags VALUES (DEFAULT, %s) RETURNING id", (name,))
    tag_id = cur.fetchone()[0]
    cur.execute("INSERT INTO recipe_tags VALUES (%s, %s)", (recipe_id, tag_id))
    postgresql.commit()

@given(parsers.parse('with an ingredient "{name}" of "{quant}"'))
def with_an_ingredient__of(name, quant, recipe_id, postgresql):
    cur = postgresql.cursor()
    cur.execute("""
        INSERT INTO ingredients VALUES (DEFAULT, %s, %s, %s)
        """, (name, quant, recipe_id))
    postgresql.commit()

@when(parsers.parse('I query ingredients of "{recipe}"'), target_fixture="res")
def i_query_ingredients_of(recipe):
    (recipes, _) = search_recipes_by_filter(recipe, [], 0)
    return get_ingredients_of_recipe(recipes[0][0])

@when(parsers.parse('I query tags of "{recipe}"'), target_fixture="res")
def i_query_tags_of(recipe):
    (recipes, _) = search_recipes_by_filter(recipe, [], 0)
    return get_tags_of_recipe(recipes[0][0])

@then(parsers.parse('I should have tags\n{tags}'))
def i_should_have_tags(tags, res):
    tags = json.loads(tags)
    assert len(res) == len(tags)

    for (_, tag) in res:
        assert tag in tags

@then(parsers.parse('I should have ingredients\n{ingredients}'))
def i_should_have_ingredients(ingredients, res):
    ingredients = json.loads(ingredients)
    assert len(res) == len(ingredients)

    for (_, name, quant, _, _) in res:
        assert [name, quant] in ingredients

