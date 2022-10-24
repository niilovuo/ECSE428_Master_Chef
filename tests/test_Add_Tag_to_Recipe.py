"""
Feature: Add Tag to Recipe

As a recipe author
I would like to add tags to my recipe
So that users can find my recipe based the list of tags
"""

from flask import session

def background(postgresql):
    """
    Background:

    Given no tags in the database
    And a user 1, "user1", "user1@gmail.com", "password1"
    And a user 2, "user2", "user2@gmail.com", "password2"
    And a recipe 1, "RecipeTitle" by user 1
    And a tag 1, "TagName"
    And a tag 2, "TagName1"
    And a tag 3, "TagName2"
    And a tag 4, "TagName3"
    """

    cur = postgresql.cursor()
    cur.execute("""
        DELETE FROM tags;

        INSERT INTO accounts VALUES
        (1, 'User1', 'user1@gmail.com', 'password1'),
        (2, 'User2', 'user2@gmail.com', 'password2');

        INSERT INTO recipes VALUES
        (1, 'RecipeTitle', NULL, NULL, '', 1);

        INSERT INTO tags VALUES
        (1, 'TagName'),
        (2, 'TagName1'),
        (3, 'TagName2'),
        (4, 'TagName3');
        """)
    postgresql.commit()

def test_add_tag_to_recipe_without_tags(app, client, postgresql):
    """
    Scenario: Add a tag to recipe without tags (Normal Flow)

    Given user 1 is logged into the system
    And there are 0 tags associated with recipe 1
    When requesting to add "TagName" tag to recipe 1
    Then the operation succeeds
    And the tag "TagName" is added
    """

    background(postgresql)
    with client.session_transaction() as session:
        session['id'] = 1

    client.post("/recipes/1/tags", data={ "tag": "TagName" })
    response = client.get("/api/recipes/1/tags")
    assert response.status_code == 200
    assert response.json == [[1, "TagName"]]

def test_add_multiple_tags(app, client, postgresql):
    """
    Scenario: Add multiple tags to recipe without tags (Alternate Flow)

    Given user 1 is logged into the system
    And there are 0 tags associated with recipe 1
    When requesting to add "TagName1" tag to recipe 1
    And requesting to add "TagName2" tag to recipe 1
    Then the operation succeeds
    And the tag "TagName1" is added
    And the tag "TagName2" is added
    """

    background(postgresql)
    with client.session_transaction() as session:
        session['id'] = 1

    client.post("/recipes/1/tags", data={ "tag": "TagName1" })
    client.post("/recipes/1/tags", data={ "tag": "TagName2" })
    response = client.get("/api/recipes/1/tags")
    assert response.status_code == 200
    assert response.json == [[2, "TagName1"], [3, "TagName2"]]

def test_add_duplicate_tag(app, client, postgresql):
    """
    Scenario: Attempt to add an already associated tag (Error Flow)

    Given user 1 is logged into the system
    And tag "TagName" is already associated with recipe 1
    When requesting to add "TagName" tag to recipe 1
    Then the operation fails with "Recipe already has tag"
    And the tag "TagName" stays
    """

    background(postgresql)
    with client.session_transaction() as session:
        session['id'] = 1

    # the 2nd (duplicate) add should fail, we check if the flashed error
    # message is there
    client.post("/recipes/1/tags", data={ "tag": "TagName" })
    response = client.post("/recipes/1/tags", data={ "tag": "TagName" },
                           follow_redirects=True)
    assert response.request.path == "/recipes/1"
    assert b'Recipe already has tag' in response.data

    # check to make sure the old tag is still there
    response = client.get("/api/recipes/1/tags")
    assert response.status_code == 200
    assert response.json == [[1, "TagName"]]

def test_add_inexistent_tag(app, client, postgresql):
    """
    Scenario: Attempt to add a tag which does not exist (Error Flow)

    Given user 1 is logged into the system
    And tag "TagName" is already associated with recipe 1
    And tag "TagXXX" does not exist
    When requesting to add "TagXXX" tag to recipe 1
    Then the operation fails with "Tag does not exist"
    And the tag "TagName" stays
    """

    background(postgresql)
    with client.session_transaction() as session:
        session['id'] = 1

    # the 2nd add should fail, we check if the flashed error message is there
    client.post("/recipes/1/tags", data={ "tag": "TagName" })
    response = client.post("/recipes/1/tags", data={ "tag": "TagXXX" },
                           follow_redirects=True)
    assert response.request.path == "/recipes/1"
    assert b'Tag does not exist' in response.data

    # check to make sure the old tag is still there
    response = client.get("/api/recipes/1/tags")
    assert response.status_code == 200
    assert response.json == [[1, "TagName"]]

def test_unauthorized_add_tag(app, client, postgresql):
    """
    Scenario: Unauthorized user attempts to add a tag (Error Flow)

    Given user 2 is logged into the system
    And tag "TagName" is already associated with recipe 1
    When requesting to add "TagName1" tag to recipe 1
    Then the operation fails with "Cannot modify this recipe"
    And the tag "TagName" stays
    """

    background(postgresql)
    with client.session_transaction() as session:
        session['id'] = 1

    client.post("/recipes/1/tags", data={ "tag": "TagName" })

    with client.session_transaction() as session:
        session['id'] = 2

    response = client.post("/recipes/1/tags", data={ "tag": "TagName1" },
                           follow_redirects=True)
    assert response.request.path == "/recipes/1"
    assert b'Cannot modify this recipe' in response.data

    # check to make sure the old tag is still there
    response = client.get("/api/recipes/1/tags")
    assert response.status_code == 200
    assert response.json == [[1, "TagName"]]

def test_not_logged_in(app, client, postgresql):
    """
    Scenario: Logged out user attempts to add a tag (Error Flow)

    Given the user is not logged into the system
    When requesting to add "TagName" tag to recipe 1
    Then the user is redirected to the login page
    """

    background(postgresql)
    response = client.post("/recipes/1/tags", data={ "tag": "TagName" },
                           follow_redirects=True)
    assert response.request.path == "/login"

