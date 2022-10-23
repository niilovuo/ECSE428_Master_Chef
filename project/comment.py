from project.db import CommentRepo

def add_comment(title, body, author, recipe):
  """
  Add a new comment for a given recipe and save it to the db

  Parameters
  ----------
  title: comment title
  body: comment body
  author: comment author
  recipe: recipe to which the comment is posted

  Returns
  -------
  None on success
  str  on failure with error message
  """

  title = str(title).strip()
  if not title:
    return "The comment title cannot be blank"
  
  body = str(body).strip()
  if not body:
    return "The comment body cannot be blank"

  try:
    author = int(author)
    recipe = int(recipe)
    new_id = CommentRepo.add_comment(title, body, author, recipe)
    return new_id
  except Exception:
    # General message to abstract internal error from user
    return "Could not add comment, please try again"

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


def delete_comment_by_id(id, user_id, author_id):
  """
  Delete the comment by id

  Parameters
  ----------
  id:
    the id
  user_id
      the user_id
  author_id
      the author_id or comment
  Returns
  -------
  error message if failed
  None if success
  """
  if user_id is None:
    return "Must be logged in to preform this action"
  if user_id != author_id:
    return "No permission to delete comment"
  comment = CommentRepo.select_by_id(id)
  if comment is None:
    return "This comment does not exist"
  
  try: 
    err = CommentRepo.delete_by_id(id)
    return err
  except Exception:
    # General message to abstract internal error from user
    return "Could not delete comment, please try again"


def search_comment_by_recipe_id(recipe_id):
  """
  Searches the comment by id

  Parameters
  ----------
  recipe_id:
    the recipe id

  Returns
  -------
  the comments list or empty list if not found
  """

  return CommentRepo.select_by_recipe_id(recipe_id)

