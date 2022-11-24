from project.db import IngredientRepo

def get_ingredients_of_recipe(recipe_id, user_id=None):
    """
    Returns all the ingredients of the specified recipe

    Parameters
    ----------
    recipe_id:
      the id of the recipe
    user_id:
      user to query whether the user has added said ingredient to their shopping list
    
    Returns
    -------
    list of all recipe-associated-ingredients,
      and boolean indicating whether user has added to their shopping list if user is specified
    will happily return an empty list if id is does not exist
    """

    return IngredientRepo.select_by_recipe(recipe_id, user_id)

