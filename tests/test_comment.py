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


def test_delete_comment_by_id_valid_info(monkeypatch,app):
    monkeypatch.setattr("project.db.CommentRepo.delete_by_id", lambda id: None)
    monkeypatch.setattr("project.db.CommentRepo.select_by_id", lambda id: 1)
    err = delete_comment_by_id(1, 1, 1)
    assert err is None


def test_delete_comment_by_id_user_not_login(monkeypatch,app):
    err = delete_comment_by_id(1, None, 1)
    assert err == "Must be logged in to preform this action"


def test_delete_comment_by_id_invalid_permission(app):
    err = delete_comment_by_id(1, 2, 1)
    assert err == "No permission to delete comment"


def test_delete_comment_by_id_invalid_id(monkeypatch,app):
    monkeypatch.setattr("project.db.CommentRepo.select_by_id", lambda id: None)
    err = delete_comment_by_id(1, 1, 1)
    assert err == "This comment does not exist"


def test_delete_comment_by_id_Exception(monkeypatch,app):
    monkeypatch.setattr("project.db.CommentRepo.delete_by_id", throwConnectionError)
    monkeypatch.setattr("project.db.CommentRepo.select_by_id", lambda id: 1)
    err = delete_comment_by_id(1, 1, 1)
    assert err == "Could not delete comment, please try again"
