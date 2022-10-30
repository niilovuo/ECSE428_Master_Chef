Feature: Delete Account

As a user of Master Chef
I would like to delete my account for the Master Chef System
So that my account information no longer exists on the system database.

  Background:
    Given the user with id "1" exist in the system

  Scenario: A logged in user attempts to their delete account (Normal Flow)
    Given the user with id "1" is logged into the system
    When attempting to delete their account
    Then the user account with id "1" does not exist

  Scenario: Logged out user attempts to delete account (Error Flow)
    Given the user with id "1" is not logged into the system
    When attempting to delete their account
    Then the system will display an error message

