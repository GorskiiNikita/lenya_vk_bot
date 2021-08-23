from pymongo import MongoClient
from datetime import datetime

from settings import MONGO_CONFIG


class MongoApi:

    def __init__(self):
        self.client = MongoClient(MONGO_CONFIG['HOST'])
        self.db = self.client.botdb

    def get_list_of_groups(self):
        groups = []
        for group in self.db.groups.find():
            groups.append(group['_id'])
        return groups

    def get_users(self):
        users = []
        for user in self.db.users.find():
            users.append(user['_id'])
        return users

    def add_group(self, group):
        self.db.groups.insert_one(group)

    def delete_group(self, group_id):
        self.db.groups.remove({'_id': group_id})

    def get_group(self, group_id):
        return self.db.groups.find_one({'_id': group_id})

    def update_group(self, group_id, data):
        self.db.groups.update_one({
            '_id': group_id
        }, {
            '$set': data
        }, upsert=False)

    def get_texts(self):
        texts = []
        for text in self.db.texts.find():
            texts.append(text)
        return texts

    def update_texts(self, texts):
        for key in texts.keys():
            self.db.texts.update_one({
                '_id': key
            }, {
                '$set': {'text': texts[key]}
            }, upsert=False)

    def update_time_texts(self):
        now = int(datetime.now().timestamp())
        self.db.times.update_one({
            '_id': 'last_update_texts'
        }, {
            '$set': {'timestamp': now}
        }, upsert=False)

    def update_time_groups(self):
        now = int(datetime.now().timestamp())
        self.db.times.update_one({
            '_id': 'last_update_groups'
        }, {
            '$set': {'timestamp': now}
        }, upsert=False)

    def checkout_schedule_version(self, new_version, original_version=None):
        version_exist = new_version in self.get_list_of_versions()
        old_version = self.get_current_schedule_version()
        self.update_current_schedule_version(new_version)
        old_schedule = [group for group in self.db.groups.find()]
        self.save_schedule_version(old_version, old_schedule)

        if version_exist:
            new_schedule = self.db.schedules.find_one({'_id': new_version})['schedule']
        elif original_version:
            new_schedule = self.db.schedules.find_one({'_id': original_version})['schedule']
            self.save_schedule_version(new_version, new_schedule)
        else:
            new_schedule = []
            self.save_schedule_version(new_version, new_schedule)

        self.db.groups.drop()

        if new_schedule:
            self.db.groups.insert_many(new_schedule)
        self.update_time_groups()

    def save_schedule_version(self, version, schedule):
        self.db.schedules.remove({'_id': version})
        self.db.schedules.insert_one({'_id': version, 'schedule': schedule})

    def get_current_schedule_version(self):
        return self.db.settings.find_one({'_id': 'main'})['current_schedule_version']

    def update_current_schedule_version(self, version):
        self.db.settings.update_one({
            '_id': 'main'
        }, {
            '$set': {'current_schedule_version': version}
        }, upsert=False)

    def get_list_of_versions(self):
        return [schedule['_id'] for schedule in self.db.schedules.find()]

    def get_schedule_status(self):
        return self.db.settings.find_one({'_id': 'main'})['schedule_enabled']

    def disable_schedule(self):
        self.db.settings.update_one({
            '_id': 'main'
        }, {
            '$set': {'schedule_enabled': False}
        }, upsert=False)

    def enable_schedule(self):
        self.db.settings.update_one({
            '_id': 'main'
        }, {
            '$set': {'schedule_enabled': True}
        }, upsert=False)


mongo_client = MongoApi()
