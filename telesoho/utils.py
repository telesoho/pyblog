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

    * A millisecond is converted to 1000 microseconds.
    * A minute is converted to 60 seconds.
    * An hour is converted to 3600 seconds.
    * A week is converted to 7 days.

    """
    __date_time = datetime.min

    def __init__(self, date_time=datetime.min):
        """
        dt = DateTime(datetime.now())
        """
        assert isinstance(date_time, datetime)
        self.__date_time = date_time

    @staticmethod
    def utc(date_time):
        """
        Return the datetime with tzinfo=UTC

        Coordinated Universal Time (UTC)
        """
        if isinstance(date_time, datetime):
            if date_time.tzinfo:
                return date_time.astimezone(tz.gettz("UTC"))
            else:
                return date_time.replace(tzinfo=tz.gettz("UTC"))
        else:
            raise ValueError("parameter is not a datetime object.")

    def get_datetime(self):
        """
        Return the datetime has been set.
        """
        return self.__date_time

    def timestamp(self, epoch=tz.EPOCH):
        """
        The Unix epoch (or Unix time or POSIX time or Unix timestamp) is
        the number of seconds that have elapsed since January 1, 1970 (midnight UTC/GMT),
        not counting leap seconds (in ISO 8601: 1970-01-01T00:00:00Z)
        """
        return timedelta.total_seconds(
            DateTime.utc(self.__date_time) - DateTime.utc(epoch))

    def microseconds(self, epoch=tz.EPOCH):
        """
        取得从EPOCH开始的微秒数(单位：μs)
        """
        return self.timestamp(epoch) * 1000000



    def set_datetime(self, date_time):
        """
        设置datetime
        """
        self.__date_time = date_time


    @staticmethod
    def from_microseconds(microseconds, epoch=tz.EPOCH):
        """
        通过微秒microseconds创建DateTime对象
        """
        if isinstance(microseconds, (int, float, long)):
            return DateTime(epoch + timedelta(microseconds=microseconds))
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
