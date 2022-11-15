Feature: Sort recipe by number of likes

  As a user of the Master Chef cooking website
  I would like to sort the list of recipies by number of likes
  So I can view the most critically acclaimed recipes on top

  Background:
    Given the following users exist in the system
        [
            ["user_id, user_name"],
            [380, "bob"],
            [381, "joe"],
            [382, "tom"],
            [383, "egg"],
            [384, "jon"],
            [385, "tim"]
        ]
        
    And the following recipes exist in the system
        [
            [ "recipe_id", "recipe_author", "recipe_title", "recipe_body" ],
            [ 1, 380, "Good recipe",    "This is a good recipe" ],
            [ 2, 381, "A recipe",       "This is a random recipe" ],
            [ 3, 382, "Wow food",       "Insane recipe never seen before" ]
        ]
      
    And the following tags exist in the system
        [
            ["tag_id", "tag_name"],
            [90, "marginally edible"]
        ]
       
    And the following associations between tags and recipes exist in the system
        [
            ["recipe_id", "tag_id"],
            [2, 90],
            [3, 90]
        ]
        
    And the following users have liked the following recipes
        [
            ["liker_id", "recipe_id"],
            [380, 1],
            [381, 1],
            [383, 2],
            [385, 2],
            [382, 2],
            [381, 2]
        ]
            
  Scenario: Sort list of all recipes (Normal flow)
    
    When the user requests to view the recipes in order of descending number of likes
    Then the system returns the following list of recipe ids
        [2, 1, 3]
  Scenario: Sort list of tagged recipes (Alternate flow)

    Given the user has filtered based on the "marginally edible" tag
    When the user requests to view the recipes in order of descending number of likes
    Then the system returns the following list of recipe ids
        [2, 3]

  Scenario: Sort list of recipes by title (Alternate flow)

    Given the user has searced for the name "recipe"
    When the user requests to view the recipes in order of descending number of likes
    Then the system returns the following list of recipe ids
        [2, 1]
