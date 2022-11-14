Feature: Unlike recipes

As a user of the Master Chef cooking website
I would like to unlike some recipes
So that I can change my preferences as I wish

Background:
  Given I am registered in the system

Scenario: Unlike a recipe (Normal Flow)
  Given I'm logged in to my account
  And I liked a recipe before
  And this recipe exists in the system
  When I unlike this recipe
  Then the recipe disappears from my list of liked recipes

Scenario: Unlike a recipe which has been deleted (Error Flow)
  Given I'm logged in to my account
  And I liked a recipe before
  And this recipe has been deleted
  When I try to unlike this recipe
  Then an error message is prompted "This recipe does not exist"
