from project.db import RecipeRepo, TagRepo, RecipeTagRepo

def add_tag_to_recipe(tag, recipe, user):
    """
    Adds a tag to a recipe as a certain user

    Parameters
    ----------
    tag:
      Name of the tag
    recipe:
      Id of the recipe
    user:
      Id of the user performing the change

    Returns
    -------
    None on success
    str  on failure where str is a error message
    """

    tag = TagRepo.select_by_name(str(tag).strip())
    if not tag:
        return "Tag does not exist"

    recipe = RecipeRepo.select_by_id_and_author(recipe, user)
    if not recipe:
        return "Cannot modify this recipe"

    try:
        RecipeTagRepo.insert_row(recipe[0], tag[0])
    except:
        # check if it fails because the tag is already there
        if RecipeTagRepo.check_exists(recipe[0], tag[0]):
            return "Recipe already has tag"

        return "Unknown error occurred"

