Feature: View my recipes

As a recipe author
I would like to view all the recipes I wrote
So that I can easily choose one of my recipes to view, edit or delete it.

  Background:
    Given the following accounts exist in the system:
      [
       [ "id", "account name", "password", "email" ],
       [ 1, "User1",        "password1", "user1@gmail.com" ],
       [ 2, "User2",        "password2", "user2@gmail.com" ],
       [ 3, "User3",        "password3", "user3@gmail.com" ],
       [ 4, "User4",        "password4", "user4@gmail.com" ]
      ]
    And the following recipes exist in the system:
      [
        [ "recipe id", "recipe author", "recipe title", "last modified" ],
        [ 1         , "User1"         , "recipe title 1.1" , "25/04/2020" ],
        [ 2         , "User2"         , "recipe title 2"   , "12/08/2021" ],
        [ 3         , "User1"         , "recipe title 1.2" , "25/09/2022" ],
        [ 4         , "User3"         , "recipe title 3"   , "2/10/2022" ]
      ]

  Scenario: Author views their recipes while logged in (Normal Flow)

    Given "User1" is logged into the system
    When attempting to view my recipes
    Then the following list of recipes is returned:
      [
        [ "recipe id", "recipe author", "recipe title", "last modified" ],
        [ 1         , "User1"         , "recipe title 1.1" , "25/04/2020" ],
        [ 3         , "User1"         , "recipe title 1.2" , "25/09/2022" ]
      ]

  Scenario: User with no recipes written views their recipes while logged in (Alternate Flow)

    Given "User 4" is logged into the system
    When attempting to view my recipes
    Then the following list of recipes is returned:
      [ [ "recipe id", "recipe author", "recipe title", "last modified" ] ]

  Scenario: Logged out user attempts to view their recipes (Error Flow)

    Given the user is not logged into the system
    When attempting to view my recipes
    Then the system asks to login

