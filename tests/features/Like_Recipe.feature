Feature: Like recipes

  As a user of the Master Chef cooking website
  I would like to like some recipes
  So that I can change my preferences as I wish

  Background:
    Given a user exists in the system

  Scenario: Like a recipe (Normal Flow)
    Given a logged in user
    And a recipe that exists in the system
    When attempting to like this recipe
    Then the recipe joins my list of liked recipes

  Scenario: Like a recipe which has been deleted (Error Flow)
    Given a logged in user
    And a recipe that does not exist in the system
    When attempting to like this recipe
    Then an error message is prompted "This recipe does not exist"

  Scenario: Like a recipe without logging in (Error Flow)
    Given a user who is not logged in to their account
    And a recipe that exists in the system
    When attempting to like this recipe
    Then an error message is prompted "Please log in first"
