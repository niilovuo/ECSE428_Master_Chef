from project.db import CommentRepo


def search_comment_by_id(id):
    """
    Searches the comment by id

    Parameters
    ----------
    id:
      the id

    Returns
    -------
    The comment or None if not found
    """

    return CommentRepo.select_by_id(id)


def delete_comment_by_id(id, user_login):
    """
    Delete the comment by id

    Parameters
    ----------
    id:
      the id
    user_login
        user is login True or False
    Returns
    -------
    False, error message if failed
    True, None if success
    """
    if not user_login:
        return False, "Must be logged in to preform this action"
    comment = CommentRepo.select_by_id(id)
    if comment is None:
        return False, "This comment does not exist"
    flag = CommentRepo.delete_by_id(id)
    return flag, None

def search_comment_by_recipe_id(recipe_id):
    """
    Searches the comment by id

    Parameters
    ----------
    recipe_id:
      the recipe id

    Returns
    -------
    The comment list or an empty list if not found
    """

    return CommentRepo.select_by_recipe_id(recipe_id)
