from project.followers import *


def test_unfollow_account_by_id_valid_info(monkeypatch, app):
    monkeypatch.setattr("project.db.AccountRepo.select_by_id", lambda x: 1)
    monkeypatch.setattr("project.db.FollowersRepo.delete_by_id", lambda x, y: None)
    err = unfollow_account_by_id(1, 2)
    assert err is None


def test_unfollow_account_by_id_account_has_been_deleted(monkeypatch, app):
    monkeypatch.setattr("project.db.FollowersRepo.delete_by_id", lambda x, y: None)
    err = unfollow_account_by_id(1, 2)
    assert err == "This user does not exist"


def test_unfollow_account_by_id_while_not_logged_in(monkeypatch, app):
    monkeypatch.setattr("project.db.AccountRepo.select_by_id", lambda x: 1)
    monkeypatch.setattr("project.db.FollowersRepo.delete_by_id", lambda x, y: None)
    err = unfollow_account_by_id(1, None)
    assert err == "You must log in before unfollow a user"


def test_unfollow_account_by_id_exception(monkeypatch, app):
    monkeypatch.setattr("project.db.AccountRepo.select_by_id", lambda x: 1)
    monkeypatch.setattr("project.db.FollowersRepo.delete_by_id", lambda x, y: 1 // 0)
    err = unfollow_account_by_id(1, 2)
    assert err == "Could not unfollow account, please try again"


def test_follow_account_by_id_valid_info(monkeypatch, app):
    monkeypatch.setattr("project.db.AccountRepo.select_by_id", lambda x: 1)
    monkeypatch.setattr("project.db.FollowersRepo.insert_row", lambda x, y: None)
    err = follow_account_by_id(1, 2)
    assert err is None

def test_follow_account_by_id_account_has_been_deleted(monkeypatch, app):
    monkeypatch.setattr("project.db.FollowersRepo.insert_row", lambda x, y: None)
    err = follow_account_by_id(1, 2)
    assert err == "This user does not exist"

def test_follow_account_by_id_while_not_logged_in(monkeypatch, app):
    monkeypatch.setattr("project.db.AccountRepo.select_by_id", lambda x: 1)
    monkeypatch.setattr("project.db.FollowersRepo.insert_row", lambda x, y: None)
    err = follow_account_by_id(1, None)
    assert err == "You must log in before follow a user"

def test_follow_account_by_id_exception(monkeypatch, app):
    monkeypatch.setattr("project.db.AccountRepo.select_by_id", lambda x: 1)
    monkeypatch.setattr("project.db.FollowersRepo.insert_row", lambda x, y: 1 // 0)
    err = follow_account_by_id(1, 2)
    assert err == "Could not follow account, please try again"
