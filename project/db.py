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

