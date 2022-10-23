Feature: Delete Account

As a user of Master Chief
I would like to delete an account of the Master Chef System
So I can start anew

Background:
    Given a user of Master Chief
    Given the following accounts exist in the system:
        | account name | password | email           |
        | Test         | Test1    | test1@gmail.com |
        | Test2        | Test2    | test2@gmail.com |

Scenario Outline: A user deletes an account (Normal Flow)

    Given a user "Test"
    When I enter the account name "Test"
    And I enter my email "test1@gmail.com"
    And I enter my password "Test1"
    Then the following account exist in the system:
        | account name | password | email           |
        | Test2        | Test2    | test2@gmail.com |
    And a "You have successfully deleted your account" message is issued

Scenario Outline: A user deletes an account with the wrong account name (Error Flow)

    Given a user "Test"
    When I enter the account name "Test2"
    And I enter my email "test1@gmail.com"
    And I enter my password "Test1"
    Then a "These account informations do not match our database" message is issued

Scenario Outline: A user deletes an account with the wrong email (Error Flow)

    Given a user "Test"
    When I enter the account name "Test"
    And I enter my email "test2@gmail.com"
    And I enter my password "Test1"
    Then a "These account informations do not match our database" message is issued

Scenario Outline: A user deletes an account with the wrong password (Error Flow)

    Given a user "Test"
    When I enter the account name "Test"
    And I enter my email "test1@gmail.com"
    And I enter my password "Test2"
    Then a "These account informations do not match our database" message is issued