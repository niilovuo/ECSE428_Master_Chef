"""Delete Comment feature tests."""


import pytest
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
    parsers
)

from project.db import CommentRepo
from project.comment import *


@scenario('features/Delete_Comment.feature', 'delete an existing comment (Normal Flow)')
def test_delete_an_existing_comment_normal_flow(app):
    pass


@scenario('features/Delete_Comment.feature', 'try to delete a comment which has already been deleted (Error Flow)')
def test_try_to_delete_a_comment_which_has_already_been_deleted_error_flow(app):
    pass


@scenario('features/Delete_Comment.feature', 'try to delete comments without logging in (Error Flow)')
def test_try_to_delete_comments_without_logging_in_error_flow(app):
    pass


@pytest.fixture
def a_user(postgresql):
    cur = postgresql.cursor()
    cur.execute("INSERT INTO accounts VALUES (1, 'owner', 'Dummy', 'Dummy', '') RETURNING id")
    user_id = cur.fetchone()[0]
    postgresql.commit()
    return user_id


@given(parsers.parse('the recipe "{title}" exists in the system'), target_fixture="recipe_id")
def the_recipe_name_exist_in_the_system(postgresql, a_user, title):
    cur = postgresql.cursor()
    cur.execute("""
        INSERT INTO recipes VALUES (DEFAULT, %s, NULL, NULL, 'go', %s, NULL)
        RETURNING id""", (title, a_user,))
    recipe_id = cur.fetchone()[0]
    postgresql.commit()
    return recipe_id


@given(parsers.parse('the user "{name}" exists in the system'), target_fixture='commenter_id')
def the_user_exist_in_the_system(postgresql, name):
    cur = postgresql.cursor()
    cur.execute("INSERT INTO accounts VALUES (2, %s, %s, %s, '') RETURNING id", (name, name, name))
    commenter_id = cur.fetchone()[0]
    postgresql.commit()
    return commenter_id


@given(parsers.parse('the recipe "{title}" has a comment authored by "{commenter}" with id "{recipe}"'))
def the_recipe_title_has_a_comment_authored_by_commenter_id_with_id(postgresql, title, commenter_id, recipe_id):
    _id = 123
    title = 'test'
    body = 'test'
    author = commenter_id
    recipe = recipe_id
    cur = postgresql.cursor()
    cur.execute("""
        INSERT INTO comments VALUES (%s, %s, %s, %s, %s)
        RETURNING id""", (_id, title, body, author, recipe))
    comment_id = cur.fetchone()[0]
    postgresql.commit()
    return comment_id


@given(parsers.parse('the comment with id "{comment_id}" has been deleted'))
def the_comment_with_id_has_been_deleted(comment_id, user_login, commenter_id):
    res = delete_comment_by_id(comment_id, user_login, commenter_id)
    assert res is None


@given('the user is not logged into the system', target_fixture='user_login')
def the_user_is_not_logged_into_the_system():
    return None


@given('"commenter" is logged into the system', target_fixture='user_login')
def user_is_logged_into_the_system(commenter_id):
    return commenter_id

@when(parsers.parse('attempting to delete comment "{comment_id}"'), target_fixture='res')
def attempting_to_delete_comment(comment_id, user_login, commenter_id):
    res = delete_comment_by_id(comment_id, user_login, commenter_id)
    return res


@then(parsers.parse('the comment with id "{comment_id}" does not exist'))
def the_comment_with_id_does_not_exist(comment_id):
    comment = search_comment_by_id(comment_id)
    assert comment is None


@then(parsers.parse('"{recipe}" has {count:d} comments'))
def has_0_comments(recipe_id, count):
    comments = search_comment_by_recipe_id(recipe_id)
    assert len(comments) == count


@then(parsers.parse('the "{error}" error message is issued'))
def the_error_message_is_issued(res, error):
    assert res == error
