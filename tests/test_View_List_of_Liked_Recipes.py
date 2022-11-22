"""View list of recipes feature tests."""
import json
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
    parsers
)
from project.likes import get_recipes_liked_by_liker

@scenario('features/View_List_of_Liked_Recipes.feature', 'User Requests views list of recipes they liked with deleted recipe while logged in (Error Flow)')
def test_user_requests_views_list_of_recipes_they_liked_with_deleted_recipe_while_logged_in_error_flow(app):
    pass

@scenario('features/View_List_of_Liked_Recipes.feature', 'User views the list of recipes they liked while logged in (Normal Flow)')
def test_user_views_the_list_of_recipes_they_liked_while_logged_in_normal_flow(app):
    pass

@scenario('features/View_List_of_Liked_Recipes.feature', 'User with no recipes liked views their list of recipes liked while logged in (Alternative Flow)')
def test_user_with_no_recipes_liked_views_their_list_of_recipes_liked_while_logged_in_alternative_flow(app):
    pass

@given('"CatChef" is logged into the system', target_fixture="user_id")
def catchef_is_logged_into_the_system(client):
    with client.session_transaction() as session:
        user_id = 2  # Cat Chef's user id = 2
        session['id'] = user_id
        return user_id

@given('"CatChef" likes the "Breakfast Eggs" recipe with recipe id "3"')
def catchef_likes_the_breakfast_eggs_recipe_with_recipe_id_3(postgresql, user_id):
    cur = postgresql.cursor()
    cur.execute("INSERT INTO liked_recipes (liker, recipe) VALUES (%s, %s) RETURNING liker",
                (user_id, 3))
    postgresql.commit()

@given('"CatChef" likes the "Fluffy Cheese Cake" recipe with recipe id "1"')
def catchef_likes_the_fluffy_cheese_cake_recipe_with_recipe_id_1(postgresql, user_id):
    cur = postgresql.cursor()
    cur.execute("INSERT INTO liked_recipes (liker, recipe) VALUES (%s, %s) RETURNING liker",
                (user_id, 1))
    postgresql.commit()

@given('"CatChef" likes the "Macaroni and Cheese" recipe with recipe id "2"')
def catchef_likes_the_macaroni_and_cheese_recipe_with_recipe_id_2(postgresql, user_id):
    cur = postgresql.cursor()
    cur.execute("INSERT INTO liked_recipes (liker, recipe) VALUES (%s, %s) RETURNING liker",
                (user_id, 2))
    postgresql.commit()

@given('did not like any recipes')
def did_not_like_any_recipes():
    pass  # No recipes liked by default

@given('the author deleted recipe id "1"')
def the_author_deleted_recipe_id_1(postgresql):
    cur = postgresql.cursor()
    cur.execute("DELETE FROM recipes WHERE id = 1")
    postgresql.commit()

@given(parsers.parse('the following accounts exist in the system:{table}'))
def the_following_accounts_exist_in_the_system(table, postgresql):
    table = json.loads(table)[1:]
    cur = postgresql.cursor()
    for (account_id, account_name, email, password) in table:
        cur.execute("""
                        INSERT INTO accounts
                        VALUES (%s, %s, %s, %s, '')
                        """, (account_id, account_name, email, password))
    postgresql.commit()

@given(parsers.parse('the following recipes exist in the system:{table}'))
def the_following_recipes_exist_in_the_system(table, postgresql):
    table = json.loads(table)[1:]
    cur = postgresql.cursor()
    for (recipe_id, recipe_title, prep_time, cook_time, directions, author_id) in table:
        cur.execute("""
                        INSERT INTO recipes
                        VALUES (%s, %s, %s, %s, %s, %s, NULL);
                        """, (recipe_id, recipe_title, prep_time, cook_time, directions, author_id))
    postgresql.commit()

@when('attempting to view the list of recipes they liked', target_fixture="res")
@when('"CatChef" attempts to view the list of recipes they liked', target_fixture="res")
def catchef_attempts_to_view_the_list_of_recipes_they_liked(user_id):
    res = get_recipes_liked_by_liker(user_id)
    return res

@then(parsers.parse('the following list of recipes liked ids is returned:{table}'))
def the_following_list_of_recipes_liked_ids_is_returned(table, res):
    table = json.loads(table)[1:]
    table = [tuple(e) for e in table]  # convert into list of tuples to compare with res
    for recipe_id in table:
        assert recipe_id in res
    assert len(res) == len(table)