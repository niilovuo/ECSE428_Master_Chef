from project.shopping_list import *


def test_view_shopping_list_valid_info(monkeypatch):
    monkeypatch.setattr("project.db.ShoppingItemsRepo.select_ingredient_by_account", lambda id: [('test', '20g')])
    shopping_list, err = get_shopping_list_of_account(1)
    assert err is None


def test_view_shopping_list_no_entries(monkeypatch):
    monkeypatch.setattr("project.db.ShoppingItemsRepo.select_ingredient_by_account", lambda id: [])
    shopping_list, err = get_shopping_list_of_account(1)
    assert err == "No items in shopping list"


def test_view_shopping_list_not_logged_in():
    shopping_list, err = get_shopping_list_of_account(None)
    assert err == "You must log in before viewing a shopping list"
