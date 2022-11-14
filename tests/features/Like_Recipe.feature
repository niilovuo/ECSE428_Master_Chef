Feature: Like recipes

As a user of the Master Chef cooking website
I would like to like some recipes
So that I can change my preferences as I wish

Background:
  Given I am registered in the system

Scenario: Like a recipe (Normal Flow)
  Given I'm logged in to my account
  And I did not like a recipe before
  And this recipe exists in the system
  When I like this recipe
  Then the recipe joins my list of liked recipes

Scenario: Like a recipe which has been deleted (Error Flow)
  Given I'm logged in to my account
  And I did not like a recipe before
  And this recipe has been deleted
  When I try to like this recipe
  Then an error message is prompted "This recipe does not exist"

Scenario: Like a recipe without logging in (Error Flow)
  Given I haven't logged in to my account
  And I did not like a recipe before
  And this recipe exists in the system
  When I try to like this recipe
  Then an error message is prompted "Please log in first"