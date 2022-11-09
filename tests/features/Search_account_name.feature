Feature: Search account name

As a user of the Master Chef cooking website
I would like to search for accounts by name
So that I can find them and follow them

  Background:
    Given the following users in the system:
        [ "Joe", "Joan", "John", "Khan", "Q1",
          "Q2", "Q3", "Q4", "Q5", "Q6",
          "Q7", "Q8" ]

  Scenario: Search by exact name (Normal Flow)
    Given the query string "Joe"
    When a user requests to search for accounts
    Then the following list of accounts is returned:
      [ "Joe" ]

  Scenario: Search by matching (Alternate Flow)
    Given the query string "jo"
    When a user requests to search for accounts
    Then the following list of accounts is returned:
      [ "Joe", "Joan", "John" ]

  Scenario: List first page (Alternate Flow)
    Given the query string ""
    When a user requests to search for accounts
    Then the following list of accounts is returned:
      [ "Joe", "Joan", "John", "Khan", "Q1",
        "Q2", "Q3", "Q4", "Q5", "Q6" ]

  Scenario: List second page (Alternate Flow)
    Given the query string ""
    And start key 1
    When a user requests to search for accounts
    Then the following list of accounts is returned:
      [ "Q7", "Q8" ]

  Scenario: Search with blanks (Error Flow)
    Given the query string " "
    When a user requests to search for accounts
    Then the following list of accounts is returned:
      []
