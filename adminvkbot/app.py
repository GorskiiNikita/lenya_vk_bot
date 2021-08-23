# -*- coding: utf-8 -*-
from flask import Flask
from views import login_page, index_page, logout, add_page, delete_group, update_group, change_texts, send, checkout, on_off


app = Flask(__name__)
app.secret_key = 'A0Z/3yX RXHH!]LWX/,?RT'


app.add_url_rule('/', view_func=index_page)
app.add_url_rule('/logout', view_func=logout)
app.add_url_rule('/login', view_func=login_page, methods=['GET', 'POST'])
app.add_url_rule('/add', view_func=add_page, methods=['GET', 'POST'])
app.add_url_rule('/update/<key>', view_func=update_group, methods=['GET', 'POST'])
app.add_url_rule('/delete/<key>', view_func=delete_group)
app.add_url_rule('/change_texts', view_func=change_texts, methods=['GET', 'POST'])
app.add_url_rule('/mass_sending', view_func=send, methods=['GET', 'POST'])
app.add_url_rule('/checkout', view_func=checkout, methods=['POST'])
app.add_url_rule('/schedule_on_off', view_func=on_off, methods=['POST'])


if __name__ == '__main__':
    app.run()
