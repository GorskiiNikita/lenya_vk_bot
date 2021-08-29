from flask import render_template, session, redirect, url_for, request
from mongodb_api import mongo_client


WEEKDAYS = [('1', 'Понедельник'),
            ('2', 'Вторник'),
            ('3', 'Среда'),
            ('4', 'Четверг'),
            ('5', 'Пятница'),
            ('6', 'Суббота')]

REVERSE_WEEKDAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
LESSONS = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh']

LESSONS_TIME = (('1', '9:00 - 10:30'),
                ('2', '10:45 - 12:15'),
                ('3', '12:55 - 14:25'),
                ('4', '14:40 - 16:10'),
                ('5', '16:25 - 17:55'),
                ('6', '18:00 - 19:30'),
                ('7', '19:40 - 21:10'))


def update_group(key):
    if 'username' not in session:
        return redirect(url_for('login_page'))
    if request.method == 'GET':
        group_data = mongo_client.get_group(key)
        resp = {}
        for i in range(6):
            for j in range(7):
                if group_data[REVERSE_WEEKDAYS[i]][LESSONS[j]] is None:
                    resp[f'{i+1}_{j+1}_numerator'] = ''
                    resp[f'{i + 1}_{j + 1}_denumerator'] = ''
                    resp[f'{i + 1}_{j + 1}_wherenumerator'] = ''
                    resp[f'{i + 1}_{j + 1}_wheredenumerator'] = ''
                    resp[f'{i + 1}_{j + 1}_teachernumerator'] = ''
                    resp[f'{i + 1}_{j + 1}_teacherdenumerator'] = ''

                    continue

                if group_data[REVERSE_WEEKDAYS[i]][LESSONS[j]][0] is None:
                    resp[f'{i + 1}_{j + 1}_numerator'] = ''
                    resp[f'{i + 1}_{j + 1}_wherenumerator'] = ''
                    resp[f'{i + 1}_{j + 1}_teachernumerator'] = ''
                else:
                    resp[f'{i + 1}_{j + 1}_numerator'] = group_data[REVERSE_WEEKDAYS[i]][LESSONS[j]][0]['name']
                    resp[f'{i + 1}_{j + 1}_wherenumerator'] = group_data[REVERSE_WEEKDAYS[i]][LESSONS[j]][0]['where']
                    resp[f'{i + 1}_{j + 1}_teachernumerator'] = group_data[REVERSE_WEEKDAYS[i]][LESSONS[j]][0]['teacher']

                if group_data[REVERSE_WEEKDAYS[i]][LESSONS[j]][1] is None:
                    resp[f'{i + 1}_{j + 1}_denumerator'] = ''
                    resp[f'{i + 1}_{j + 1}_wheredenumerator'] = ''
                    resp[f'{i + 1}_{j + 1}_teacherdenumerator'] = ''
                else:
                    resp[f'{i + 1}_{j + 1}_denumerator'] = group_data[REVERSE_WEEKDAYS[i]][LESSONS[j]][1]['name']
                    resp[f'{i + 1}_{j + 1}_wheredenumerator'] = group_data[REVERSE_WEEKDAYS[i]][LESSONS[j]][1]['where']
                    resp[f'{i + 1}_{j + 1}_teacherdenumerator'] = group_data[REVERSE_WEEKDAYS[i]][LESSONS[j]][1]['teacher']

        return render_template('update_page.html', weekdays=WEEKDAYS, lessons=LESSONS_TIME, data=resp, group_id=key)

    group_data = dict(request.form)
    entry = {'_id': key,
             'monday': {
                 'first': None,
                 'second': None,
                 'third': None,
                 'fourth': None,
                 'fifth': None,
                 'sixth': None,
                 'seventh': None
             },
             'tuesday': {
                 'first': None,
                 'second': None,
                 'third': None,
                 'fourth': None,
                 'fifth': None,
                 'sixth': None,
                 'seventh': None
             },
             'wednesday': {
                 'first': None,
                 'second': None,
                 'third': None,
                 'fourth': None,
                 'fifth': None,
                 'sixth': None,
                 'seventh': None
             },
             'thursday': {
                 'first': None,
                 'second': None,
                 'third': None,
                 'fourth': None,
                 'fifth': None,
                 'sixth': None,
                 'seventh': None
             },
             'friday': {
                 'first': None,
                 'second': None,
                 'third': None,
                 'fourth': None,
                 'fifth': None,
                 'sixth': None,
                 'seventh': None
             },
             'saturday': {
                 'first': None,
                 'second': None,
                 'third': None,
                 'fourth': None,
                 'fifth': None,
                 'sixth': None,
                 'seventh': None
             }
    }

    for i in range(0, 6):
        for j in range(0, 5):
            numerator = group_data[f'{i + 1}_{j + 1}_numerator'].strip()
            denumerator = group_data[f'{i + 1}_{j + 1}_denumerator'].strip()
            if numerator == '' and denumerator == '':
                continue
            elif numerator != '' and denumerator == '':
                entry[REVERSE_WEEKDAYS[i]][LESSONS[j]] = [
                    {'name': numerator,
                     'where': group_data[f'{i + 1}_{j + 1}_wherenumerator'],
                     'teacher': group_data[f'{i + 1}_{j + 1}_teachernumerator']},
                    None]
            elif numerator == '' and denumerator != '':
                entry[REVERSE_WEEKDAYS[i]][LESSONS[j]] = [None,
                                                          {'name': denumerator,
                                                           'where': group_data[f'{i + 1}_{j + 1}_wheredenumerator'],
                                                           'teacher': group_data[f'{i + 1}_{j + 1}_teacherdenumerator']}]
            else:
                entry[REVERSE_WEEKDAYS[i]][LESSONS[j]] = [
                    {'name': numerator,
                     'where': group_data[f'{i + 1}_{j + 1}_wherenumerator'],
                     'teacher': group_data[f'{i + 1}_{j + 1}_teachernumerator']},
                    {'name': denumerator,
                     'where': group_data[f'{i + 1}_{j + 1}_wheredenumerator'],
                     'teacher': group_data[f'{i + 1}_{j + 1}_teacherdenumerator']}]

    mongo_client.update_group(key, entry)
    return redirect(url_for('index_page'))
