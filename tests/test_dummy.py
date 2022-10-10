# XXX: Just a file to trick pytest into thinking that there are tests
#      Will need to go once there are real tests

import project

def test_home(client):
    assert client.get("/").status_code == 200

def test_1(db_session):
    cur = db_session.cursor()
    cur.execute("""
        INSERT INTO dummy
        VALUES (DEFAULT, 'Abcd1234')
    """)
    db_session.commit()

    cur = db_session.cursor()
    data = cur.execute("""
        SELECT * FROM dummy
    """).fetchone()
    assert data[1] == 'Abcd1234'

def test_2(db_session):
    cur = db_session.cursor()
    data = cur.execute("""
        SELECT * FROM dummy
    """).fetchone()
    assert data is None

