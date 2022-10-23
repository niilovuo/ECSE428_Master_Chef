from project.db import RecipeRepo
import re

def create_recipe(data, author):
    """
    Creates a recipe and a list of associated ingredients; 
    Data is expected as a form dictionary where ingredients are specified as ingredients[i][name|quantity],
    Where i represents the ingredient index and name|quanity whether that input is specifying name or quantity.
    Time for the recipe can be in the forms `HH:mm:ss`, `mm:ss`, or `mm`.
    """
    (data, ingredients) = parse_recipe_params(data)
    return RecipeRepo.insert_recipe(author_id = author, ingredients = ingredients, **data)

def edit_recipe(recipe_id, data, author):
    """
    Updates recipe data.
    The recipe's ingredients will be dynamically updated / created / deleted as required so that different length ingredients lists can be used. Form data format expected to be the same as in create_recipe.
    The author of the recipe will not be modified, and if the author does not match with the actual author of the recipe the transaciton will fail.
    """
    (data, ingredients) = parse_recipe_params(data)
    return RecipeRepo.update_recipe(recipe_id = recipe_id, author_id = author, ingredients = ingredients, **data)

def parse_recipe_params(data):
    recipe_data = {}
    ingredients = {}
    for (k,v) in data.items():
        ing = re.match("ingredients\[(.+)\]\[(name|quantity)\]", k)
        if ing == None:
            if k in ["prep_time", "cook_time"]:
                time = re.match("([0-9]+)(\:[0-9]+)?(\:[0-9]+)?", v)
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
            
