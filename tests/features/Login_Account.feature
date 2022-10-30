Feature: Log in to account

As a user of the online cooking forum
I would like to log in to my account
So that I can use the features available only to logged in users


Scenario: Log in to an existing account with email & password (Normal Flow)

Given the user is not logged into the system
And an account by the name "acc1", email "abc@mail.com", password "123" exists within the system
When requesting to log in to account with email "abc@mail.com" and password "123"
Then the system updates the state for the user to be logged into account "acc1"

Scenario: Log in to a non-existing account (Error Flow)

Given the user is not logged into the system
And an account by the email "abc@mail.com" does not exist within the system
When requesting to log in to account with email "abc@mail.com" and password "123"
Then a "Incorrect username or password" message is issued
And the user is not logged into the system

Scenario: Log in to an existing account with incorrect password (Error Flow)

Given the user is not logged into the system
And an account by the name "acc1", email "abc@mail.com", password "123" exists within the system
When requesting to log in to account with email "abc@mail.com" and password "231"
Then a "Incorrect username or password" message is issued
And the user is not logged into the system

