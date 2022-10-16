Feature: Search recipes by name

As a user
I would like to search recipes by name
So that I can find the right recipe faster

Background:

Given the following recipes exist in the system
    [
        [ "recipe_id", "recipe_author", "recipe_title", "recipe_body" ],
        [ 1, "Someone Somewhere",  "Good recipe",    "This is a good recipe" ],
        [ 2, "Another Person",     "A recipe",       "This is a random recipe" ],
        [ 3, "Person Guy",         "Wow food",       "Insane recipe never seen before" ]
    ]

Scenario: Search a recipe by name (Normal Flow)

When searching for recipes with the query string "Good recipe"
Then the following list of recipes is returned
    [
        [ "recipe_id", "recipe_author", "recipe_title", "recipe_body" ],
        [ 1, "Someone Somewhere",  "Good recipe",    "This is a good recipe" ]
    ]

Scenario: Search for a term matching multiple recipes (Alternate Flow)

When searching for recipes with the query string "recipe"
Then the following list of recipes is returned
    [
        [ "recipe_id", "recipe_author", "recipe_title", "recipe_body" ],
        [ 1, "Someone Somewhere",  "Good recipe",    "This is a good recipe" ],
        [ 2, "Another Person",     "A recipe",       "This is a random recipe" ]
    ]


Scenario: Search for recipes with invalid search parameter (Error Flow)

When searching for recipes with the query string " "
Then the following list of recipes is returned
    [
        [ "recipe_id", "recipe_author", "recipe_title", "recipe_body" ]
    ]
