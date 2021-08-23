from flask import session, redirect, url_for, request, render_template
from tasks import send_to_user
from mongodb_api import mongo_client


def send():
    if 'username' not in session:
        return redirect(url_for('login_page'))

    if request.method == 'GET':
        return render_template('mass_sender.html')

    message = request.form.get('message')

    users = mongo_client.get_users()

    for user in users:
        send_to_user.delay(message, user)

    return redirect(url_for('index_page'))
