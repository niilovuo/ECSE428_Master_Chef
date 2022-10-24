Feature: Filter recipes by tags

  As a user
  I would like to filter recipes by tags
  So that I can filter recipes that violate my dietary restrictions

  Background:
    Given the following recipes exist in the system
      [
        [ "recipe_id", "recipe_author", "recipe_title", "recipe_body" ],
        [ 1, "Someone Somewhere",  "Good recipe",    "This is a good recipe" ],
        [ 2, "Another Person",     "A recipe",       "This is a random recipe" ],
        [ 3, "Person Guy",         "Wow food",       "Insane recipe never seen before" ]
      ]

    And no tags at all
    And the following tags exist in the system
      [
        [ "tag_id", "tag_title" ],
        [ 1, "vegan" ],
        [ 2, "gluten-free" ],
        [ 3, "healthy" ]
      ]

    And the following associations between recipes and tags exist in the system
      [
        [ "recipe_id", "tag_id" ],
        [ 1, 1 ],
        [ 2, 3 ],
        [ 3, 1 ],
        [ 3, 2 ]
      ]


  Scenario: Query all possible tags (Normal Flow)
    When the user requests the list of all possible tags
    Then the system returns the following list of tags
      [
        [ "tag_id", "tag_title" ],
        [ 1, "vegan" ],
        [ 2, "gluten-free" ],
        [ 3, "healthy" ]
      ]

  Scenario: Filter recipes by tag (Normal Flow)
    Given the query tag "vegan"
    When a user requests the list of recipes
    Then the following list of recipes is returned
      [
        [ "recipe_id", "recipe_author", "recipe_title", "recipe_body" ],
        [ 1, "Someone Somewhere",  "Good recipe",    "This is a good recipe" ],
        [ 3, "Person Guy",         "Wow food",       "Insane recipe never seen before" ]
      ]

  Scenario: Filter a recipe with multiple tags (Alternate Flow)
    Given the query tag "vegan"
    And the query tag "gluten-free"
    When a user requests the list of recipes
    Then the following list of recipes is returned
      [
        [ "recipe_id", "recipe_author", "recipe_title", "recipe_body" ],
        [ 3, "Person Guy",         "Wow food",       "Insane recipe never seen before" ]
      ]

  Scenario: Filter a recipe by tags and search for title (Alternate Flow)
    Given the query string "recipe"
    And the query tag "vegan"
    When a user requests the list of recipes
    Then the following list of recipes is returned
      [
        [ "recipe_id", "recipe_author", "recipe_title", "recipe_body" ],
        [ 1, "Someone Somewhere",  "Good recipe",    "This is a good recipe" ]
      ]

  Scenario: Filter a recipe with invalid tag (Error Flow)
    Given the query tag "apoplexy-inducing"
    When a user requests the list of recipes
    Then the "This tag does not exist" error message is issued

  Scenario: Filter a recipe with multiple tags, one of which is invalid (Error Flow)
    Given the query tag "vegan"
    And the query tag "100% organic certified cortical homunculus meat"
    When a user requests the list of recipes
    Then the "This tag does not exist" error message is issued
