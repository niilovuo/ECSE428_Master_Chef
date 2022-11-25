Feature: Edit account name

As a user of the Master Chef cooking website
I would like to change my user account
So that my account name is updated on the system

Scenario: Edit account name (Normal Flow)

    Given a user is logged into the system
    And account name "Master Chef" belongs to the user    
    When requesting to edit the account name to "newName"
    Then the system will change the account name to the requested "newName"


Scenario: Logged out user attempts to edit account name (Error Flow)

    Given a user is not logged into the system
    And account name "Master Chef" belongs to the user    
    When requesting to edit the account name to "newName"
    Then the system will issue an "Invalid edit" error message


Scenario: Edit account name with an empty string (Error Flow)

    Given a user is logged into the system
    And account name "Master Chef" belongs to the user    
    When requesting to edit the account name to an empty account name
    Then the system will issue an "Invalid edit" error message


Scenario: Edit account name with the name which is alreay taken by another user (Error Flow)

    Given a user is logged into the system
    And account name "Master Chef" belongs to the user    
    And there is a user with name "Another Master Chef"
    When requesting to edit the account name to "Another Master Chef"
    Then the system will issue an "Invalid edit" error message


Scenario: Edit account name with the name which includes a special character other than under score (Error Flow)

    Given a user is logged into the system
    And account name "Master Chef" belongs to the user    
    When requesting to edit the account name to "$$$"
    Then the system will issue an "Invalid edit" error message
