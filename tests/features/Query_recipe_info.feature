Feature: Query recipe info

As a user I would like to query recipe info so I can learn more about it

  Background:
    Given a user
    And no tags at all
    And a recipe named "Recipe Foo"
    And with a tag named "test-only"
    And with a tag named "foobars"
    And a recipe named "Recipe Bar"
    And with a tag named "baz"
    And with an ingredient "salt" of "5 tbsp"

  Scenario: Search for tags
    When I query tags of "Recipe Foo"
    Then I should have tags
      ["test-only", "foobars"]

  Scenario: Search for ingredients
    When I query ingredients of "Recipe Bar"
    Then I should have ingredients
      [ ["salt", "5 tbsp"] ]
