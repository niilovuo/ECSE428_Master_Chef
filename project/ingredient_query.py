from project.db import IngredientRepo

def get_ingredients_of_recipe(recipe_id):
    """
    Returns all the ingredients of the specified recipe

    Parameters
    ----------
    recipe_id:
      the id of the recipe

    Returns
    -------
    list of all recipe-associated-ingredients
    will happily return an empty list if id is does not exist
    """

    return IngredientRepo.select_by_recipe(recipe_id)

