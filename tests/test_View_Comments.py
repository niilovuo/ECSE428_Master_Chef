"""View Comments feature tests."""
import json
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
    parsers
)


@given(parsers.parse('the following users exist in the system:{table}'))
def users_exist_in_the_system(table, postgresql):
    table = json.loads(table)[1:]
    cur = postgresql.cursor()
    for (id, name, email, password) in table:
        cur.execute("""
                        INSERT INTO accounts
                        VALUES (%s, %s, %s, %s, '')
                        """, (id, name, email, password))
    postgresql.commit()


@scenario('features/View_Comments.feature', 'User Requests List of Comments for a Recipe (Normal Flow)')
def test_user_requests_list_of_comments_for_a_recipe_normal_flow(app):
    pass


@scenario('features/View_Comments.feature',
          'User Requests List of Comments for a Recipe with No Comments (Alternative Flow)')
def test_user_requests_list_of_comments_for_a_recipe_with_no_comments_alternative_flow(app):
    pass


@scenario('features/View_Comments.feature',
          'User Requests List of Comments for a Recipe which does not exist (Error Flow)')
def test_user_requests_list_of_comments_for_a_recipe_which_does_not_exist_error_flow(app):
    pass


@given(parsers.parse('the following comments exist in the system:{table}'))
def setup_comments(table, postgresql):
    table = json.loads(table)[1:]
    cur = postgresql.cursor()
    for (comment_id, title, body, author_id, recipe_id) in table:
        cur.execute("""
                        INSERT INTO comments
                        VALUES (%s, %s, %s, %s, %s) RETURNING id
                        """, (comment_id, title, body, author_id, recipe_id))
    postgresql.commit()


@given('the recipe with id "1" exists in the system')
def the_recipe_with_id_1_exists_in_the_system(postgresql):
    cur = postgresql.cursor()
    cur.execute("""
        INSERT INTO recipes VALUES (%s, %s, NULL, NULL, 'go', %s, NULL)
        """, (1, "recipe", 1))
    postgresql.commit()


@given('the recipe with id "1" does not exist in the system')
def the_recipe_with_id_1_does_not_exist_in_the_system():
    pass  # No recipe by default


@when('a user requests the list of comments for recipe "1"', target_fixture='response')
def a_user_requests_the_list_of_comments_for_recipe_1(client):
    response = client.get("/api/recipes/1/comments")
    return response


@then(parsers.parse('the following list of comments is returned:{table}'))
def attempt_to_view_comments(table, response):
    table = json.loads(table)[1:]
    if table:
        for (comment_id, _, _, _, _) in table:
            m = bytes(f'[{comment_id},', 'utf-8')
            assert m in response.data
        assert response.status_code == 200
    else:
        assert len(response.json) == 0


@then('the "Invalid recipe id" error message is issued')
def the_invalid_recipe_id_error_message_is_issued(response):
    assert response.status_code == 404
    assert response.data == b"Invalid recipe id"
