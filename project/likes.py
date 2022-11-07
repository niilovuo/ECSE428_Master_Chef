from project.db import LikeRepo

def did_user_like(recipe_id, user_id):
    """
    Given a user id and a recipe id, return whether or not the user has liked the recipe.

    Parameters
    ----------
    recipe_id
    author_id

    Returns
    -------
    boolean
    """
    return LikeRepo.did_user_like(recipe_id, user_id)

def like_recipe(recipe_id, user_id):
    """
    Attempt to like a recipe; will fail if the recipe has already been liked,
    But this operation doesn't necesarily need to be handled because this will happen
    In cases with stale data, and assuming succes will fix the stale data...
    Eg. Client thinks recipe is not liked, tries to like recipe,
    Then regardless of the success or failure, expect the recipe to be liked
    Because if the recipe was already liked it still will be

    Parameters
    ----------
    recipe_id
    author_id

    Returns
    -------
    id of user on success;
    error message if failed
    """
    return LikeRepo.like_recipe(recipe_id, user_id)

def unlike_recipe(recipe_id, user_id):
    """
    Attempt to unlike a recipe

    Parameters
    ----------
    recipe_id
    author_id

    Returns
    -------
    id of user on success;
    error message if failed
    """
    return LikeRepo.unlike_recipe(recipe_id, user_id)
