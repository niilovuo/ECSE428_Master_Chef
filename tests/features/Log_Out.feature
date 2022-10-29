Feature: Log out from account

As a user of the online cooking forum
I would like to log out of my account
So that I can securely end my session with the online cooking forum

Scenario: Log out of account while logged in (Normal flow)
Given account with email "test@test.com" and password "kul32" exists in the system
And user with email "test@test.com" and password "kul32" is logged into the system
When a log out operation is requested
Then the system updates the state for the user "test@test.com" to logged out

Scenario: Log out of account while logged out (Error flow)

Given the user is not logged into the system
When a log out operation is requested
Then the system retains the state for the user as logged out

