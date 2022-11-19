from project.db import RecipeRepo, TagRepo, RecipeTagRepo
import re

def create_recipe(data, author):
    """
    Creates a recipe and a list of associated ingredients; 
    Data is expected as a form dictionary where ingredients are specified as ingredients[i][name|quantity],
    Where i represents the ingredient index and name|quanity whether that input is specifying name or quantity.
    Time for the recipe can be in the forms `HH:mm:ss`, `mm:ss`, or `mm`.
    Returns id of recipe upon success, otherwise throws an error.
    """
    (data, ingredients) = parse_recipe_params(data)
    return RecipeRepo.insert_recipe(author_id = author, ingredients = ingredients, **data)

def edit_recipe(recipe_id, data, author):
    """
    Updates recipe data.
    The recipe's ingredients will be dynamically updated / created / deleted as required so that different length ingredients lists can be used. Form data format expected to be the same as in create_recipe.
    The author of the recipe will not be modified, and if the author does not match with the actual author of the recipe the transaciton will fail.
    Returns id of recipe upon success, otherwise throws an error.
    """
    (data, ingredients) = parse_recipe_params(data)
    return RecipeRepo.update_recipe(recipe_id = recipe_id, author_id = author, ingredients = ingredients, **data)

def delete_recipe_by_id(recipe_id, user_id, author_id):
    """
    Delete the recipe by id

    Parameters
    ----------
    id:
      recipe id
    user_id
        the user_id
    author_id
        the author_id
    Returns
    -------
    error message if failed
    None if success
    """
    if user_id is None:
        return "You need to log in to delete this recipe"
    if user_id != author_id:
        return "Only the author of this recipe can modify the recipe"

    recipe = RecipeRepo.select_by_id(recipe_id)
    if recipe is None:
        return "This recipe does not exist"

    try:
        err = RecipeRepo.delete_by_id(id)
        return err
    except Exception:
        # General message to abstract internal error from user
        return "Could not delete recipe, please try again"


def delete_recipe_by_id(recipe_id, user_id, author_id):
    """
    Delete the recipe by id
    Parameters
    ----------
    id:
      recipe id
    user_id
        the user_id
    author_id
        the author_id
    Returns
    -------
    error message if failed
    None if success
    """
    if user_id is None:
        return "You need to log in to delete this recipe"
    if user_id != author_id:
        return "Only the author of this recipe can modify the recipe"

    recipe = RecipeRepo.select_by_id(recipe_id)
    if recipe is None:
        return "This recipe does not exist"

    try:
        err = RecipeRepo.delete_by_id(recipe_id)
        return err
    except Exception:
        # General message to abstract internal error from user
        return "Could not delete recipe, please try again"

def parse_recipe_params(data):
    recipe_data = {}
    ingredients = {}
    for (k,v) in data.items():
        ing = re.match("ingredients\\[(.+)\\]\\[(name|quantity)\\]", k)
        if ing == None:
            if k in ["prep_time", "cook_time"]:
                time = re.match("([0-9]+)(\\:[0-9]+)?(\\:[0-9]+)?", v)
                if time != None:
                    ts = [t for t in time.groups() if t != None]
                    if len(ts) == 1:
                        ts.append(":00")
                    if len(ts) == 2:
                        ts.insert(0, "00:")
                        
                    recipe_data[k] = "".join(ts)
            else:
                recipe_data[k] = v
        elif v != "":
            if ing.group(1) in ingredients:
                ingredients[ing.group(1)][ing.group(2)] = v
            else:
                ingredients[ing.group(1)] = {ing.group(2): v}
    return (recipe_data, ingredients.values())
            
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


def remove_tag_of_recipe(tag_name, recipe_id, user_id):
    """
    remove a tag of a recipe as a certain user

    Parameters
    ----------
    tag_name:
      Name of the tag
    recipe_id:
      Id of the recipe
    user_id:
      Id of the user performing the change

    Returns
    -------
    None on success
    str  on failure where str is a error message
    """
    if user_id is None:
        return "Need to log in to modify this recipe"
    tag = TagRepo.select_by_name(str(tag_name).strip())
    if not tag:
        return "Tag does not exist"

    recipe = RecipeRepo.select_by_id_and_author(recipe_id, user_id)
    if not recipe:
        return "Cannot modify this recipe"
    exists = RecipeTagRepo.check_exists(recipe_id, tag[0])
    if not exists:
        return "Recipe does not have this tag"
    try:
        error = RecipeTagRepo.delete_by_id(recipe_id, tag[0])
        return error
    except Exception:
        return "Could not remove tag of recipe, please try again"

def add_image_to_recipe(image, recipe_id, user_id):
    """
    add an image to a recipe as the author

    Parameters
    ----------
    image:
      Image data
    recipe_id:
      Id of the recipe
    user_id:
      Id of the user performing the change

    Returns
    -------
    None on success
    str  on failure where str is a error message
    """
    if user_id is None:
        return "Need to log in to modify this recipe"
    recipe = RecipeRepo.select_by_id_and_author(recipe_id, user_id)
    if not recipe:
        return "Cannot modify this recipe"
    try:
        error = RecipeRepo.update_image_by_id(image, recipe_id)
        return error
    except Exception as e:
        return "Could not add image to recipe, please try again"
