from datetime import datetime, timedelta
from dateutil import tz
from telesoho.utils import JSON, DateTime



def test_timezone():
    native_dt = datetime(2012, 1, 1)
    uct_dt = native_dt.replace(tzinfo=tz.gettz('UTC'))
    jst_dt = datetime(2012, 1, 1, tzinfo=tz.gettz('Asia/Tokyo'))

    print "native_dt", native_dt
    print "uct_dt", uct_dt
    print "jst_dt", jst_dt
    print "jst_dt astimezone", jst_dt.astimezone(tz.gettz('UTC'))
    print "jst_dt replace", jst_dt.replace(tzinfo=tz.gettz('UTC'))


def test_timezone2():
        uct_datetime = DateTime(
            datetime(
                2010, 1, 1, hour=1, minute=1, second=1, microsecond=123456, tzinfo=tz.gettz('UTC')
            )
        )

        jst_datetime = DateTime(
            datetime(
                2010, 1, 1, 1, 1, 1, 123456, tzinfo=tz.gettz('Asia/Tokyo')
            )
        )

        print uct_datetime.get_datetime()
        print uct_datetime.timestamp()
        print DateTime.from_timestamp(uct_datetime.timestamp()).get_datetime()



if __name__ == '__main__':
    test_timezone2()