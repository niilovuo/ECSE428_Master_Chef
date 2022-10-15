Feature: Add New Account

As a user of Master Chef
I would like to create an account for the Master Chef System
So I can share & discuss new recipes with fellow cooks

  Background:
    Given the following accounts exist in the system
        [
            [ "account name", "password", "email" ],
            [ "Test", "Test1", "test1@gmail.com" ],
            [ "Test2", "Test2", "test2@gmail.com" ]
        ]

  Scenario: New user creates an account (Normal Flow)

    Given the user is not logged into the system
    When attempting to create an account "newAccount1", with email "newAccount1@gmail.com" and password "newAccount1"
    Then the operation should succeed
    And the account name "newAccount1" is associated with the email "newAccount1@gmail.com"
    And the account name "newAccount1" is associated with the password "newAccount1"

  Scenario: New user creates an account with used account name (Error Flow)

    Given the user is not logged into the system
    When attempting to create an account "Test", with email "newAccount2@gmail.com" and password "newAccount2"
    Then the "This account name is already in use" error message is issued
    And the account name "Test" is associated with the email "test1@gmail.com"

  Scenario: A user creates another account (Error Flow)

    Given the user is not logged into the system
    When attempting to create an account "newAccount3", with email "test1@gmail.com" and password "newAccount3"
    Then the "This email is already bound to an account" error message is issued
    And the account name "Test" is associated with the email "test1@gmail.com"

