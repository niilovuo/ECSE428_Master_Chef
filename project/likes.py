from project.db import LikeRepo
from project.recipe_query import search_recipe_by_id


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

def get_recipes_liked_by_liker(liker_id):
    """
    Returns all the recipes liked by the liker

    Parameters
    ----------
    liker_id: the id of the liker

    Returns
    -------
    list of liked recipe IDs or empty list if not found
    """
    return LikeRepo.select_all_recipes_liked_by_liker_id(liker_id)

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
    if user_id is None:
        return 'Please log in first'
    elif recipe_id is None:
        return 'Invalid recipe id'
    elif search_recipe_by_id(recipe_id) is None:
        return 'This recipe does not exist'
    else:
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
    if user_id is None:
        return 'Please log in first'
    elif recipe_id is None:
        return 'Invalid recipe id'
    elif search_recipe_by_id(recipe_id) is None:
        return 'This recipe does not exist'
    else:
        return LikeRepo.unlike_recipe(recipe_id, user_id)
