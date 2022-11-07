""" Change account password """

import json
from flask import session
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
    parsers
)

from project.db import AccountRepo
from project.account import db_save_account, search_account_by_name

@scenario('features/Change_account_password.feature',
          'Successfully update password (Normal Flow)')
def test_success_case(app):
    pass

@scenario('features/Change_account_password.feature',
          'Problematic cases (Error Flow)')
def test_erroneous_case(app):
    pass

@scenario('features/Change_account_password.feature',
          'Idempotent update (Alternate Flow)')
def test_idempotent_case(app):
    pass

@scenario('features/Change_account_password.feature',
          'Unauthorized attempt (Error Flow)')
def test_unauth_case(app):
    pass

@given(parsers.parse('the following account is in the system:{table}'))
def add_accounts_to_system(table):
    table = json.loads(table)[1:]
    for (name, email, password) in table:
        db_save_account(name, email, password)

@given(parsers.parse('User "{name}" is logged in'), target_fixture="info")
def log_me_in(client, name):
    info = search_account_by_name(name)
    with client.session_transaction() as session:
        session['id'] = info[0]
    return info

@given(parsers.parse('User "{name}" is not logged in'), target_fixture="info")
def dont_log_me_in(name):
    # still need to query the user even if we don't need to login
    info = search_account_by_name(name)
    return info

@given(parsers.re('a current password "(?P<curpass>.*)"'), target_fixture="curpass")
def select_current_password(curpass):
    return curpass

@given(parsers.re('a new password "(?P<newpass>.*)"'), target_fixture="newpass")
def select_new_password(newpass):
    return newpass

@given(parsers.re('a confirm password "(?P<chkpass>.*)"'), target_fixture="chkpass")
def select_confirm_password(chkpass):
    return chkpass

@when('I request to update my password', target_fixture="response")
def submit_the_form(client, curpass, newpass, chkpass):
    response = client.post("/setting", data={
        "current_passwd": curpass,
        "new_passwd": newpass,
        "confirm_passwd": chkpass
    }, follow_redirects=True)
    return response

@then('the operation succeeds')
def check_success(response):
    assert response.status_code == 200

@then('I should get redirected to login')
def check_redirect(response):
    assert response.request.path == "/login"

@then(parsers.parse('I should get the error message "{errmsg}"'))
def check_error_message(response, errmsg):
    assert bytes(errmsg, 'utf-8') in response.data

@then('my password is changed')
def check_changed(client, newpass, info):
    client.get("/logout")
    response = client.post("/login", data={
        "email": info[2],
        "password": newpass
    }, follow_redirects=True)
    assert response.request.path == "/profile"

@then(parsers.parse('my password stays as "{password}"'))
def check_exact_password(client, password, info):
    check_changed(client, password, info)
