from itertools import zip_longest

import psycopg2

# XXX: If you don't belong in Db, you very likely should not be accessing this
_conn = None

class Db:

    @staticmethod
    def init_session(**kwargs):
        """
        Initializes a database connection

        Parameters
        ----------
        **kwargs:
          forwarded to psycopg2 connect
        """

        global _conn
        _conn = psycopg2.connect(**kwargs)

    @staticmethod
    def deinit_session():
        """
        Deinitializes a database connection

        Further calls to get_db_session is undefined
        """

        global _conn
        _conn.close()
        _conn = None

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

    @staticmethod
    def get_session():
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
    def insert_recipe(title, author_id, prep_time=None, cook_time=None, directions="", ingredients=[]):
        _conn = Db.get_session()
        try:
            cur = _conn.cursor()
            cur.execute("""
                INSERT INTO recipes (title, prep_time, cook_time, directions, author)
                VALUES (%s, %s, %s, %s, %s) RETURNING id;
                """, (title, prep_time, cook_time, directions, author_id))
            recipe_id = cur.fetchone()[0]
            print(recipe_id)
            cur.executemany("INSERT INTO ingredients (name, quantity, recipe) VALUES (%s, %s, %s);", [(e["name"], e["quantity"], recipe_id) for e in ingredients])
            _conn.commit()
            print(recipe_id)
            return recipe_id
        except Exception as e:
            _conn.rollback()
            raise e

    @staticmethod
    def update_recipe(recipe_id, title, prep_time, cook_time, directions, author_id, ingredients):
        _conn = Db.get_session()
        try:
            cur = _conn.cursor()
            cur.execute("SELECT author FROM recipes WHERE id = %s;", (recipe_id,))
            author_recipe_id = cur.fetchone()[0]
            if (author_recipe_id != author_id):
                raise Exception("Not your recipe")
            cur.execute("UPDATE recipes SET title = %s, prep_time = %s, cook_time = %s, directions = %s WHERE id = %s;", (title, prep_time, cook_time, directions, recipe_id))
            cur.execute("SELECT id FROM ingredients WHERE recipe = %s;", (recipe_id,))
            extant_ingredients = cur.fetchall()
            print(extant_ingredients)
            for (new, ext) in zip_longest(ingredients, extant_ingredients):
                if new == None:
                    cur.execute("DELETE FROM ingredients WHERE id = %s;", ext)
                elif ext == None:
                    cur.execute("INSERT INTO ingredients (name, quantity, recipe) VALUES (%s, %s, %s);", (new["name"], new["quantity"], recipe_id))
                else:
                    cur.execute("UPDATE ingredients SET name = %s, quantity = %s WHERE id = %s", (new["name"], new["quantity"], ext[0]))
            _conn.commit()
            return recipe_id
        except Exception as e:
            _conn.rollback()
            raise e
    
class TagRepo:

    @staticmethod
    def select_all():
        _conn = Db.get_session()
        cur = _conn.cursor()
        cur.execute("SELECT * FROM tags")
        return cur.fetchall()

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
            return str(e)

