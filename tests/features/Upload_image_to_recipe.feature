Feature: Upload Image to Recipe

As a recipe author of the Master Chef cooking website
I would like to upload an image of the recipe
So that users can be visually appealed to the recipe

Scenario: Upload an image to a recipe with no images (Normal Flow)

    Given Recipe Author is logged into the system
    And "RecipeTitle" is a recipe which was authored by Recipe Author
    And there is 0 image associated with "RecipeTitle"
    When requesting to upload an image "Image1" to recipe "RecipeTitle"
    Then the system will remember recipe "RecipeTitle" as being associated with "Image1"

Scenario: Upload an image to a recipe with one image (Alternate Flow)

    Given Recipe Author is logged into the system
    And "RecipeTitle" is a recipe which was authored by Recipe Author
    And there is 1 image "Image1" associated with "RecipeTitle"
    When requesting to upload an image "Image2" to recipe "RecipeTitle"
    Then the system will remove the association between "Image1" and "RecipeTitle"
    And the system will remember recipe "RecipeTitle" as being associated with "Image2"

Scenario: Unauthorized user attempts to upload an image (Error Flow)

    Given Recipe Author is logged into the system
    And "RecipeTitle" is a recipe which was not authored by Recipe Author
    When requesting to upload an image "Image1" to recipe "RecipeTitle"
    Then the system will issue a "Invalid edit" error message

Scenario: Logged out user attempts to upload an image (Error Flow)

    Given Recipe Author is not logged into the system
    And "RecipeTitle" is a recipe which was authored by Recipe Author
    When requesting to upload an image "Image1" to recipe "RecipeTitle"
    Then the "Need to log in to modify this recipe" error message is issued
