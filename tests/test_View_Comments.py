"""View Comments feature tests."""
import json
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
)

from project.comment import search_comment_by_recipe_id
@scenario('features/View_Comments.feature', 'User Requests List of Comments for a Recipe (Normal Flow)')
def test_user_requests_list_of_comments_for_a_recipe_normal_flow():
    pass


@scenario('features/View_Comments.feature', 'User Requests List of Comments for a Recipe with No Comments (Alternative Flow)')
def test_user_requests_list_of_comments_for_a_recipe_with_no_comments_alternative_flow():
    pass

@given('the following comments exist in the system:{table}')
def setup_comments(table, postgresql):
    table = json.loads(table)[1:]
    cur = postgresql.cursor()
    for (comment_id, title, body, author_id, recipe_id ) in table:
        cur.execute("""
                        INSERT INTO comments
                        VALUES (%s, %s, %s, %s, %s) RETURNING id
                        """, (comment_id, title, body, author_id, recipe_id))
    postgresql.commit()

@given('the recipe with id "1" exists in the system')
def the_recipe_with_id_1_exists_in_the_system(postgresql):
    cur = postgresql.cursor()
    cur.execute("""
        INSERT INTO recipes VALUES (%s, %s, NULL, NULL, 'go', %s)
        """, (1, "recipe", 1))
    postgresql.commit()

@when('a user requests the list of comments for recipe "{1}"', target_fixture='response')
def a_user_requests_the_list_of_comments_for_recipe_1():
    """a user requests the list of comments for recipe "1"."""
    response = search_comment_by_recipe_id(1)
    return response

@then('the following list of comments is returned:{table}')
def attempt_to_view_comments(table, response):
    table = json.loads(table)[1:]
    if table:
        for (comment_id, _, _, _, _) in table:
            m = bytes(f'"comment_id": {comment_id}', 'utf-8')
            assert m in response.data
    else:
        assert b'"comment_id": ' not in response.data
