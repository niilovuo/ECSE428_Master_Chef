from project.db import RecipeRepo, TagRepo
import re

PAGE_ENTRIES = 1024

def search_recipes_by_filter(title, tags, start):
    """
    Searches recipes by name and tags from some offset page

    A special handling around blank characters:
    -  empty title matches everything (so it's just tag filtering)
    -  blank (non-empty) title never matches
    -  everything else is matched as a substring / contains thing

    Parameters
    ----------
    title:
      recipes' names will contain this (case ignored)
    tags:
      recipes' tags will contain ALL of these
    start:
      starts from this offset (for pagination purposes)

    Returns
    -------
    (list, None) on success where list is a page of recipes
    (None, str)  on failure where str is the error message
    """

    assert start >= 0

    tag_ids = TagRepo.select_by_names(tags)
    if len(tag_ids) != len(tags):
        return (None, "This tag does not exist")

    if title and not title.strip():
        # the title was blank (non-empty)
        return ([], None)

    title = re.escape(title.strip())
    tag_ids = [ent[0] for ent in tag_ids]
    results = RecipeRepo.select_many_filtered(
            title, tag_ids, start * PAGE_ENTRIES, PAGE_ENTRIES)
    return (results, None)

def search_recipes_by_author(author_id):
    """
    Searches recipes by the author id

    Parameters
    ----------
    author_id:
      the id of the author

    Returns
    -------
    list of all recipes belonging to some author
    will happily return an empty list if author does not exist
    """

    return RecipeRepo.select_by_author(author_id)

def search_recipe_by_id(id):
    """
    Searches the recipe by id

    Parameters
    ----------
    id:
      the id

    Returns
    -------
    The recipe or None if not found
    """
    return RecipeRepo.select_by_id(id)

def search_followed_user_recipes(user_id):
    """
    Searches recipes by the author id

    Parameters
    ----------
    user_id:
      the id of the user

    Returns
    -------
    list of all recipes created by accounts followed by the user
    will happily return an empty list if author does not follow anyone
    """
    result = RecipeRepo.select_followed_user_recipes_by_user_id(user_id)
    return result

def convert_recipe_obj(recipe):
    """
    Converts recipe to a dict that can be jsonified
    (notably, flask does not know what to do about time)

    Parameters
    ----------
    recipe:
      returned from the database

    Returns
    -------
    a dict, time fields are strings of HH:MM:SS
    """

    return {
        'id': recipe[0],
        'title': recipe[1],
        'prep_time': str(recipe[2]) if recipe[2] else None,
        'cook_time': str(recipe[3]) if recipe[3] else None,
        'directions': recipe[4],
        'author': recipe[5],
        # 'image': recipe[6],  # Commented out because tojson does not enjoy memoryview objects
        'num_likes': recipe[7]
    }

