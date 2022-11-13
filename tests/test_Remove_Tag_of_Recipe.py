"""Delete tag pf recipe feature tests."""
from flask import session
import pytest
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
    parsers
)

from project.recipe import remove_tag_of_recipe
from project.db import RecipeTagRepo
from project.tag_query import get_tags_of_recipe, search_tag_by_name


@scenario('features/Remove_tag_from_recipe.feature', 'Remove a tag from recipe (Normal Flow)')
def test_remove_a_tag_from_recipe_normal_flow(app):
    pass


@scenario('features/Remove_tag_from_recipe.feature', 'Remove multiple tags from recipe (Alternate Flow)')
def test_remove_multiple_tags_from_recipe_alternate_flow(app):
    pass


@scenario('features/Remove_tag_from_recipe.feature', 'Attempt to remove a tag not associated with recipe (Error Flow)')
def test_remove_a_tag_not_associated_with_recipe_error_flow(app):
    pass


@scenario('features/Remove_tag_from_recipe.feature', 'Attempt to remove a tag which does not exist (Error Flow)')
def test_remove_a_tag_which_does_not_exist_error_flow(app):
    pass


@scenario('features/Remove_tag_from_recipe.feature', 'Unauthorized user attempts to remove a tag (Error Flow)')
def test_unauthorized_user_attempts_to_remove_a_tag_error_flow(app):
    pass


@scenario('features/Remove_tag_from_recipe.feature', 'Logged out user attempts to remove a tag (Error Flow)')
def test_logged_out_user_attempts_to_remove_a_tag_error_flow(app):
    pass


@given('no tags at all')
def clear_out_all_tags(postgresql):
    cur = postgresql.cursor()
    cur.execute("DELETE FROM tags;")
    postgresql.commit()


@pytest.fixture
def a_user(postgresql):
    cur = postgresql.cursor()
    cur.execute("INSERT INTO accounts VALUES (1, 'owner', 'Dummy', 'Dummy', '') RETURNING id")
    user_id = cur.fetchone()[0]
    postgresql.commit()
    return user_id


@given('Recipe Author is logged into the system', target_fixture="user_id")
def user_is_logged_into_the_system(client, a_user):
    with client.session_transaction() as session:
        session['id'] = a_user
        return a_user

@given('the user is not logged into the system', target_fixture="user_id")
def the_user_is_not_logged_into_the_system(client):
    with client.session_transaction() as session:
        session['id'] = None
        return None

@given(parsers.parse('"{title}" is a recipe which was authored by Recipe Author'), target_fixture="recipe_id")
def recipe_title_is_a_recipe_which_was_authored_by_author(title, a_user, postgresql):
    cur = postgresql.cursor()
    cur.execute("""
        INSERT INTO recipes VALUES (DEFAULT, %s, NULL, NULL, 'go', %s, NULL)
        RETURNING id""", (title, a_user,))
    recipe_id = cur.fetchone()[0]
    postgresql.commit()
    return recipe_id


@given(parsers.parse('"{title}" is a recipe which was not authored by Recipe Author'), target_fixture="recipe_id")
def recipe_title_is_a_recipe_which_was_not_authored_by_author(title, postgresql):
    cur = postgresql.cursor()
    cur.execute("INSERT INTO accounts VALUES (2, 'test1', 'test1', 'test1', '') RETURNING id")
    other_id = cur.fetchone()[0]
    postgresql.commit()
    cur.execute("""
        INSERT INTO recipes VALUES (DEFAULT, %s, NULL, NULL, 'go', %s, NULL)
        RETURNING id""", (title, other_id,))
    recipe_id = cur.fetchone()[0]
    postgresql.commit()
    return recipe_id


@given(parsers.parse('"{tag_name}" is a tag which exists in the system'), target_fixture="tag_id")
def tag_name_is_a_tag_which_exists_in_the_system(postgresql, tag_name):
    cur = postgresql.cursor()
    cur.execute("""
        INSERT INTO tags VALUES (DEFAULT, %s)
        RETURNING id""", (tag_name,))
    tag_id = cur.fetchone()[0]
    postgresql.commit()
    return tag_id


@given(parsers.parse('"{tag_name}" is a tag which does not exist in the system'), target_fixture="tag_id")
def tag_name_is_a_tag_which_does_not_exists_in_the_system(postgresql, tag_name, recipe_id):
    return None


@given(parsers.parse('{tag_name}" is associated with "{title}"'), target_fixture="is_associated")
def tag_name_is_associated_with_title(postgresql, tag_id, recipe_id):
    cur = postgresql.cursor()
    cur.execute("""
               INSERT INTO recipe_tags VALUES (%s, %s)
               """, (recipe_id, tag_id))
    postgresql.commit()
    return True


