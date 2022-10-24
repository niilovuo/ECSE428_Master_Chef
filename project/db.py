import psycopg2
from flask import g

# XXX: You should never access these (unless you are Db)
_db_conf = None

class Db:

    @staticmethod
    def init_session(**kwargs):
        """
        Initializes data required to establish a database connection

        Parameters
        ----------
        **kwargs:
          forwarded to psycopg2 connect
        """

        global _db_conf
        _db_conf = kwargs

    @staticmethod
    def deinit_session():
        """
        Closes a session to a database

        If no sessions are opened, then nothing happens
        """

        _conn = g.pop("_conn", None)
        if _conn:
            _conn.close()

    @staticmethod
    def get_session():
        """
        Returns a connection to a database

        If session was closed, then it is reopened using info from init_session

        Returns
        -------
        connection to a database
        """

        if "_conn" not in g:
            g._conn = psycopg2.connect(**_db_conf)

        return g._conn

    @staticmethod
    def setup_tables():
        """
        Creates the tables defined in schema.sql if they are absent
        """

        _conn = Db.get_session()
        try:
            cur = _conn.cursor()
            cur.execute(open('./project/schema.sql', 'r').read())
            _conn.commit()
        except Exception as e:
            _conn.rollback()
            raise e

class AccountRepo:

    @staticmethod
    def insert_row(name, email, password):
        _conn = Db.get_session()
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
        _conn = Db.get_session()
        cur = _conn.cursor()
        cur.execute("""
            SELECT * FROM accounts WHERE name = %s
            """, (name,))
        return cur.fetchone()

    @staticmethod
    def select_by_email(email):
        _conn = Db.get_session()
        cur = _conn.cursor()
        cur.execute("""
            SELECT * FROM accounts WHERE email = %s
            """, (email,))
        return cur.fetchone()

    @staticmethod
    def select_by_id(id):
        _conn = Db.get_session()
        cur = _conn.cursor()
        cur.execute("""
            SELECT * FROM accounts WHERE id = %s
            """, (id,))
        return cur.fetchone()

class RecipeRepo:

    @staticmethod
    def select_many_filtered(title, tags=[], offset=0, limit=None):
        if limit is None:
            limit = "ALL"

        _conn = Db.get_session()
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
                  HAVING ARRAY_AGG(tag) @> %s::integer[])
                ORDER BY id
                LIMIT {limit} OFFSET {offset}
                """, (title, tags))
        return cur.fetchall()

    @staticmethod
    def select_by_id(id):
        _conn = Db.get_session()
        cur = _conn.cursor()
        cur.execute("""
            SELECT * FROM recipes WHERE id = %s
            """, (id,))
        return cur.fetchone()

    @staticmethod
    def select_by_id_and_author(id, author_id):
        _conn = Db.get_session()
        cur = _conn.cursor()
        cur.execute("""
            SELECT * FROM recipes WHERE id = %s AND author = %s
            """, (id, author_id))
        return cur.fetchone()

class TagRepo:

    @staticmethod
    def select_all():
        _conn = Db.get_session()
        cur = _conn.cursor()
        cur.execute("SELECT * FROM tags")
        return cur.fetchall()

    @staticmethod
    def select_by_name(name):
        _conn = Db.get_session()
        cur = _conn.cursor()
        cur.execute("""
            SELECT * FROM tags WHERE name = %s
            """, (name,))
        return cur.fetchone()

    @staticmethod
    def select_by_names(names):
        _conn = Db.get_session()
        cur = _conn.cursor()
        cur.execute("""
            SELECT * FROM tags WHERE name = ANY(%s)
            """, (names,))
        return cur.fetchall()

    @staticmethod
    def select_by_recipe(recipe_id):
        _conn = Db.get_session()
        cur = _conn.cursor()

        cur.execute("""
            SELECT * FROM tags WHERE id in (
              SELECT tag from recipe_tags
              WHERE recipe = %s)
            """, (recipe_id,))
        return cur.fetchall()

class RecipeTagRepo:

    @staticmethod
    def insert_row(recipe, tag):
        _conn = Db.get_session()
        try:
            cur = _conn.cursor()
            cur.execute("""
                INSERT INTO recipe_tags
                VALUES (%s, %s)
                """, (recipe, tag))
            _conn.commit()
        except Exception as e:
            _conn.rollback()
            raise e

    @staticmethod
    def check_exists(recipe, tag):
        _conn = Db.get_session()
        cur = _conn.cursor()
        cur.execute("""
            SELECT * FROM recipe_tags WHERE
            recipe = %s AND tag = %s
            """, (recipe, tag))
        return cur.fetchone() is not None

class IngredientRepo:

    @staticmethod
    def select_by_recipe(recipe_id):
        _conn = Db.get_session()
        cur = _conn.cursor()

        cur.execute("""
            SELECT * FROM ingredients
            WHERE recipe = %s
            """, (recipe_id,))
        return cur.fetchall()

class CommentRepo:

    @staticmethod
    def add_comment(title, body, author, recipe):
        _conn = Db.get_session()
        try:
            cur = _conn.cursor()
            cur.execute("""
                INSERT INTO comments
                VALUES (DEFAULT, %s, %s, %s, %s) RETURNING id
                """, (title, body, author, recipe))
            _conn.commit()
            return cur.fetchone()[0]
        except Exception as e:
            _conn.rollback()
            raise e

    @staticmethod
    def select_all():
        _conn = Db.get_session()
        cur = _conn.cursor()
        cur.execute("SELECT * FROM comments")
        return cur.fetchall()

    @staticmethod
    def select_by_id(id):
        _conn = Db.get_session()
        cur = _conn.cursor()
        cur.execute("""
                SELECT * FROM comments WHERE id = %s
                """, (id,))
        return cur.fetchone()

    @staticmethod
    def select_by_recipe_id(recipe_id):
        _conn = Db.get_session()
        cur = _conn.cursor()
        cur.execute("""
                SELECT * FROM comments WHERE recipe = %s
                """, (recipe_id,))
        return cur.fetchall()

    @staticmethod
    def delete_by_id(id):
        try:
            _conn = Db.get_session()
            cur = _conn.cursor()
            cur.execute("""
                    DELETE FROM comments WHERE id = %s
                    """, (id,))
            _conn.commit()
            return None
        except Exception as e:
            _conn.rollback()
            raise e

