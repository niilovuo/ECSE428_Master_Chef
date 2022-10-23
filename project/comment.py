from project.db import CommentRepo, RecipeRepo

def get_comments_of_recipe(recipe_id):
    """
    Returns all the comments of the specified recipe

    Parameters
    ----------
    recipe_id:
      the recipe id

    Returns
    -------
    Comments list or empty list if no comment

    """

    return CommentRepo.select_by_recipe_id(recipe_id)
