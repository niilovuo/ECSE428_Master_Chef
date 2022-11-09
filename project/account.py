from werkzeug.security import generate_password_hash
from email_validator import validate_email
from project.db import AccountRepo

def add_new_account(name, email, password):
    """
    Attempts to add a new account.

    This one will validate + normalize + save it into a database

    Parameters
    ----------
    name:
      name of user
    email:
      email of user
    password:
      password of user

    Returns
    -------
    None on success
    str  on failure with error message
    """

    (r, err) = normalize_account_info(name, email, password)
    if r is None:
        return err

    (name, email, password) = r
    try:
        (r, err) = db_save_account(name, email, password)
        if r is None:
            return err
    except Exception as e:
        return "Unknown error occurred. Please try again later"

    return None

def normalize_account_info(name, email, password):
    """
    Validates and normalizes the name, email, and password.

    Note that all three being valid does not mean adding it to the server will
    succeed because it might have other constraints such as duplication.

    Parameters
    ----------
    name:
      name of user
    email:
      email of user
    password:
      password of user

    Returns
    -------
    ((name, email, password), None) on success
    (None, str)                     on failure
    """

    name = str(name).strip()
    if not name:
        return (None, "The account name cannot be blank")
    if any((not c.isalnum() and c != '_' for c in name)):
        return (None, "The account name must be alphanumeric or underscore")

    try:
        email = str(email).strip()
        email = validate_email(email, check_deliverability=False).email
    except:
        return (None, "The email is malformed")

    password = str(password).strip()
    if not password:
        return (None, "The password cannot be blank")
    if len(password) < 4:
        return (None, "The password must be at least 4 characters")
    if any((c.isspace() for c in password)):
        return (None, "The password cannot contain spaces")

    return ((name, email, password), None)

def db_save_account(name, email, password):
    """
    Attempts to save an account to the database.

    Note that the only additional operation done on the fields is hashing the
    password. This function does not perform any validation aside from checking
    for duplicate name and email.

    Parameters
    ----------
    name:
      name of user
    email:
      email of user
    password:
      password of user, it will get hashed

    Returns
    -------
    (id, None)  where id belongs to the new user on success
    (None, str) where str is an error message about duplicated name or email

    Exceptions
    ----------
    If some other exception happens (not caused by duplicated name or email),
    that is raised
    """

    try:
        new_id = AccountRepo.insert_row(
            name, email, generate_password_hash(password))
        return (new_id, None)
    except Exception as e:
        if AccountRepo.select_by_name(name) is not None:
            return (None, "This account name is already in use")

        if AccountRepo.select_by_email(email) is not None:
            return (None, "This email is already bound to an account")

        # if we can't determine why, just re-raise the old error
        raise e

def delete_account_by_id(id):
    """
    Delte account by id

    Parameters
    ----------
    id:
      the id

    Returns
    -------
    None on success
    """

    try:
      AccountRepo.delete_row_by_id(id)

    except Exception as e:
        return "Unknown error occurred. Please try again later"

    return None

def search_account_by_id(id):
    """
    Searches the account by id

    Parameters
    ----------
    id:
      the id

    Returns
    -------
    The account or None if not found
    """

    return AccountRepo.select_by_id(id)

def search_account_by_name(name):
    """
    Searchs the account by exact username

    Parameters
    ----------
    name:
      the exact username

    Returns
    -------
    The account or None if not found
    """

    return AccountRepo.select_by_name(name)

def search_account_by_filter(name, start, limit):
    """
    Searches account by name from some offset page

    Special handling around blank characters:
    -  empty name matches everything
    -  blank (non-empty) title never matches
       (though technically names can't have spaces anyways)
    -  everything else is matched as a substring / contains thing

    Parameters
    ----------
    name:
      name filter (case insensitive)
    start:
      starts from this offset (for pagination purposes)
    limit:
      returns at most this amount of entries (for pagination purposes)

    Returns
    -------
    list containing optionally many accounts
    """

    import re

    assert start >= 0
    assert limit >= 0

    if name and not name.strip():
        # name was blank (non-empty)
        return []

    name = re.escape(name.strip())
    results = AccountRepo.select_many_filtered(name, start, limit)
    return results

def search_account_by_email(email):
    """
    Searches the account by email

    Parameters
    ----------
    email:
      the email

    Returns
    -------
    The account or None if not found
    """

    return AccountRepo.select_by_email(email)

def convert_account_obj(account):
    """
    Converts account to a dict that can be jsonified
    (notably, the hashed password is dropped)

    Parameters
    ----------
    account:
      returned from the database

    Returns
    -------
    None if account was None
    a dict, password field is removed
    """

    if account is None:
        return None

    return {
        'id': account[0],
        'name': account[1],
        'email': account[2],
        'bio': account[4]   # skip [3], it's the password
    }

