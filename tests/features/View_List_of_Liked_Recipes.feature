Feature: View list of recipes

As a user of the Master Chef cooking website
I would like to see the list of recipes I liked
So that I can quickly find and view the recipes I liked again

Background:
	Given the following accounts exist in the system:
    	[
		  [ "account_id", "account_name", "email", "password" ],
		  [ "1", "Dog Chef", "dogChef@mail.com", "password1" ],
		  [ "2", "Cat Chef", "catChef@mail.com", "milk364%" ],
		  [ "3", "Human Chef", "humanChef@mail.com", "psw123$" ],
		  [ "4", "MicrowaveChef", "microwave@mail.com", "psw@178" ]
    	]

Scenario: User views the list of recipes they liked while logged in (Normal Flow)
	Given "CatChef" is logged into the system
	And the following recipes exist in the system:
    	[
		  ["recipe_id", "recipe_title", "prep_time", "cook_time", "directions", "author_id"],
		  ["1", "Fluffy Cheese Cake", "00:30:00", "00:45:00", "Mix cheese with cake", "3"],
		  ["2", "Macaroni and Cheese", "00:10:00", "00:10:00", "Put cheese", "1"],
		  ["3", "Breakfast Eggs", "1:00", "3:00", "Crack eggs & microwave", "4"]
    	]
	And "CatChef" likes the "Macaroni and Cheese" recipe with recipe id "2"
	And "CatChef" likes the "Breakfast Eggs" recipe with recipe id "3"
	When attempting to view the list of recipes they liked
	Then the following list of recipes liked ids is returned:
		[
			["recipe_id"],
			[2],
			[3]
		]
Scenario: User with no recipes liked views their list of recipes liked while logged in (Alternative Flow)
	Given "CatChef" is logged into the system
	And did not like any recipes
	When attempting to view the list of recipes they liked
	Then the following list of recipes liked ids is returned:
		[["recipe_id"]]
Scenario: User Requests views list of recipes they liked with deleted recipe while logged in (Error Flow)
	Given "CatChef" is logged into the system
	And the following recipes exist in the system:
    	[
		  ["recipe_id", "recipe_title", "prep_time", "cook_time", "directions", "author_id"],
		  ["1", "Fluffy Cheese Cake", "00:30:00", "00:45:00", "Mix cheese with cake", "3"],
		  ["2", "Macaroni and Cheese", "00:10:00", "00:10:00", "Put cheese", "1"]
    	]
	And "CatChef" likes the "Fluffy Cheese Cake" recipe with recipe id "1"
	And "CatChef" likes the "Macaroni and Cheese" recipe with recipe id "2"
	And the author deleted recipe id "1"
	When "CatChef" attempts to view the list of recipes they liked
	Then the following list of recipes liked ids is returned:
		[
			["recipe_id"],
			[2]
		]
