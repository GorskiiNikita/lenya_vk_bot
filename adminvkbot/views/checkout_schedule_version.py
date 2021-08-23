from flask import session, redirect, url_for, request
from mongodb_api import mongo_client


def checkout():
    if 'username' not in session:
        return redirect(url_for('login_page'))

    form_data = dict(request.form)
    action = form_data.get('action')

    if action == 'new' and form_data.get('new-version'):
        mongo_client.checkout_schedule_version(form_data.get('new-version'))
    elif action == 'exist':
        mongo_client.checkout_schedule_version(form_data.get('schedule-versions'))
    elif action == 'copy':
        mongo_client.checkout_schedule_version(form_data.get('new-version'), form_data.get('schedule-versions'))

    return redirect(url_for('index_page'))
