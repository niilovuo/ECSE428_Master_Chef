Feature: Delete Comment

  As a user
  I would like to delete some of my comments
  So that I can take back my careless, hurtful, and generally uncool words

  Background:
    Given the recipe "recipleTitle" exists in the system
    And the user "commenter" exists in the system
    And the recipe "recipeTitle" has a comment authored by "commenter" with id "123"

  Scenario: delete an existing comment (Normal Flow)
    Given "commenter" is logged into the system
    When attempting to delete comment "123"
    Then the comment with id "123" does not exist
    And "recipeTitle" has 0 comments

  Scenario: try to delete a comment which has already been deleted (Error Flow)
    Given "commenter" is logged into the system
    And the comment with id "123" has been deleted
    When attempting to delete comment "123"
    Then the "This comment does not exist" error message is issued
    And "recipeTitle" has 0 comments

  Scenario: try to delete comments without logging in (Error Flow)
    Given the user is not logged into the system
    When attempting to delete comment "123"
    Then the "Must be logged in to preform this action" error message is issued
    And "recipeTitle" has 1 comments