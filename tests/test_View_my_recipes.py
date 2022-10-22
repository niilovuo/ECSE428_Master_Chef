"""
Feature: View my recipes

As a recipe author
I would like to view all the recipes I wrote
So that I can easily choose one of my recipes to view, edit or delete it.
"""

from flask import session

def background(postgresql):
    """
    Given the following accounts exist in the system:
     | account name | password  | email           |
     | User1        | password1 | user1@gmail.com |
     | User2        | password2 | user2@gmail.com |
     | User3        | password3 | user3@gmail.com |
     | User4        | password4 | user4@gmail.com |
    And the following recipes exist in the system:
     | recipe id | recipe author | recipe title     | last modified |
     | 1         | User1         | recipe title 1.1 | 25/04/2020    |
     | 2         | User2         | recipe title 2   | 12/08/2021    |
     | 3         | User1         | recipe title 1.2 | 25/09/2022    |
     | 4         | User3         | recipe title 3   | 2/10/2022     |
    """

    cur = postgresql.cursor()
    cur.execute("""
        INSERT INTO accounts VALUES
        (DEFAULT, 'User1', 'user1@gmail.com', 'password1'),
        (DEFAULT, 'User2', 'user2@gmail.com', 'password2'),
        (DEFAULT, 'User3', 'user3@gmail.com', 'password3'),
        (DEFAULT, 'User4', 'user4@gmail.com', 'password4');

        INSERT INTO recipes VALUES
        (1, 'recipe title 1.1', NULL, NULL, '', 1),
        (2, 'recipe title 2', NULL, NULL, '', 2),
        (3, 'recipe title 1.2', NULL, NULL, '', 1),
        (4, 'recipe title 3', NULL, NULL, '', 3);
        """)
    postgresql.commit()


def test_scenario_logged_in_has_recipe(app, client, postgresql):
    """
    Scenario: Author views their recipes while logged in (Normal Flow)

    Given "User1" is logged into the system
    When attempting to view my recipes
    Then the following list of recipes is returned:
     | recipe id | recipe author | recipe title     | last modified |
     | 1         | User1         | recipe title 1.1 | 25/04/2020    |
     | 3         | User1         | recipe title 1.2 | 25/09/2022    |
    """

    background(postgresql)
    with client.session_transaction() as session:
        session['username'] = "User1"

    response = client.get("/profile")
    assert response.status_code == 200
    assert b'"id": 1' in response.data
    assert b'"id": 3' in response.data

def test_scenario_logged_in_no_recipes(app, client, postgresql):
    """
    Scenario: User with no recipes written views their recipes while logged in (Alternate Flow)

    Given "User 4" is logged into the system
    When attempting to view my recipes
    Then the following list of recipes is returned:
     | recipe id | recipe author | recipe title     | last modified |
    And a "You don't have any recipes" info message is issued
    """

    background(postgresql)
    with client.session_transaction() as session:
        session['username'] = "User4"

    response = client.get("/profile")
    assert response.status_code == 200
    assert b'"id": ' not in response.data

def test_scenario_not_logged_in(app, client, postgresql):
    """
    Scenario: Logged out user attempts to view their recipes (Error Flow)

    Given the user is not logged into the system
    When attempting to view my recipes
    Then the system issues an error message "Please log in to view your recipes"
    """

    background(postgresql)

    # we redirect them back to login
    response = client.get("/profile", follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/login"
