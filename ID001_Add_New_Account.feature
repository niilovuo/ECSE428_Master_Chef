Feature: Add New Account

As a user of Master Chief
I would like to create an account for the Master Chef System
So I can discuss new recipes with fellow cooks

Background:

    Given the following accounts exist in the system:
        | account name | password | email           |
        | Test         | Test1    | test1@gmail.com |
        | Test2        | Test2    | test2@gmail.com |

Scenario Outline: New user creates an account (Normal Flow)

    Given I am a new user
    When I enter an unused account name <account name>
    And I enter my email
    And I enter my desired password
    Then the account name shall exist in the system
    And the system will remember my email
    And the system will remember my password

Scenario Outline: New user creates an account with used account name (Error Flow)

    Given I am a new user
    When I enter the account name "Test"
    And I enter my email
    And I enter my desired password
    Then a "This account name is already in use" message is issued

Scenario Outline: A user creates another account (Error Flow)

    Given a user "Test"
    When I enter an unused account name <account name>
    And I enter my email "test1@gmail.com"
    And I enter my desired password
    Then a "This email is already bound to an account" message is issued