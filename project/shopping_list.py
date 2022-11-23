from project.db import ShoppingItemsRepo


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


def add_ingredient_to_shopping_items(account_id, ingredient_id):
    """
        add ingredient to shopping list of account
        does not add duplicate ingredient

        Parameters
        ----------
        account_id:
        the id of the account

        ingredient_id:
        the id of ingredient

        Returns
        -------
        None on success
        str on failure where str is the error message
    """
    try:
        ShoppingItemsRepo.insert_row(account_id, ingredient_id)
        return None
    except Exception as e:
        return "Unknown error occurred. Item could not be added"


def delete_ingredient_from_shopping_items(ingredient_id, account_id):
    """
        remove ingredient from shopping list of account

        Parameters
        ----------

        ingredient_id:
        the id of ingredient

        account_id:
        the id of the account

        Returns
        -------
        None on success
        str on failure where str is the error message
    """
    try:
        deleted = ShoppingItemsRepo.delete_by_id(ingredient_id, account_id)
        if deleted == 0:
            return "Item not in shopping list"
        else:
            return None
    except Exception as e:
        return "Unknown error occurred. Item could not be removed"
