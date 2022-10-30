Feature: Delete Recipe

As a recipe author
I would like to delete a Recipe
So that it is removed from the list of Recipes

Background:

    Given the following accounts exist in the system:
        | User   |
        | User1  |
        | User2  |
    And the recipe "Recipe1" exists in the system and belongs to "User1"
    And the recipe "Recipe2" exists in the system and belongs to "User2"

Scenario: A recipe author deletes a recipe they created (Normal Flow)
    Given "User1" is logged into the system
    When user1 attempting to delete "recipe1"
    Then "recipe1" does not exist in the system
    And "User1" has no associated recipes
    And the following recipes exist in the system:
        | Recipe  |
        | Recipe2 |
    And a "You have successfully deleted your recipe" message is issued


Scenario: Unauthorized user attempts to remove a recipe (Error Flow)
    Given "User2" is logged into the system
    When user2 attempting to delete "recipe1"
    Then the "Only the author of this recipe can modify the recipe" error message is issued
    And the following recipes exist in the system:
        | Recipe  |
        | Recipe1 |
        | Recipe2 |

Scenario: Logged out user attempts to remove a recipe (Error Flow)
    Given the user is not logged into the system
    When guest attempting to delete "recipe1"
    Then a "You need to log in to delete this recipe" error message is issued
    And the following recipes exist in the system:
        | Recipe  |
        | Recipe1 |
        | Recipe2 |


    
