Feature: Add ingredient to shopping list

  As a user of the Master Chef cooking website
  I would like to add an ingredient in a recipe to my shopping list
  So I can save the ingredients I need to buy

  Background:
    Given user "abc" with password "123" exists in the system
    And the recipe "stew" exists in the system
    And the recipe "stew" has the following ingredients
        [["Ingredient id", "Ingredient Name", "Quantity"],
        ["7", "leek", "200g"],
        ["8", "coriander", "20g"],
        ["9", "turnip", "2"],
        ["10", "condensed milk", "2 cups"]]


  Scenario: Logged in user adds ingredient (Normal Flow)
    Given user "abc" is logged into the system
    And the following entries exist in the shopping list for user "abc"
        [["Ingredient id", "Ingredient Name", "Quantity"],
        ["7", "leek", "200g"],
        ["8", "coriander", "20g"]]

    When attempting to add the ingredient with id "9"
    Then the user "abc" has the following ingredients in their shopping list
          [["Ingredient id", "Ingredient Name", "Quantity"],
          ["7", "leek", "200g"],
          ["8", "coriander", "20g"],
          ["9", "turnip", "2"]]


  Scenario: Attempt add duplicate ingredient to shopping list (Error Flow)
    Given user "abc" is logged into the system
    And the following entries exist in the shopping list for user "abc"
        [["Ingredient id", "Ingredient Name", "Quantity"],
        ["7", "leek", "200g"],
        ["8", "coriander", "20g"]]

    When attempting to add the ingredient with id "8"
    Then the user "abc" has the following ingredients in their shopping list
          [["Ingredient id", "Ingredient Name", "Quantity"],
          ["7", "leek", "200g"],
          ["8", "coriander", "20g"]]

    And the "Item could not be added" error message is issued

  Scenario: Attempt to add item while not logged in (Error Flow)
    Given the user is not logged into the system
    When attempting to add the ingredient with id "8"
    Then  the "Please login first" error message is issued
