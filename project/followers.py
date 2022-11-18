from project.account import search_account_by_id
from project.db import FollowersRepo


def unfollow_account_by_id(account_id, follower_id):
    """
    Attempt to unfollow an account by id
    Parameters
    ----------
    account_id
    follower_id

    Returns
    -------
    error message if failed
    None if success
    """
    if not follower_id:
        return "You must log in before unfollow a user"
    account = search_account_by_id(account_id)
    if not account:
        return "This user does not exist"
    try:
        err = FollowersRepo.delete_by_id(account_id, follower_id)
        return err
    except Exception:
        return "Could not unfollow account, please try again"
