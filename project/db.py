import psycopg2

_conn = None

def init_db_session(**kwargs):
    """
    Initializes a database connection

    Parameters
    ----------
    **kwargs:
      forwarded to psycopg2 connect
    """

    global _conn
    _conn = psycopg2.connect(**kwargs)

def deinit_db_session():
    """
    Deinitializes a database connection

    Further calls to get_db_session is undefined
    """

    global _conn
    _conn.close()
    _conn = None

def setup_db_tables():
    """
    Creates the tables defined in schema.sql if they are absent
    """

    global _conn
    try:
        cur = _conn.cursor()
        cur.execute(open('./project/schema.sql', 'r').read())
        _conn.commit()
    except Exception as e:
        _conn.rollback()
        raise e

def get_db_session():
    """
    Returns a connection to a database

    Returns
    -------
    connection to a database
    """

    global _conn
    return _conn
