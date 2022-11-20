"""Upload Image to Recipe feature tests."""

from flask import session
import io
from werkzeug.datastructures import FileStorage
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
)


@scenario('features/Upload_image_to_recipe.feature', 'Logged out user attempts to upload an image (Error Flow)')
def test_logged_out_user_attempts_to_upload_an_image_error_flow(app):
    """Logged out user attempts to upload an image (Error Flow)."""
    pass

@scenario('features/Upload_image_to_recipe.feature', 'Unauthorized user attempts to upload an image (Error Flow)')
def test_unauthorized_user_attempts_to_upload_an_image_error_flow(app):
    """Unauthorized user attempts to upload an image (Error Flow)."""
    pass

@scenario('features/Upload_image_to_recipe.feature', 'Upload an image to a recipe with no images (Normal Flow)')
def test_upload_an_image_to_a_recipe_with_no_images_normal_flow(app):
    """Upload an image to a recipe with no images (Normal Flow)."""
    pass

@scenario('features/Upload_image_to_recipe.feature', 'Upload an image to a recipe with one image (Alternate Flow)')
def test_upload_an_image_to_a_recipe_with_one_image_alternate_flow(app):
    """Upload an image to a recipe with one image (Alternate Flow)."""
    pass


@given('"RecipeTitle" is a recipe which was authored by Recipe Author')
def recipeTitleExists(postgresql):
    """"RecipeTitle" is a recipe which was authored by Recipe Author."""
    cur = postgresql.cursor()
    cur.execute("INSERT INTO accounts VALUES (1, 'RecipeAuthor', 'user1@mail.com', '1234555', '')")
    cur.execute("INSERT INTO recipes VALUES (1, 'RecipeTitle', NULL, NULL, '', 1, NULL)")
    postgresql.commit()


@given('"RecipeTitle" is a recipe which was not authored by Recipe Author')
def notRecipeAuthorRecipeExists(postgresql):
    """"RecipeTitle" is a recipe which was not authored by Recipe Author."""
    cur = postgresql.cursor()
    cur.execute("INSERT INTO accounts VALUES (1, 'RecipeAuthor', 'user1@mail.com', '1234555', '')")
    cur.execute("INSERT INTO accounts VALUES (2, 'NotRecipeAuthor', 'user2@mail.com', '1234555', '')")
    cur.execute("INSERT INTO recipes VALUES (1, 'RecipeTitle', NULL, NULL, '', 2, NULL)")
    postgresql.commit()


@given('Recipe Author is logged into the system')
def logMeIn(client):
    """Recipe Author is logged into the system."""
    with client.session_transaction() as session:
        session['id'] = 1


@given('Recipe Author is not logged into the system')
def notLoggedIn():
    """Recipe Author is not logged into the system."""
    pass  # default


@given('there is 0 image associated with "RecipeTitle"')
def noImageAssociatedWithRecipeTitle():
    """there is 0 image associated with "RecipeTitle"."""
    pass  # default


@given('there is 1 image "Image1" associated with "RecipeTitle"')
def imageAssociatedWithRecipeTitle(postgresql):
    """there is 1 image "Image1" associated with "RecipeTitle"."""
    cur = postgresql.cursor()
    cur.execute("UPDATE recipes SET image = %s WHERE id = %s;", ('img1_data', 1))
    postgresql.commit()


@when('requesting to upload an image "Image1" to recipe "RecipeTitle"', target_fixture='response')
def doAddImage1(client):
    """requesting to upload an image "Image1" to recipe "RecipeTitle"."""
    mock_file = FileStorage(
        stream=io.BytesIO(b'img1_data'),
        filename="Image1.png"
    )

    response = client.post("/api/recipes/1/images/add",
        data={
            "image": mock_file,
        },
        content_type='multipart/form-data'
    )
    return response


@when('requesting to upload an image "Image2" to recipe "RecipeTitle"', target_fixture='response')
def doAddImage2(client):
    """requesting to upload an image "Image2" to recipe "RecipeTitle"."""
    mock_file = FileStorage(
        stream=io.BytesIO(b'img2_data'),
        filename="Image2.png"
    )

    response = client.post("/api/recipes/1/images/add",
        data={
            "image": mock_file,
        },
        content_type='multipart/form-data'
    )
    return response


@then('the "Need to log in to modify this recipe" error message is issued')
def checkNeedToLoginMessage(response):
    """the "Need to log in to modify this recipe" error message is issued."""
    assert response.status_code != 200
    assert response.data == bytes("Need to log in to modify this recipe", 'utf-8')


@then('the system will issue a "Invalid edit" error message')
def checkInvalidEditMessage(response):
    """the system will issue a "Invalid edit" error message."""
    assert response.status_code != 200
    assert response.data == bytes("Invalid edit", 'utf-8')


@then('the system will remember recipe "RecipeTitle" as being associated with "Image1"')
def checkImage1associatedWithRecipe(response, postgresql):
    """the system will remember recipe "RecipeTitle" as being associated with "Image1"."""
    cur = postgresql.cursor()
    cur.execute("SELECT * FROM recipes WHERE id = %s", (1,))
    recipe = cur.fetchone()
    assert bytes(recipe[6]) == b'img1_data'


@then('the system will remember recipe "RecipeTitle" as being associated with "Image2"')
def checkImage2associatedWithRecipe(response, postgresql):
    """the system will remember recipe "RecipeTitle" as being associated with "Image2"."""
    cur = postgresql.cursor()
    cur.execute("SELECT * FROM recipes WHERE id = %s", (1,))
    recipe = cur.fetchone()
    assert bytes(recipe[6]) == b'img2_data'


@then('the system will remove the association between "Image1" and "RecipeTitle"')
def checkImage1removedFromRecipe(postgresql):
    """the system will remove the association between "Image1" and "RecipeTitle"."""
    cur = postgresql.cursor()
    cur.execute("SELECT * FROM recipes WHERE id = %s", (1,))
    recipe = cur.fetchone()
    assert bytes(recipe[6]) != b'img1_data'