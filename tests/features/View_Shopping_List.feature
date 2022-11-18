Feature: View shopping list

As a user of the Master Chef cooking website
I would like to view my shopping list
So I can view the ingredients I need to buy

Scenario: View a shopping list containing entries while logged in (Normal Flow)

  Given user 'abc' is logged into the system
  And the following entries exist in the shopping list for user 'abc'
    [
      ["ingredient name", "ingredient quantity"],
      ["leek", "200g"],
      ["coriander", "20g"]
    ]

  When user 'abc' requests to view their shopping list
  Then the system returns the following list
    [
      ["ingredient name", "ingredient quantity"],
      ["leek", "200g"],
      ["coriander", "20g"]
    ]

Scenario: View a shopping list containing no entries while logged in (Error Flow)

  Given user 'abc' is logged into the system
  And the no entries exist in the shopping list for user 'abc'
  When user 'abc' requests to view their shopping list
  Then the system issues a message "No items in shopping list"

Scenario: View a shopping list containing no entries while not logged in (Error Flow)

  Given the user is not logged into the system
  When the user requests to view their shopping list
  Then the system issues a message "You must log in before viewing a shopping list"
