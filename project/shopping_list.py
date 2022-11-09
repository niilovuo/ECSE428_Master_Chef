from project.db import ShoppingItemsRepo, IngredientRepo


def get_shopping_list_of_account(account_id):
    """
    get shopping list of account

    Parameters
    ----------
    account_id:
    the id of the account

    Returns
    -------
    (list, None) on success where list is a page of ingredients
    (None, str)  on failure where str is the error message
    """
    if not account_id:
        return None, "You must log in before viewing a shopping list"
    shopping_list = ShoppingItemsRepo.select_ingredient_by_account(account_id)
    if not shopping_list:
        return None, "No items in shopping list"
    return shopping_list, None
