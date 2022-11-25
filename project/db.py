from itertools import zip_longest

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
            cur.execute(open('./project/db_data.sql', 'r').read())
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
                VALUES (DEFAULT, %s, %s, %s, %s) RETURNING id
                """, (name, email, password, ''))
            _conn.commit()
            return cur.fetchone()[0]
        except Exception as e:
            # rollback so continue (postgres's safety feature)
            _conn.rollback()
            raise e

    @staticmethod
    def delete_row_by_id(id):
        try:
            _conn = Db.get_session()
            cur = _conn.cursor()
            cur.execute("""
                    DELETE FROM accounts WHERE id = %s
                    """, (id,))
            _conn.commit()
            return None
        except Exception as e:
            _conn.rollback()
            raise e

    @staticmethod
    def select_many_filtered(name, offset=0, limit=None):
        if limit is None:
            limit = "ALL"

        _conn = Db.get_session()
        cur = _conn.cursor()
        cur.execute(f"""
            SELECT * FROM accounts WHERE name ~* %s
            ORDER BY id
            LIMIT {limit} OFFSET {offset}
            """, (name,))
        return cur.fetchall()

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

    @staticmethod
    def update_password(id, password):
        try:
            _conn = Db.get_session()
            cur = _conn.cursor()
            cur.execute("""
                UPDATE accounts SET password = %s WHERE id = %s
                """, (password, id))
            _conn.commit()
        except Exception as e:
            _conn.rollback()
            raise e
    
    @staticmethod
    def update_name_by_id(name,id):
        try:
            _conn = Db.get_session()
            cur = _conn.cursor()
            cur.execute("""
                UPDATE accounts SET name = %s WHERE id = %s 
                """, (name, id,))
            _conn.commit()
            return None

        except Exception as e:
            _conn.rollback()
            raise e
            
    @staticmethod
    def update_bio_by_id(bio, id):
        try: 
            _conn = Db.get_session()
            cur = _conn.cursor()
            cur.execute("""
                UPDATE accounts SET bio = %s WHERE id = %s 
                """, (bio, id,))
            _conn.commit()
            return None
        except Exception as e:
            _conn.rollback()
            raise e

    @staticmethod
    def update_email_by_id(email, id):
        try:
            _conn = Db.get_session()
            cur = _conn.cursor()
            cur.execute("""
                UPDATE accounts SET email = %s WHERE id = %s 
                """, (email, id,))
            _conn.commit()
            return None
        except Exception as e:
            _conn.rollback()
            raise e

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
                SELECT recipes.*, COUNT(liked_recipes.*) AS num_likes FROM recipes
                LEFT JOIN liked_recipes ON recipes.id = liked_recipes.recipe
                WHERE title ~* %s
                GROUP BY recipes.id
                ORDER BY num_likes DESC, recipes.id
                LIMIT {limit} OFFSET {offset};
                """, (title,))
        else:
            cur.execute(f"""
                SELECT recipes.*, COUNT(liked_recipes.*) AS num_likes FROM recipes
                LEFT JOIN liked_recipes ON recipes.id = liked_recipes.recipe
                WHERE title ~* %s AND id IN (
                  SELECT recipe FROM recipe_tags
                  GROUP BY recipe
                  HAVING ARRAY_AGG(tag) @> %s::integer[])
                GROUP BY recipes.id
                ORDER BY num_likes DESC, recipes.id
                LIMIT {limit} OFFSET {offset};
                """, (title, tags))
        return cur.fetchall()

    @staticmethod
    def select_by_id(id):
        _conn = Db.get_session()
        cur = _conn.cursor()
        cur.execute("""
            SELECT recipes.*, COUNT(liked_recipes.*) AS num_likes FROM recipes
            LEFT JOIN liked_recipes ON recipes.id = liked_recipes.recipe
            WHERE recipes.id = %s
            GROUP BY recipes.id;
            """, (id,))
        return cur.fetchone()

    @staticmethod
    def select_by_author(author_id):
        _conn = Db.get_session()
        cur = _conn.cursor()

        cur.execute("""
            SELECT recipes.*, COUNT(liked_recipes.*) AS num_likes FROM recipes
            LEFT JOIN liked_recipes ON recipes.id = liked_recipes.recipe
            WHERE recipes.author = %s
            GROUP BY recipes.id
            ORDER BY num_likes DESC, recipes.id;
            """, (author_id,))
        return cur.fetchall()

    @staticmethod
    def select_followed_user_recipes_by_user_id(follower):
        _conn = Db.get_session()
        cur = _conn.cursor()
        cur.execute("""SELECT id FROM recipes
            WHERE recipes.author in (SELECT account FROM followers where follower = %s)
            ORDER BY recipes.id""", (follower,))
        return cur.fetchall()

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
            cur.executemany("INSERT INTO ingredients (name, quantity, recipe) VALUES (%s, %s, %s);",
                            [(e["name"], e["quantity"], recipe_id) for e in ingredients])
            _conn.commit()
            return recipe_id
        except Exception as e:
            _conn.rollback()
            raise e

    @staticmethod
    def update_recipe(recipe_id, title, author_id, prep_time=None, cook_time=None, directions="", ingredients=[]):
        _conn = Db.get_session()
        try:
            cur = _conn.cursor()
            cur.execute("SELECT author FROM recipes WHERE id = %s;", (recipe_id,))
            author_recipe_id = cur.fetchone()[0]
            if author_recipe_id != author_id:
                raise Exception("Not your recipe")
            cur.execute("UPDATE recipes SET title = %s, prep_time = %s, cook_time = %s, directions = %s WHERE id = %s;",
                        (title, prep_time, cook_time, directions, recipe_id))
            cur.execute("SELECT id FROM ingredients WHERE recipe = %s;", (recipe_id,))
            extant_ingredients = cur.fetchall()
            for (new, ext) in zip_longest(ingredients, extant_ingredients):
                if new == None:
                    cur.execute("DELETE FROM ingredients WHERE id = %s;", ext)
                elif ext == None:
                    cur.execute("INSERT INTO ingredients (name, quantity, recipe) VALUES (%s, %s, %s);",
                                (new["name"], new.get("quantity", ""), recipe_id))
                else:
                    cur.execute("UPDATE ingredients SET name = %s, quantity = %s WHERE id = %s",
                                (new["name"], new.get("quantity", ""), ext[0]))
            _conn.commit()
            return recipe_id
        except Exception as e:
            _conn.rollback()
            raise e

    @staticmethod
    def select_by_id_and_author(id, author_id):
        _conn = Db.get_session()
        cur = _conn.cursor()
        cur.execute("""
            SELECT * FROM recipes WHERE id = %s AND author = %s
            """, (id, author_id))
        return cur.fetchone()

    @staticmethod
    def delete_by_id(id):
        try:
            _conn = Db.get_session()
            cur = _conn.cursor()
            cur.execute("""
                    DELETE FROM recipes WHERE id = %s
                    """, (id,))
            _conn.commit()
            return None
        except Exception as e:
            _conn.rollback()
            raise e

    @staticmethod
    def update_image_by_id(image, recipe_id):
        try:
            _conn = Db.get_session()
            cur = _conn.cursor()
            cur.execute("UPDATE recipes SET image = %s WHERE id = %s;", (image, recipe_id))
            _conn.commit()
            return None
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

    @staticmethod
    def delete_by_id(recipe_id, tag_id):
        _conn = Db.get_session()
        try:
            cur = _conn.cursor()
            cur.execute("""
                    DELETE FROM recipe_tags WHERE 
                    recipe = %s AND tag = %s
                    """, (recipe_id, tag_id))
            _conn.commit()
            return None
        except Exception as e:
            _conn.rollback()
            raise e


