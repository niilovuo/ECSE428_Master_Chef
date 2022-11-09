""" Search account name """

import json
import pytest
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
    parsers
)

@scenario('features/Search_account_name.feature',
          'Search by exact name (Normal Flow)')
def test_by_exact_match(app):
    pass

@scenario('features/Search_account_name.feature',
          'Search by matching (Alternate Flow)')
def test_by_partial_match(app):
    pass

@scenario('features/Search_account_name.feature',
          'List first page (Alternate Flow)')
def test_list_first_page(app):
    pass

@scenario('features/Search_account_name.feature',
          'List second page (Alternate Flow)')
def test_list_second_page(app):
    pass

@scenario('features/Search_account_name.feature',
          'Search with blanks (Error Flow)')
def test_by_blank_pattern(app):
    pass

@given(parsers.parse('the following users in the system:\n{table}'))
def setup_users(table, postgresql):
    table = json.loads(table)
    cur = postgresql.cursor()
    for name in table:
        cur.execute("INSERT INTO accounts VALUES (DEFAULT, %s, %s, '', '')",
                    (name, name))

    postgresql.commit()

@given(parsers.re('the query string "(?P<query>.*)"'), target_fixture="query")
def pass_search_query(query):
    return query

@pytest.fixture
def start_page():
    return 0

@given(parsers.parse('start key {start:d}'), target_fixture="start_page")
def pass_start_page(start):
    return start

@when("a user requests to search for accounts", target_fixture="response")
def do_search(client, query, start_page):
    return client.get(f"/users?q={query}&start={start_page}")

@then(parsers.parse('the following list of accounts is returned:\n{table}'))
def check_response(table, response):
    table = json.loads(table)
    for name in table:
        assert bytes(f">{name}<", 'utf-8') in response.data
