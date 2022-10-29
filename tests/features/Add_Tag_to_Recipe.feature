Feature: Add Tag to Recipe

As a recipe author
I would like to add tags to my recipe
So that users can find my recipe based the list of tags

  Background:

    Given no tags in the database
    And a user 1, "user1", "user1@gmail.com", "password1"
    And a user 2, "user2", "user2@gmail.com", "password2"
    And a recipe 1, "RecipeTitle" by user 1
    And a tag 1, "TagName"
    And a tag 2, "TagName1"
    And a tag 3, "TagName2"
    And a tag 4, "TagName3"

  Scenario: Add a tag to recipe without tags (Normal Flow)

    Given user 1 is logged into the system
    And there are no tags associated with recipe 1
    When requesting to add "TagName" tag to recipe 1
    Then the operation succeeds
    And the recipe 1 has tag "TagName"

  Scenario: Add multiple tags to recipe without tags (Alternate Flow)

    Given user 1 is logged into the system
    And there are no tags associated with recipe 1
    When requesting to add "TagName1" tag to recipe 1
    And requesting to add "TagName2" tag to recipe 1
    Then the operation succeeds
    And the recipe 1 has tag "TagName1"
    And the recipe 1 has tag "TagName2"

  Scenario: Attempt to add an already associated tag (Error Flow)

    Given user 1 is logged into the system
    And tag "TagName" is already associated with recipe 1
    When requesting to add "TagName" tag to recipe 1
    Then the operation fails with "Recipe already has tag"
    And the recipe 1 has tag "TagName"

  Scenario: Attempt to add a tag which does not exist (Error Flow)

    Given user 1 is logged into the system
    And tag "TagName" is already associated with recipe 1
    And tag "TagXXX" does not exist
    When requesting to add "TagXXX" tag to recipe 1
    Then the operation fails with "Tag does not exist"
    And the recipe 1 has tag "TagName"

  Scenario: Unauthorized user attempts to add a tag (Error Flow)

    Given user 2 is logged into the system
    And tag "TagName" is already associated with recipe 1
    When requesting to add "TagName1" tag to recipe 1
    Then the operation fails with "Cannot modify this recipe"
    And the recipe 1 has tag "TagName"

  Scenario: Logged out user attempts to add a tag (Error Flow)

    Given the user is not logged into the system
    When requesting to add "TagName" tag to recipe 1
    Then the user is redirected to the login page

