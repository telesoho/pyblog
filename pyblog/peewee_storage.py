# coding:utf-8
"""
peewee数据库定义

![peewee官方文档](http://docs.peewee-orm.com/en/latest/peewee/models.html)
"""
from datetime import datetime
import os
from flask import current_app as app
from peewee import CharField, DateTimeField, Model, Proxy, TextField, SqliteDatabase
from telesoho.utils import DateTime

DATABASE_PROXY = Proxy()  # Create a proxy for our db.

class MyBaseModel(Model):
    """
    数据库Model基类
    """

    def set_data(self, item):
        """
        Set data by dict
        """
        for k in item:
            if k in self.props():
                setattr(self, k, item[k])

    def get_data(self):
        """
        Get a copy of data
        """
        return self._data.copy()

    @classmethod
    def props(cls):
        """
        Get all model properties
        """
        return [i for i in cls.__dict__ if i[:1] != '_']

    class Meta(object):
        """
        Meta
        """
        database = DATABASE_PROXY  # Use proxy for our DB.


class Post(MyBaseModel):
    """
    文章
    """
    cover = CharField(help_text=u"封面图片链接", null=True)
    title = CharField(help_text=u"标题", null=True)
    author = CharField(null=True, default="", max_length=100, help_text=u"作者")
    post_date = DateTimeField(index=True, default=datetime.now, help_text=u"文章提交日期")
    last_modified_date = DateTimeField(index=True, default=datetime.now, help_text=u'文章最后修改时间')
    content = TextField(help_text=u"文章内容")


def resetdb():
    """
    初始化数据库
    """
    database_file = app.config['DATABASE']
    if os.path.isfile(database_file):
        # 备份原数据库
        newfile = "{}.{}".format(
            database_file, DateTime(datetime.now()).timestamp())
        os.rename(
            database_file,
            newfile
        )
        print("Old database has beed backup to:%s" % newfile)

    database = SqliteDatabase(database_file)
    database.connect()

    # Configure our proxy to use the db we specified in config.
    DATABASE_PROXY.initialize(database)

    # with Using(database, [Data]):
    #     # Query is executed against the read replica.
    #     Data.get(Data.value == 5)

    #     # Since we did not specify this model in the list of overrides
    #     # it will use whatever database it was defined with.
    #     SomeOtherModel.get(SomeOtherModel.field == 3)
    database.create_tables([Post], True)
    database.close()
