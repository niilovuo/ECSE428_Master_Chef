Feature: Follow Account

  As a user
  I would like to follow some other users
  So that I can view their recipes more conveniently

  Background:
    Given I have registered in the system

  # Normal Flow
  Scenario: Follow a user
    Given I log in to my account
    And I did not follow that user before
    And this user exists in the system
    When I follow this user
    Then the user join my following list

  # Error Flow
  Scenario: Follow a user whose account has been deleted
    Given I log in to my account
    And I did not follow that user before
    And this user's account has been deleted
    When I follow this user
    Then an error message is prompted "This user does not exist"

   # Error Flow
  Scenario: Follow a user without logging in
    Given I have not logged in to my account
    And I did not follow that user before
    And this user exists in the system
    When I follow this user
    Then an error message is prompted "You must log in before follow a user"