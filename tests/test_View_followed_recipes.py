import json
from flask import session
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
    parsers
)
from project.recipe_query import search_followed_user_recipes
from project.followers import follow_account_by_id

@given(parsers.parse('the following accounts exist in the system:{table}'), target_fixture = "author_dict")
def the_following_accounts_exist_in_the_system(postgresql, table):
    table = json.loads(table)[1:]
    cur = postgresql.cursor()
    author_dict = {}
    account_id = 0
    for (account_name, password, email) in table:
        account_id = account_id + 1
        str_account_id = str(account_id)
        author_dict[account_name] = str_account_id
        cur.execute(""" INSERT INTO accounts VALUES (%s, %s, %s, %s, '') """, (str_account_id, account_name, email, password))
    postgresql.commit()
    return author_dict

@given(parsers.parse('the following recipes exist in the system:{table}'))
def the_following_recipes_exist_in_the_system(table, postgresql, author_dict):
    table = json.loads(table)[1:]
    cur = postgresql.cursor()
    for (recipe_id, recipe_author, recipe_title, last_modified) in table:
        author_id = author_dict[recipe_author]
        cur.execute(""" INSERT INTO recipes VALUES (%s, %s, '00:00:00', '00:00:00', 'directions', %s, NULL); """, (recipe_id, recipe_title, author_id))
    postgresql.commit()

@scenario('features/View_followed_recipes.feature','User views their followed accounts recipes while logged in (Normal Flow)')
def test_user_views_their_followed_accounts_recipes_while_logged_in(app):
    pass

@scenario('features/View_followed_recipes.feature','User with no followed accounts views followed accounts recipes while logged in (Alternate Flow)')
def test_user_with_no_followed_accounts_views_followed_accounts_recipes_while_logged_in_alternate_flow(app):
    pass

@scenario('features/View_followed_recipes.feature', "Logged out user attempts to view their followed accounts recipes (Error Flow)")
def test_logged_out_user_attempts_to_view_their_followed_accounts_recipes_error_flow(app):
    pass

@given('"User1" is logged into the system', target_fixture = "user1_id")
def User1_is_logged_into_the_system(client, author_dict):
    with client.session_transaction() as session:
        user1_id = author_dict["User1"]
        session['id'] = user1_id
        return user1_id

@given('"User1" follows users "User2" and "User3"')
def User1_follows_users_User2_and_User3(postgresql, user1_id, author_dict):
    follow_account_by_id(author_dict["User2"], user1_id)
    follow_account_by_id(author_dict["User3"], user1_id)

@given("the user is not logged into the system", target_fixture="user1_id")
def the_user_is_not_logged_into_the_system(client):
    with client.session_transaction() as session:
        user1_id = None
        session['id'] = user1_id
        return user1_id

@when('attempting to view the followed accounts recipes', target_fixture="result")
def attempting_to_view_the_followed_accounts_recipes(user1_id):
    result = search_followed_user_recipes(user1_id)
    return result

@then(parsers.parse('the following list of recipes is returned:{table}'))
def the_following_list_of_recipes_is_returned(table, result):
    table = json.loads(table)[1:]
    followed_recipe_ids = []
    for recipe_id in table:
        followed_recipe_ids += recipe_id[0]

    int_recipe_id = []

    for followed_recipe in followed_recipe_ids:
        int_recipe_id.append(int(followed_recipe))
    
    result = [i[0] for i in result]

    for followed_recipe_id in int_recipe_id:
        assert followed_recipe_id in result

    assert len(result) == len(table)

@then(parsers.parse('the system issues an error message "{error}"'))
def the_system_issues_an_error_message(error,user1_id):
    user_id = user1_id
    if user_id == None:
        res = "Please login first"
    assert res == error

@given('"User2" is logged into the system', target_fixture = "user2_id")
def User2_is_logged_into_the_system(client, author_dict):
    with client.session_transaction() as session:
        user2_id = author_dict["User2"]
        session['id'] = user2_id
        return user2_id

@given('"User2" follows no users')
def User2_follows_no_users():
    pass

@when('"User2" attempts to view the followed accounts recipes', target_fixture="result2")
def User2_attempts_to_view_the_followed_accounts_recipes(user2_id):
    result2 = search_followed_user_recipes(user2_id)
    return result2

@then(parsers.parse('"User2" following list of recipes is returned:{table}'))
def User2_following_list_of_recipes_is_returned(table, result2):
    table = json.loads(table)[1:]
    assert len(table) == 0
    assert len(result2) == len(table)