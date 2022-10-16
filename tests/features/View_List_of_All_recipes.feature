Feature: View List of All Recipes

As a user
I would like to view a list of all recipes
So that I read ones that interest me

Scenario: User Requests List of Recipes (Normal Flow)

Given the following recipes exist in the system
    [
        [ "recipe_id", "recipe_author", "recipe_title", "recipe_body" ],
        [ 1, "Someone Somewhere",  "Good recipe",    "This is a good recipe" ],
        [ 2, "Another Person",     "A recipe",       "This is a random recipe" ],
        [ 3, "Person Guy",         "Wow food",       "Insane recipe never seen before" ]
    ]

When a user requests the list of recipes
Then the following list of recipes is returned
    [
        [ "recipe_id", "recipe_author", "recipe_title", "recipe_body" ],
        [ 1, "Someone Somewhere",  "Good recipe",    "This is a good recipe" ],
        [ 2, "Another Person",     "A recipe",       "This is a random recipe" ],
        [ 3, "Person Guy",         "Wow food",       "Insane recipe never seen before" ]
    ]

Scenario: User Requests List of Recipes When There Are No Recipes (Alternative Flow)

Given the following recipes exist in the system
    [
        [ "recipe_id", "recipe_author", "recipe_title", "recipe_body" ]
    ]

When a user requests the list of recipes
Then the following list of recipes is returned
    [
        [ "recipe_id", "recipe_author", "recipe_title", "recipe_body" ]
    ]
