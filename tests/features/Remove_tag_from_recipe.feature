Feature: Remove tag from recipe

As a recipe author
I would like to remove tags from my recipe
So that users will not mistakenly find my recipe under an incorrect set of tags

Background:
Given no tags at all


Scenario: Remove a tag from recipe (Normal Flow)

Given Recipe Author is logged into the system
And "RecipeTitle" is a recipe which was authored by Recipe Author
And "TagName" is a tag which exists in the system
And "TagName" is associated with "RecipeTitle"
And there are 3 tags associated with "RecipeTitle"
When requesting to remove "TagName" from recipe "RecipeTitle"
Then the "RecipeTitle" will not have "TagName" among its list of tags
And "RecipeTitle" is associated with 2 tags


Scenario: Remove multiple tags from recipe (Alternate Flow)

Given Recipe Author is logged into the system
And "RecipeTitle" is a recipe which was authored by Recipe Author
And "TagName1" and "TagName2" are tags which exist in the system
And "TagName1" and "TagName2" are associated with "RecipeTitle"
And there are 3 tags associated with "RecipeTitle"
When requesting to remove "TagName1" and "TagName2" from recipe "RecipeTitle"
Then the "RecipeTitle" will not have "TagName1" among its list of tags
And the "RecipeTitle" will not have "TagName2" among its list of tags
And "RecipeTitle" is associated with 1 tags


Scenario: Attempt to remove a tag not associated with recipe (Error Flow)

Given Recipe Author is logged into the system
And "RecipeTitle" is a recipe which was authored by Recipe Author
And "TagName" is a tag which exists in the system
And "TagName" is not associated with "RecipeTitle"
And there are 3 tags associated with "RecipeTitle"
#And "TagName" is not associated with "RecipeTitle"
When requesting to remove "TagName" from recipe "RecipeTitle"
Then the "RecipeTitle" will not have "TagName" among its list of tags
And "RecipeTitle" is associated with 3 tags
And the "Recipe does not have this tag" error message is issued

Scenario: Attempt to remove a tag which does not exist (Error Flow)

Given Recipe Author is logged into the system
And "RecipeTitle" is a recipe which was authored by Recipe Author
And "TagName" is a tag which does not exist in the system
And "TagName" is not associated with "RecipeTitle"
And there are 3 tags associated with "RecipeTitle"
When requesting to remove "TagName" from recipe "RecipeTitle"
Then the "RecipeTitle" will not have "TagName" among its list of tags
And "RecipeTitle" is associated with 3 tags
And the "Tag does not exist" error message is issued

Scenario: Unauthorized user attempts to remove a tag (Error Flow)

Given Recipe Author is logged into the system
And "RecipeTitle" is a recipe which was not authored by Recipe Author
And "TagName" is a tag which exists in the system
And "TagName" is associated with "RecipeTitle"
And there are 3 tags associated with "RecipeTitle"
When requesting to remove "TagName" from recipe "RecipeTitle"
Then the "RecipeTitle" will have "TagName" among its list of tags
And "RecipeTitle" is associated with 3 tags
And the "Cannot modify this recipe" error message is issued

Scenario: Logged out user attempts to remove a tag (Error Flow)

Given the user is not logged into the system
And "RecipeTitle" is a recipe which was authored by Recipe Author
And "TagName" is a tag which exists in the system
And "TagName" is associated with "RecipeTitle"
And there are 3 tags associated with "RecipeTitle"
When requesting to remove "TagName" from recipe "RecipeTitle"
Then the "RecipeTitle" will have "TagName" among its list of tags
And "RecipeTitle" is associated with 3 tags
And the "Need to log in to modify this recipe" error message is issued