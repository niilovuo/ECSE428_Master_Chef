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

  if isinstance(author, int) and isinstance(recipe, int):
    try:
      new_id = CommentRepo.add_comment(title, body, author, recipe)
      return new_id
    except Exception:
      pass
  # General message to abstract internal error from user
  # author and recipe ids should always be integers
  return "Could not add comment, please try again"
