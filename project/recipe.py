from project.db import RecipeRepo
import re

def create_recipe(data, author):
    (data, ingredients) = parse_recipe_params(data)
    return RecipeRepo.insert_recipe(author_id = author, ingredients = ingredients, **data)
    
def edit_recipe(recipe_id, data, author):
    (data, ingredients) = parse_recipe_params(data)
    return RecipeRepo.update_recipe(recipe_id = recipe_id, author_id = author, ingredients = ingredients, **data)

def parse_recipe_params(data):
    recipe_data = {}
    ingredients = {}
    print(data)
    for (k,v) in data.items():
        ing = re.match("ingredients\[(.+)\]\[(name|quantity)\]", k)
        if ing == None:
            if k in ["prep_time", "cook_time"]:
                time = re.match("([0-9]+)(\:[0-9]+)?(\:[0-9]+)?", v)
                if time != None:
                    print(time.groups())
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
            
