Feature: Edit account bio

As a user of the Master Chef cooking website
I would like to be able to introduce myself
So that I may befriend other Master Chef users

Scenario: Add an account bio (Normal Flow)

    Given a user of Master Chef is logged into the system
    And bio belongs to the Master Chef user
    And a default "Hello" in bio
    When requesting to add a "It's nice to meet you" message
    Then the system will change the default message to the requested "It's nice to meet you"

Scenario: Edit an account bio (Alternate Flow)

    Given a user of Master Chef is logged into the system
    And bio belongs to the Master Chef user
    And a "It's nice to meet you" message in the bio
    When requesting to edit a bio to "It's really nice to meet you" message
    And user confirms the changes to be saved
    Then the system will change the "It's nice to meet you" message to the requested "It's really nice to meet you"

Scenario: Logged out user attempts to edit an account bio (Error Flow)

    Given a user of Master Chef is not logged into the system
    And bio belongs to the Master Chef user
    And a "It's nice to meet you" message in the bio
    When requesting to edit a bio
    Then the system will issue an "Invalid edit" error message
