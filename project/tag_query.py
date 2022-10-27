from project.db import TagRepo

def get_all_tags():
    """
    Returns all the tags available on the server

    Returns
    -------
    All the tags
    """

    return TagRepo.select_all()

def get_tags_of_recipe(recipe_id):
    """
    Returns all the tags of the specified recipe

    Parameters
    ----------
    recipe_id:
      the id of the recipe

    Returns
    -------
    list of all recipe-associated-tags
    will happily return an empty list if id is does not exist
    """

    return TagRepo.select_by_recipe(recipe_id)


def search_tag_by_name(name):
    """
    Searches the comment by name

    Parameters
    ----------
    name:
      the name

    Returns
    -------
    The tag or None if not found
    """
    return TagRepo.select_by_name(str(name).strip())