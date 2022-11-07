from project.db import LikeRepo

def did_user_like(recipe_id, user_id):
    return LikeRepo.did_user_like(recipe_id, user_id)

def like_recipe(recipe_id, user_id):
    return LikeRepo.like_recipe(recipe_id, user_id)

def unlike_recipe(recipe_id, user_id):
    return LikeRepo.unlike_recipe(recipe_id, user_id)
