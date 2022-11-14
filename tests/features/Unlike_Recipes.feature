Feature: Unlike recipes

  As a user of the Master Chef cooking website
  I would like to unlike some recipes
  So that I can change my preferences as I wish

  Background:
    Given a user exists in the system

  Scenario: Unlike a recipe (Normal Flow)
   Given a logged in user
   And a recipe that exists in the system
   And I have liked this recipe
   When attempting to unlike the recipe
   Then the recipe disappears from my list of liked recipes

  Scenario: Unlike a recipe which has been deleted (Error Flow)
    Given a user who is not logged in to their account
    And a recipe that does not exist in the system
    When attempting to unlike the recipe
    Then an error message is prompted "This recipe does not exist"
