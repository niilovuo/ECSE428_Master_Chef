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

class AccountRepo:

    @staticmethod
    def insert_row(name, email, password):
        global _conn
        try:
            cur = _conn.cursor()
            cur.execute("""
                INSERT INTO accounts
                VALUES (DEFAULT, %s, %s, %s) RETURNING id
                """, (name, email, password))
            _conn.commit()
            return cur.fetchone()[0]
        except Exception as e:
            # rollback so continue (postgres's safety feature)
            _conn.rollback()
            raise e

    @staticmethod
    def select_by_name(name):
        global _conn
        cur = _conn.cursor()
        return cur.execute("""
            SELECT * FROM accounts WHERE name = %s
            """, (name,)).fetchone()

    @staticmethod
    def select_by_email(email):
        global _conn
        cur = _conn.cursor()
        return cur.execute("""
            SELECT * FROM accounts WHERE email = %s
            """, (email,)).fetchone()

