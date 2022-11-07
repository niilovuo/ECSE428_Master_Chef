Feature: Change account password

As a user of the Master Chef cooking website
I would like to change my password
So that I can log in with the new password

  Background:
    Given the following account is in the system:
      [
        [  "name",            "email", "password" ],
        [ "name1", "email1@gmail.com", "password1" ],
        [ "name2", "email2@gmail.com", "password2" ]
      ]

  Scenario: Successfully update password (Normal Flow)
    Given User "name1" is logged in
    And a current password "password1"
    And a new password "newPassword"
    And a confirm password "newPassword"
    When I request to update my password
    Then the operation succeeds
    And my password is changed

  Scenario Outline: Problematic cases (Error Flow)
    Given User "name1" is logged in
    And a current password <curpass>
    And a new password <newpass>
    And a confirm password <chkpass>
    When I request to update my password
    Then I should get the error message <errmsg>
    And my password stays as "password1"
  Examples:
    |     curpass |      newpass |      chkpass | errmsg |
    |     "wrong" |       "abcd" |       "abcd" | "Your current password information is incorrect" |
    | "password1" |           "" |           "" | "The password cannot be blank" |
    | "password1" |       "abcd" |        "abc" | "The confirm password does not match" |
    | "password1" |       "abcd" |           "" | "The confirm password does not match" |
    | "password1" |  "password1" |  "password1" | "The new password cannot be identical to the current one" |

  Scenario: Idempotent update (Alternate Flow)
    Given User "name1" is logged in
    And a current password ""
    And a new password ""
    And a confirm password ""
    When I request to update my password
    Then the operation succeeds
    And my password stays as "password1"

  Scenario: Unauthorized attempt (Error Flow)
    Given User "name1" is not logged in
    And a current password "password1"
    And a new password "newPassword"
    And a confirm password "newPassword"
    When I request to update my password
    Then I should get redirected to login
    And my password stays as "password1"