class IngredientRepo:

    @staticmethod
    def select_by_recipe(recipe_id, user_id=None):
        _conn = Db.get_session()
        cur = _conn.cursor()
        if user_id:
            cur.execute("""
                SELECT ingredients.*,
                EXISTS(
                    SELECT id FROM shopping_items
                    WHERE ingredients.id = shopping_items.ingredient
                    AND shopping_items.account = %s)
                FROM ingredients 
                WHERE ingredients.recipe = %s;
                """, (user_id, recipe_id))
        else:
            cur.execute("""
                SELECT *, FALSE FROM ingredients
                WHERE recipe = %s;
                """, (recipe_id,))
        return cur.fetchall()

    @staticmethod
    def select_name_quantity_by_id(id):
        _conn = Db.get_session()
        cur = _conn.cursor()

        cur.execute("""
            SELECT name, quantity FROM ingredients
            WHERE id = %s
            """, (id,))
        return cur.fetchone()

    @staticmethod
    def insert_row(name, quantity, recipe):
        _conn = Db.get_session()
        try:
            cur = _conn.cursor()
            cur.execute("""
                INSERT INTO ingredients
                VALUES (DEFAULT, %s, %s, %s) RETURNING id
                """, (name, quantity, recipe))
            _conn.commit()
            return cur.fetchone()[0]
        except Exception as e:
            _conn.rollback()
            raise e


