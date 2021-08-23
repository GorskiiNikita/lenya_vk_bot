from flask import render_template, redirect, url_for, session
from mongodb_api import mongo_client


def index_page():
    if 'username' in session:
        list_of_groups = [group.upper() for group in mongo_client.get_list_of_groups()]
        list_of_versions = mongo_client.get_list_of_versions()
        list_of_versions.sort()
        cur_version_index = list_of_versions.index(mongo_client.get_current_schedule_version())
        list_of_versions[0], list_of_versions[cur_version_index] = list_of_versions[cur_version_index], list_of_versions[0]
        return render_template('index.html', groups=list_of_groups, schedule_versions=list_of_versions, schedule_enable=mongo_client.get_schedule_status())
    return redirect(url_for('login_page'))
