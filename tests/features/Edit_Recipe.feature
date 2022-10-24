Feature: 
As a recipe author
I want to be able to edit my existing recipes
So I can keep them up to date.

  Background: 
    Given "User1" exists in the system
    And "User1" has created a recipe with the following information [[ "Recipe ID", "Recipe Title", "Prep Time", "Cook Time", "Directions" ],[ "1", "Pancakes with butter", "3:00", "5:00", "mix with water" ]]

    And the recipe with id "1" has the following ingredients [[ "Ingredient Name", "Quantity" ],[ "eggs", "2" ],[ "butter", "1/4 tbsp" ],[ "wheat flow", "1/2 cup" ]]
  
  Scenario: Logged in user attempts to change recipe title
    Given "User1" is logged into the system
    When attempting to change recipe title of recipe "1" to "Pancakes with honey"
    Then new recipe title of recipe with id "1" shall be "Pancakes with honey"
  
  Scenario: Logged in user adds new ingredient to existing recipe
    Given "User1" is logged into the system
    When attempting to add Ingredient "honey" with quantity "1/4 tsp." to recipe "1"
    Then recipe "1" shall have "4" ingredients
  
  Scenario: Logged out user attempts to edit recipe
    Given the user is not logged into the system
    When attempting to add Ingredient "honey" with quantity "1/4 tsp." to recipe "1"
    Then recipe "1" shall have "3" ingredients
    And the "Need to log in to modify this recipe" error message is issued
  
  
