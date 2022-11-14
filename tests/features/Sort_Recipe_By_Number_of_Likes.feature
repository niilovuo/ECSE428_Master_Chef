Feature: Sort recipe by number of likes

As a user of the Master Chef cooking website
I would like to sort the list of recipies by number of likes
So I can view the most critically acclaimed recipes on top

Background:

  Given the following recipes exist in the system
  | recipe id | recipe author | recipe title     | tags      | likes |
  | 1         | User1         | recipe title 1.1 | italian   | 1     |
  | 2         | User2         | recipe title 2   | vegan     | 4     |
  | 3         | User1         | recipe title 1.2 | vegan     | 3     |
  | 4         | User3         | recipe title 3   | mexican   | 2     |

Scenario: Sort list of all recipes (Normal flow)

  Given the user is accessing the list of recipes
  When the user requests to view the recipes in order of descending number of likes
  Then the system returns the following list of recipes:
  | recipe id | recipe author | recipe title     | tags      | likes |
  | 2         | User2         | recipe title 2   | vegan     | 4     |
  | 3         | User1         | recipe title 1.2 | vegan     | 3     |
  | 4         | User3         | recipe title 3   | mexican   | 2     |
  | 1         | User1         | recipe title 1.1 | italian   | 1     |

Scenario: Sort list of vegan recipes (Alternate flow)

  Given the user is accessing the list of recipes
  And the user has filtered based on the 'vegan' tag
  When the user requests to view the recipes in order of descending number of likes
  Then the system returns the following list of recipes:
  | recipe id | recipe author | recipe title     | tags      | likes |
  | 2         | User2         | recipe title 2   | vegan     | 4     |
  | 3         | User1         | recipe title 1.2 | vegan     | 3     |

Scenario: Sort list of mexican recipes (Alternate flow)

  Given the user is accessing the list of recipes
  And the user has filtered based on the 'mexican' tag
  When the user requests to view the recipes in order of descending number of likes
  Then the system returns the following list of recipes:
  | recipe id | recipe author | recipe title     | tags      | likes |
  | 4         | User3         | recipe title 3   | mexican   | 2     |