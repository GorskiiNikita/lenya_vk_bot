from flask import session, redirect, url_for, request
from mongodb_api import mongo_client


def on_off():
    if 'username' not in session:
        return redirect(url_for('login_page'))

    form_data = dict(request.form)

    if form_data.get('turn') == 'on':
        mongo_client.enable_schedule()
    else:
        mongo_client.disable_schedule()

    return redirect(url_for('index_page'))