class LikeRepo:
    @staticmethod
    def did_user_like(recipe_id, user_id):
        _conn = Db.get_session()
        cur = _conn.cursor()
        cur.execute("SELECT liker FROM liked_recipes WHERE liker = %s AND recipe = %s;", (user_id, recipe_id))
        return cur.fetchone() is not None

    @staticmethod
    def select_all_recipes_liked_by_liker_id(liker_id):
        _conn = Db.get_session()
        cur = _conn.cursor()
        cur.execute("SELECT recipe FROM liked_recipes WHERE liker = %s;", (liker_id,))
        return cur.fetchall()

    @staticmethod
    def like_recipe(recipe_id, user_id):
        _conn = Db.get_session()
        try:
            cur = _conn.cursor()
            cur.execute("INSERT INTO liked_recipes (liker, recipe) VALUES (%s, %s) RETURNING liker",
                        (user_id, recipe_id))
            _conn.commit()
            return cur.fetchone()[0]
        except Exception as e:
            _conn.rollback()
            raise e

    @staticmethod
    def unlike_recipe(recipe_id, user_id):
        _conn = Db.get_session()
        try:
            cur = _conn.cursor()
            cur.execute("DELETE FROM liked_recipes WHERE liker = %s AND recipe = %s RETURNING liker;",
                        (user_id, recipe_id))

            _conn.commit()
            return cur.fetchone()[0]
        except Exception as e:
            _conn.rollback()
            raise e


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


class ShoppingItemsRepo:

    @staticmethod
    def select_ingredient_by_account(account_id):
        _conn = Db.get_session()
        cur = _conn.cursor()

        cur.execute("""
            SELECT name, quantity FROM ingredients LEFT JOIN 
            shopping_items ON ingredients.id=shopping_items.ingredient 
            WHERE shopping_items.account = %s;
            """, (account_id,))
        return cur.fetchall()

    @staticmethod
    def insert_row(account, ingredient):
        _conn = Db.get_session()
        try:
            cur = _conn.cursor()
            cur.execute("""
                INSERT INTO shopping_items
                VALUES (%s, %s)
                """, (account, ingredient))
            _conn.commit()
        except Exception as e:
            _conn.rollback()
            raise e

    @staticmethod
    def delete_by_id(ingredient,account):
        _conn = Db.get_session()
        try:
            cur = _conn.cursor()
            cur.execute("""
                        DELETE FROM shopping_items WHERE ingredient = %s AND account = %s
                        """, (ingredient, account))
            rowcount = cur.rowcount
            _conn.commit()
            cur.close()
            return rowcount

        except Exception as e:
            _conn.rollback()
            raise e


class FollowersRepo:

    @staticmethod
    def insert_row(account, follower):
        _conn = Db.get_session()
        try:
            cur = _conn.cursor()
            cur.execute("""
                INSERT INTO followers
                VALUES (%s, %s) RETURNING account
                """, (account, follower))
            _conn.commit()
            return cur.fetchone()[0]
        except Exception as e:
            _conn.rollback()
            raise e

    @staticmethod
    def delete_by_id(account, follower):
        _conn = Db.get_session()
        try:
            cur = _conn.cursor()
            cur.execute("""
                    DELETE FROM followers WHERE account = %s AND follower = %s
                    """, (account, follower))
            _conn.commit()
            return None
        except Exception as e:
            _conn.rollback()
            raise e

    @staticmethod
    def select_by_id(account, follower):
        _conn = Db.get_session()
        cur = _conn.cursor()
        cur.execute("""
                SELECT * FROM followers WHERE account = %s AND follower = %s
                """, (account, follower))
        return cur.fetchone()
