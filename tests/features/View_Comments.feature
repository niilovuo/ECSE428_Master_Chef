Feature: View Comments

As a user
I would like to view the comments for a recipe
So that I can engage with other people

Scenario: User Requests List of Comments for a Recipe (Normal Flow)
  Given the recipe with id "1" exists in the system
  And the following comments exist in the system:
    [
      [ "comment_id", "title", "body", "author_id", "recipe_id" ],
      [ "1", "Food", "I like food", "3", "1" ],
      [ "2", "No food", "Food is gross", "1", "1" ],
      [ "3", "Food ok", "Some food is ok I guess", "2", "1" ]
    ]
  When a user requests the list of comments for recipe "1"
  Then the following list of comments is returned:
    [
      [ "comment_id", "title", "body", "author_id", "recipe_id" ],
      [ "1", "Food", "I like food", "3", "1" ],
      [ "2", "No food", "Food is gross", "1", "1" ],
      [ "3", "Food ok", "Some food is ok I guess", "2", "1" ]
    ]

Scenario: User Requests List of Comments for a Recipe with No Comments (Alternative Flow)
  Given the recipe with id "1" exists in the system
  And the following comments exist in the system:
      [[ "comment_id", "title", "body", "author_id", "recipe_id" ]]
  When a user requests the list of comments for recipe "1"
  Then the following list of comments is returned:
      [[ "comment_id", "title", "body", "author_id", "recipe_id" ]]
