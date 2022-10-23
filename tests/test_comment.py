from project.comment import *

def test_addComment_ValidInfo(monkeypatch):
  monkeypatch.setattr("project.db.CommentRepo.add_comment", lambda title, body, author, recipe: 0)
  id = add_comment("Comment", "Hi, I'm a comment", 1, 1)
  assert type(id) is int

def test_addComment_InvalidTitle():
  id = add_comment("", "Hi, I'm a comment", 1, 1)
  assert id == "The comment title cannot be blank"

def test_addComment_InvalidBody():
  id = add_comment("Comment", "", 1, 1)
  assert id == "The comment body cannot be blank"

def test_addComment_InvalidAuthorId():
  id = add_comment("Comment", "Hi, I'm a comment", "not an integer", 1)
  assert id == "Could not add comment, please try again"

def test_addComment_InvalidRecipeId():
  id = add_comment("Comment", "Hi, I'm a comment", 1, "not an integer")
  assert id == "Could not add comment, please try again"

def test_addComment_Exception(monkeypatch):
  monkeypatch.setattr("project.db.CommentRepo.add_comment", throwConnectionError)
  id = add_comment("Comment", "Hi, I'm a comment", 1, 1)
  assert id == "Could not add comment, please try again"

# Pretend to throw exception from the repo
def throwConnectionError():
  raise Exception("Connection error")