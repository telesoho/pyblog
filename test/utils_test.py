import unittest

from datetime import datetime, timedelta
from dateutil import tz
from telesoho.utils import JSON, DateTime



class TestUtilsMethods(unittest.TestCase):
    """
    Test utils class
    """

    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        pass

    def test_json_pprint_s(self):
        """
        test JSON.pprint_s
        """
        test_dict = {
            "v1":"abc",
            "v2":"efg",
            "obj":(1, 2),
            "plist":[3, 4],
            'date': datetime(2010, 1, 1, 1, 1, 1, 100)
        }
        ret = """{
    "date": "2010-01-01T01:01:01.000100", 
    "obj": [
        1, 
        2
    ], 
    "plist": [
        3, 
        4
    ], 
    "v1": "abc", 
    "v2": "efg"
}"""
        self.assertTrue(JSON.pprint_s(test_dict) == ret)


    def test_timestemp(self):
        """ Test Time class
        """
        uct_datetime = DateTime(
            datetime(
                2010, 1, 1, hour=1, minute=1, second=1, microsecond=1235, tzinfo=tz.gettz('UTC')
            )
        )

        jst_datetime = DateTime(
            datetime(
                2010, 1, 1, 1, 1, 1, 1235, tzinfo=tz.gettz('Asia/Tokyo')
            )
        )

        self.assertNotEqual(uct_datetime, jst_datetime)

        self.assertTrue(uct_datetime.timestamp() > jst_datetime.timestamp())

        self.assertTrue(uct_datetime.timestamp_us > jst_datetime.timestamp_us())

        self.assertTrue(uct_datetime.timestamp(epoch=uct_datetime.get_datetime()) == 0)

        self.assertTrue(
            (DateTime.from_timestamp(
                uct_datetime.timestamp()).timestamp() == uct_datetime.timestamp())
        )

        self.assertTrue(
            (DateTime.from_timestamp_us(
                uct_datetime.timestamp_us()).timestamp_us() == uct_datetime.timestamp_us())
        )


    def test_timezone(self):
        native_dt = datetime(2012, 1, 1)
        uct_dt = native_dt.replace(tzinfo=tz.gettz('UCT'))
        jst_dt = datetime(2012, 1, 1, tzinfo=tz.gettz('Asia/Tokyo'))

        print native_dt
        print uct_dt
        print jst_dt
        print jst_dt.astimezone(tz.gettz('UCT'))


    def tearDown(self):
        "Hook method for deconstructing the test fixture after testing it."
        pass

if __name__ == '__main__':
    unittest.main()
