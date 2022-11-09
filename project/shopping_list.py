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
    shopping_items = ShoppingItemsRepo.select_by_account(account_id)
    if not shopping_items:
        return None, "No items in shopping list"
    shopping_list = []
    for item in shopping_items:
        ingredient = IngredientRepo.select_name_quantity_by_id(item[1])
        if ingredient:
            shopping_list.append(list(ingredient))
    return shopping_list, None
