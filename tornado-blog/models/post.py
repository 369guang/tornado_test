# -*- coding: utf-8 -*-

import datetime
import sys
import json
import os
from peewee import *
from playhouse.shortcuts import RetryOperationalError
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
import webconfig


class RetryMySQLDatabase(RetryOperationalError, MySQLDatabase):
    pass

db = MySQLDatabase(
    webconfig.getConfig('db', 'database'),
    host=webconfig.getConfig('db', 'host'),
    user=webconfig.getConfig('db', 'user'),
    passwd=webconfig.getConfig('db', 'passwd'),
    port=int(webconfig.getConfig('db', 'port')),
    charset='utf8'
)


class BaseModel(Model):

    class Meta:
        database = db

    @classmethod
    def getOne(cls, *query, **kwargs):
        try:
            return cls.get(*query, **kwargs)
        except DoesNotExist:
            return None

    def __str__(self):
        r = {}
        for k in self._data.keys():
            try:
                r[k] = str(getattr(self, k))
            except:
                r[k] = json.dumps(getattr(self, k))
        return str(r)


class Admin(BaseModel):
    '''
    admin user
    '''
    id = PrimaryKeyField()
    username = CharField(null=True, max_length=100)
    password = CharField(null=False, max_length=256)
    status = CharField(null=False, default='enable')
    email = CharField(null=False, max_length=50)
    description = TextField(null=True)
    last_login_ip = CharField()
    last_login_time = DateTimeField(formats='%Y-%m-%d %H:%M:%S')
    update_time = DateTimeField(
        default=datetime.datetime.now, formats='%Y-%m-%d %H:%M:%S')

    class Meta:
        db_table = 'users'
        order_by = ('-id',)


class Post(BaseModel):
    '''
    blog 
    '''
    id = PrimaryKeyField()
    title = CharField(null=True, max_length=256)
    content = TextField(null=True)
    update_time = DateTimeField(
        default=datetime.datetime.now, formats='%Y-%m-%d %H:%M:%S')
    create_time = DateTimeField(
        default=datetime.datetime.now, formats='%Y-%m-%d %H:%M:%S')

    class Meta:
        db_table = 'post'
        order_by = ('-id',)


class DatabaseManager(object):
    '''
    database ctrl
    '''

    def __init__(self):
        self.tables = [Admin, Post]

    def initial(self):
        print "正在连接数据库"
        db.connect()
        print "连接成功"
        print "正在初始化数据库"
        db.create_tables(self.tables, safe=True)
        Admin.create(username='admin', password='admin', last_login_ip='127.0.0.1',
                     status='enable', last_login_time=datetime.datetime.now(), update_time=datetime.datetime.now())
        Admin.create(username='guest', password='guest', last_login_ip='127.0.0.1',
                     status='enable', last_login_time=datetime.datetime.now(), update_time=datetime.datetime.now())
        print "数据库初始完成"

    def start_check(self):
        '''
        start check
        '''
        pass

    def db_check(self):
        try:
            if len(db.get_tables()) == 0:
                return False
            else:
                return True
        except Exception as ex:
            print ex
            sys.exit()


if __name__ == '__main__':
    dbmg = DatabaseManager()
    dbmg.initial()
