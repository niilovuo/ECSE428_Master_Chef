Feature: Add Comment

  As a user
  I would like to add comments to others' recipe
  So that I can discuss the recipe with the author

  Background:
    Given there is at least one user registered
    And the recipe id 1 exists in the system
    And recipe id 1 has 0 comments

  Scenario: Add a comment to an existing recipe (Normal Flow)
    Given the user is logged into the system
    When attempting to add comment to recipe id 1 with content "nice recipe"
    Then the comment with content "nice recipe" is associated to the recipe id 1
    And recipe id 1 has 1 comments

  Scenario: Add a blank comment (Error Flow)
    Given the user is logged into the system
    When attempting to add comment to recipe id 1 with content ""
    Then the "The comment title cannot be blank" error message is issued
    And recipe id 1 has 0 comments

  Scenario: Add a comment without logging in (Error Flow)
    Given the user is not logged into the system
    When attempting to add comment to recipe id 1 with content "nice recipe"
    Then the "You must log in to comment" error message is issued
    And recipe id 1 has 0 comments

