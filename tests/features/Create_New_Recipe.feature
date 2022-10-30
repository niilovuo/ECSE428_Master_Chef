Feature: Create new recipe

As a recipe author
I want to add new recipes
So that I can share them with others

Background: 

Given "User1" exists in the system

And "User1" has created a recipe with the following information
	[[ "Recipe ID", "Recipe Title", "Prep Time", "Cook Time", "Directions" ],
	[ "1", "Pancakes with butter", "3:00", "5:00", "mix with water" ]]

And the recipe with id "1" has the following ingredients
	[["Ingredient Name", "Quantity"],
	["eggs", "2"],
	["butter", "1/4 tbsp"],
	["wheat flow", "1/2 cup"]]

Scenario: Logged in user attempts to create new recipe with valid recipe information (Normal Flow)

Given "User1" is logged into the system
When trying to create a recipe with the following information
	[[ "Recipe Title", "Prep Time", "Cook Time", "Directions" ],
	[ "Pancakes with oil", "3:00", "5:00", "mix with water" ]]
And the following list of ingredients
	[["Ingredient Name", "Quantity"],
	["eggs", "2"],
	["oil", "1/3 cup"],
	["wheat flow", "1/2 cup"]]
Then the number of recipes associated with "User1" will be "2"
And the recipe with the following information exists
	[[ "Recipe Title", "Prep Time", "Cook Time", "Directions" ],
	[ "Pancakes with oil", "3:00", "5:00", "mix with water" ]]
And the recipe with title "Pancakes with oil" will have the following ingredients
	[["Ingredient Name", "Quantity"],
	["eggs", "2"],
	["oil", "1/3 cup"],
	["wheat flow", "1/2 cup"]]

Scenario: Logged in user attempts to create new recipe with a title that they have already created (Alternate Flow)

Given "User1" is logged into the system
When trying to create a recipe with the following information
	[[ "Recipe Title", "Prep Time", "Cook Time", "Directions" ],
	[ "Pancakes with butter", "3:00", "5:00", "mix with water" ]]
And the following list of ingredients
	[["Ingredient Name", "Quantity"],
	["eggs", "2"],
	["butter", "1/4 tbsp"],
	["wheat flow", "1/2 cup"]]
Then the number of recipes associated with "User1" will be "2"
And the recipe with the following information exists
	[[ "Recipe Title", "Prep Time", "Cook Time", "Directions" ],
	[ "Pancakes with butter", "3:00", "5:00", "mix with water" ]]
And the recipe with title "Pancakes with butter" will have the following ingredients
	[["Ingredient Name", "Quantity"],
	["eggs", "2"],
	["butter", "1/4 tbsp"],
	["wheat flow", "1/2 cup"]]
But the system will issue a "You've already created a recipe with this name. Consider changing the name of the recipe so it will be more clear for users viewing your recipes." info message

Scenario: Logged out user attempts to create new recipe and with valid recipe information (Error flow)

Given User1 is not logged in 
When trying to create a recipe with the following information
	[[ "Recipe Title", "Prep Time", "Cook Time", "Directions" ],
	[ "Pancakes with oil", "3:00", "5:00", "mix with water" ]]
And the following list of ingredients
	[["Ingredient Name", "Quantity"],
	["eggs", "2"],
	["oil", "1/3 cup"],
	["wheat flow", "1/2 cup"]]
Then the number of recipes associated with "User1" will be "1"
And the "Please log in to create a recipe" error message will be issued
