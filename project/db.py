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
        cur.execute("""
            SELECT * FROM accounts WHERE name = %s
            """, (name,))
        return cur.fetchone()

    @staticmethod
    def select_by_email(email):
        global _conn
        cur = _conn.cursor()
        cur.execute("""
            SELECT * FROM accounts WHERE email = %s
            """, (email,))
        return cur.fetchone()

class RecipeRepo:

    @staticmethod
    def select_many_filtered(title, tags=[], offset=0, limit=None):
        if limit is None:
            limit = "ALL"

        global _conn
        cur = _conn.cursor()

        if not tags:
            # avoid querying recipe tags if we are not filtering based on tags
            # otherwise an empty recipe_tags table will cause trouble
            cur.execute(f"""
                SELECT * FROM recipes WHERE title ~* %s
                ORDER BY id
                LIMIT {limit} OFFSET {offset}
                """, (title,))
        else:
            cur.execute(f"""
                SELECT * FROM recipes WHERE title ~* %s AND id IN (
                  SELECT recipe FROM recipe_tags
                  GROUP BY recipe
                  HAVING ARRAY_AGG(tag) @> %s)
                ORDER BY id
                LIMIT {limit} OFFSET {offset}
                """, (title, tags))
        return cur.fetchall()

    @staticmethod
    def select_by_id(id):
        global _conn
        cur = _conn.cursor()
        cur.execute("""
            SELECT * FROM recipes WHERE id = %s
            """, (id,))
        return cur.fetchone()

class TagRepo:

    @staticmethod
    def select_all():
        global _conn
        cur = _conn.cursor()
        cur.execute("SELECT * FROM tags")
        return cur.fetchall()

    @staticmethod
    def select_by_names(names):
        global _conn
        cur = _conn.cursor()
        cur.execute("""
            SELECT * FROM tags WHERE name = ANY(%s)
            """, (names,))
        return cur.fetchall()

