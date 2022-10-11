from werkzeug.security import generate_password_hash
from email_validator import validate_email
from project.db import get_db_session

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
        (r, err) = db_save_account(get_db_session(), name, email, password)
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

def db_save_account(db_session, name, email, password):
    """
    Attempts to save an account to the database.

    Note that the only additional operation done on the fields is hashing the
    password. This function does not perform any validation aside from checking
    for duplicate name and email.

    Parameters
    ----------
    db_session:
      database connection
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
        cur = db_session.cursor()
        cur.execute("""
            INSERT INTO accounts
            VALUES (DEFAULT, %s, %s, %s) RETURNING id
            """, (name, email, generate_password_hash(password)))
        db_session.commit()
        new_id = cur.fetchone()[0]
        return (new_id, None)
    except Exception as e:
        # rollback so continue (postgres's safety feature)
        db_session.rollback()

        # try to see if it was because of a duplicate name or email
        cur = db_session.cursor()
        cur.execute("""
            SELECT * FROM accounts WHERE name = %s
            """, (name,))
        if cur.fetchone() is not None:
            return (None, "This account name is already in use")

        cur = db_session.cursor()
        cur.execute("""
            SELECT * FROM accounts WHERE email = %s
            """, (email,))
        if cur.fetchone() is not None:
            return (None, "This email is already bound to an account")

        # if we can't determine why, just re-raise the old error
        raise e
