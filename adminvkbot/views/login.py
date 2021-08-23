from flask import render_template, request, redirect, url_for, session


def login_page():
    if request.method == 'GET':
        if 'username' in session:
            return redirect(url_for('index_page'))
        return render_template('login_page.html', invalid_auth=False)
    else:
        login = request.form.get('login')
        password = request.form.get('password')
        if login == 'admin' and password == 'qwerty':
            session['username'] = login
            return redirect(url_for('index_page'))
        else:
            return render_template('login_page.html', invalid_auth=True)


def logout():
    session.pop('username', None)
    return redirect(url_for('index_page'))

