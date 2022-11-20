Feature: Like recipes

  As a user
  I would like to like some recipes
  So that I can change my preferences as I wish

  Background:
    Given I have registered in the system

  # Normal Flow
  Scenario: like a recipe
    Given I log in to my account
    And I did not liked a recipe before
    And this recipe exists in the system
    When I like this recipe
    Then the recipe join my list of liked recipes

  # Error Flow
  Scenario: like a recipe which has been deleted
    Given I log in to my account
    And I did not liked a recipe before
    And this recipe has been deleted
    When I like this recipe
    Then an error message is prompted "This recipe does not exist"

   # Error Flow
  Scenario: like a recipe without logging in
    Given I have not logged in to my account
    And I did not liked a recipe before
    And this recipe exists in the system
    When I like this recipe
    Then an error message is prompted "Please log in first"