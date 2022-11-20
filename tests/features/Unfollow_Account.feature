Feature: Unfollow Account

As a user of the Master Chef cooking website
I would like to unfollow some other users
So that I can no longer view their recipes

Background:
  Given I am registered in the system

Scenario: Unfollow a user (Normal Flow)
  Given I'm logged in to my account
  And I followed a user before
  And this user exists in the system
  When I unfollow this user
  Then the user no longer in my following list

Scenario: Unfollow a user whose account has been deleted (Error Flow)
  Given I'm logged in to my account
  And I followed a user before
  And this user's account has been deleted
  When I unfollow this user
  Then an error message is prompted "This user does not exist"

Scenario: Unfollow a user while not logged in (Error Flow)
  Given I followed a user before
  And I'm not logged in to my account
  When I unfollow this user
  Then an error message is prompted "You must log in before unfollow a user"