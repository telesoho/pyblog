# coding=utf-8
"""
实用类
"""
import json
from datetime import datetime, timedelta
import time
# see https://github.com/dateutil/dateutil
from dateutil import parser, tz


class JSON(object):
    """
    JSON操作类
    """

    @staticmethod
    def pprint_s(obj):
        """
        Return pretty-print a Python object string
        """
        json_str = JSON.dumps(obj, indent=4, sort_keys=True)
        return json_str

    @staticmethod
    def dumps(obj, **kwargs):
        """
        将对象转为JSON字符串,(支持日期格式)
        """
        default_params = {
            "default" : JSON._isoformat_handler,
        }
        merged_params = dict(kwargs, **default_params)
        return json.dumps(obj, **merged_params)

    @staticmethod
    def dump(obj, file_point, **kwargs):
        """
        将对象转为JSON字符串,(支持日期格式)
        """
        default_params = {
            "default" : JSON._isoformat_handler,
        }
        merged_params = dict(kwargs, **default_params)
        return json.dump(obj, file_point, **merged_params)

    @staticmethod
    def loads(obj, **kwargs):
        """
        加载JSON字符串
        """
        default_params = {
            # "default" : JSON._date_handler,
        }
        merged_params = dict(kwargs, **default_params)
        return json.loads(obj, **merged_params)


    @staticmethod
    def _isoformat_handler(obj):
        """
        isoformat handle
        """
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        else:
            raise TypeError



class DateTime(object):
    """
    DateTime class
    """
    __date_time = datetime.min

    @staticmethod
    def uct(date_time):
        """
        Return a specifed datetime to UCT datetime
        """
        if isinstance(date_time, datetime):
            if date_time.tzinfo:
                return date_time.astimezone(tz.gettz("UCT"))
            else:
                return date_time.replace(tzinfo=tz.gettz("UCT"))
        else:
            raise ValueError("parameter is not a datetime object.")

    def get_datetime(self):
        return self.__date_time

    def timestamp(self, epoch=tz.EPOCH):
        """
        取得timestamp, 秒为单位
        """
        return timedelta.total_seconds(
            DateTime.uct(self.__date_time) - DateTime.uct(epoch))

    def timestamp_us(self, epoch=tz.EPOCH):
        """
        取得timestamp, 微秒为单位
        """
        return self.timestamp(epoch) * 1000


    def __init__(self, date_time, parserinfo=None, **kwargs):
        """
        dt = DateTime("2012/12/2 12:12:12.232")
        dt = DateTime(datetime.now())
        """
        if isinstance(date_time, datetime):
            self.__date_time = date_time
        elif isinstance(date_time, (str, unicode)):
            try:
                date_time = parser.parse(str, parserinfo, **kwargs)
                self.__date_time = date_time.date()
            except ValueError:
                # parse failed
                self.__date_time = datetime.min
        elif isinstance(date_time, (int, float, long)):
            pass


    def set_datetime(self, date_time):
        """
        设置datetime
        """
        self.__date_time = date_time


    @staticmethod
    def current_milliseconds():
        """
        Get current milliseconds
        """
        return long(round(time.time() * 1000))

    @staticmethod
    def from_timestamp_us(timestamp_us, epoch=tz.EPOCH):
        """
        通过微秒timestamp_us创建DateTime对象
        """
        if isinstance(timestamp_us, (int, float, long)):
            return DateTime(epoch + timedelta(milliseconds=timestamp_us))
        else:
            raise ValueError

    @staticmethod
    def from_timestamp(timestamp, epoch=tz.EPOCH):
        """
        通过秒数timestamp创建DateTime对象
        """
        if isinstance(timestamp, (int, float, long)):
            return DateTime(epoch + timedelta(seconds=timestamp))
        else:
            raise ValueError