@given(parsers.parse('{tag_name}" is not associated with "{title}"'), target_fixture="is_associated")
def tag_name_is_not_associated_with_title(postgresql, recipe_id):
    return False


@given('there are 3 tags associated with "RecipeTitle"')
def there_are_3_tags_associated_with_title(recipe_id, postgresql, tag_id, is_associated):
    cur = postgresql.cursor()

    if isinstance(tag_id, int) and is_associated is True:
        cur.execute("""
            INSERT INTO tags VALUES (DEFAULT, 't2'), (DEFAULT, 't3')
            RETURNING id""")
        tag_id1, tag_id2 = cur.fetchall()
        cur.execute("""
                   INSERT INTO recipe_tags VALUES (%s, %s), (%s, %s)
                   """, (recipe_id, tag_id1[0], recipe_id, tag_id2[0]))
    elif isinstance(tag_id, list) and is_associated is True:
        cur.execute("""
            INSERT INTO tags VALUES (DEFAULT, 't3')
            RETURNING id""")
        tag_id = cur.fetchone()[0]
        cur.execute("""
            INSERT INTO recipe_tags VALUES (%s, %s)
            """, (recipe_id, tag_id))
    else:
        cur.execute("""
            INSERT INTO tags VALUES (DEFAULT, 't1'), (DEFAULT, 't2'), (DEFAULT, 't3')
            RETURNING id""")
        tag_id1, tag_id2, tag_id3 = cur.fetchall()
        cur.execute("""
            INSERT INTO recipe_tags VALUES (%s, %s), (%s, %s), (%s, %s)
            """, (recipe_id, tag_id1[0], recipe_id, tag_id2[0], recipe_id, tag_id3[0]))
    postgresql.commit()


@given(parsers.parse('"{tag_name1}" and "{tag_name2}" are tags which exist in the system'), target_fixture="tag_id")
def tag1_and_tag2_are_tags_which_exist_in_the_system(tag_name1, tag_name2, postgresql):
    cur = postgresql.cursor()
    cur.execute("""
        INSERT INTO tags VALUES (DEFAULT, %s)
        RETURNING id""", (tag_name1,))
    tag_id1 = cur.fetchone()[0]
    cur.execute("""
        INSERT INTO tags VALUES (DEFAULT, %s)
        RETURNING id""", (tag_name2,))
    tag_id2 = cur.fetchone()[0]
    postgresql.commit()
    return [tag_id1, tag_id2]


@given('"TagName1" and "TagName2" are associated with "RecipeTitle"', target_fixture="is_associated")
def tag1_and_tag2_are_associated_with_title(postgresql, recipe_id, tag_id):
    cur = postgresql.cursor()
    cur.execute("""
        INSERT INTO recipe_tags VALUES (%s, %s), (%s, %s)
        """, (recipe_id, tag_id[0], recipe_id, tag_id[1]))
    postgresql.commit()
    return True

@when(parsers.parse('requesting to remove "{tag_name}" from recipe "{title}"'), target_fixture='res')
def requesting_to_remove_tag_name_from_recipe_title(tag_name, recipe_id, user_id):
    res = remove_tag_of_recipe(tag_name, recipe_id, user_id)
    return res


@when(parsers.parse('requesting to remove "{tag_name1}" and "{tag_name2}" from recipe "RecipeTitle"'))
def requesting_to_remove_tag1_and_tag2_from_recipe_title(tag_name1, tag_name2, recipe_id, user_id):
    remove_tag_of_recipe(tag_name1, recipe_id, user_id)
    remove_tag_of_recipe(tag_name2, recipe_id, user_id)


@then(parsers.parse('the "RecipeTitle" will not have "{tag_name}" among its list of tags'))
def the_recipe_title_will_not_have_tag_name_among_its_list_of_tags(tag_name, recipe_id):
    tag = search_tag_by_name(tag_name)
    if not tag:
        res = False
    else:
        res = RecipeTagRepo.check_exists(recipe_id, tag[0])
    assert res is False


@then(parsers.parse('the "RecipeTitle" will have "{tag_name}" among its list of tags'))
def the_recipe_title_will_have_tag_name_among_its_list_of_tags(tag_name, recipe_id):
    tag = search_tag_by_name(tag_name)
    res = RecipeTagRepo.check_exists(recipe_id, tag[0])
    assert res is True

@then(parsers.parse('"RecipeTitle" is associated with {num:d} tags'))
def the_recipe_title_is_associated_with_num_tags(recipe_id, num):
    res = get_tags_of_recipe(recipe_id)
    assert len(res) == num


@then(parsers.parse('the "{error}" error message is issued'))
def the_error_message_is_issued(res, error):
    assert res == error
