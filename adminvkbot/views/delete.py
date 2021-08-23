from flask import session, redirect, url_for
from mongodb_api import mongo_client


def delete_group(key):
    if 'username' not in session:
        return redirect(url_for('login_page'))
    mongo_client.update_time_groups()
    mongo_client.delete_group(key)
    return redirect(url_for('index_page'))