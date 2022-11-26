Feature: View followed accounts' recipes

As a user of the Master Chef cooking website
I would like to view all the recipes of the people I follow
So that I can see all of the newest recipes from those people

Background:

  Given the following accounts exist in the system:
    [
      ["account_name", "password", "email"],
      ["User1", "password1", "user1@gmail.com"],
      ["User2", "password2", "user2@gmail.com"],
      ["User3", "password3", "user3@gmail.com"],
      ["User4", "password4", "user4@gmail.com"]
    ]
  And the following recipes exist in the system:
    [
      ["recipe_id", "recipe_author", "recipe_title", "last_modified"],
      ["1", "User1", "recipe title 1.1", "25/04/2020"],
      ["2", "User2", "recipe title 2", "12/08/2021"],
      ["3", "User1", "recipe title 1.2", "25/09/2022"],
      ["4", "User3", "recipe title 3", "2/10/2022"],
      ["5", "User4", "recipe title 4", "2/10/2022"]
    ]

Scenario: User views their followed accounts recipes while logged in (Normal Flow)

  Given "User1" is logged into the system
  And "User1" follows users "User2" and "User3"
  When attempting to view the followed accounts recipes
  Then the following list of recipes is returned:
    [ 
      ["recipe_id", "recipe_author", "recipe_title", "last_modified"],
      ["2", "User2", "recipe title 2", "12/08/2021"],
      ["4", "User3", "recipe title 3", "2/10/2022"]
    ]
    
Scenario: User with no followed accounts views followed accounts recipes while logged in (Alternate Flow)

  Given "User2" is logged into the system
  And "User2" follows no users
  When "User2" attempts to view the followed accounts recipes
  Then "User2" following list of recipes is returned:
    [ 
      ["recipe_id", "recipe_author", "recipe_title", "last_modified"]
    ]

Scenario: Logged out user attempts to view their followed accounts recipes (Error Flow)

  Given the user is not logged into the system
  When attempting to view the followed accounts recipes
  Then the system issues an error message "Please login first"
