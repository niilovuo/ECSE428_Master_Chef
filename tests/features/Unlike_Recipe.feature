Feature: Unlike recipes

  As a user
  I would like to unlike some recipes
  So that I can change my preferences as I wish

  Background:
    Given I have registered in the system

  # Normal Flow
  Scenario: unlike a recipe
    Given I log in to my account
    And I liked a recipe before
    And this recipe exists in the system
    When I unlike this recipe
    Then the recipe disappears from my list of liked recipes

  # Error Flow
  Scenario: unlike a recipe which has been deleted
    Given I log in to my account
    And I liked a recipe before
    And this recipe has been deleted
    When I unlike this recipe
    Then an error message is prompted "This recipe does not exist"

   # Error Flow
  Scenario: unlike a recipe without logging in
    Given I have not logged in to my account
    And I liked a recipe before
    And this recipe exists in the system
    When I unlike this recipe
    Then an error message is prompted "Please log in first"