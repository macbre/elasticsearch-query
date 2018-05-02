"""
Set of unit tests for kibana.py
"""
import time
import unittest

from wikia_common_kibana import Kibana


class KibanaTestClass(unittest.TestCase):
    """
    Unit tests for Kibana class
    """
    @staticmethod
    def test_indexes():
        instance = Kibana()
        assert instance._index.startswith('logstash-')

    @staticmethod
    def test_indexes_prefix():
        instance = Kibana(index_prefix='syslog-ng')
        assert instance._index.startswith('syslog-ng-')

    @staticmethod
    def test_indexes_prefix():
        instance = Kibana(index_prefix='syslog-ng', index_sep="_")
        assert instance._index.startswith('syslog-ng_')
        assert ',syslog-ng_' in instance._index

    @staticmethod
    def test_format_index():
        assert Kibana.format_index(prefix='logstash', timestamp=1) == 'logstash-1970.01.01'
        assert Kibana.format_index(prefix='logstash', timestamp=1408450795) == 'logstash-2014.08.19'
        assert Kibana.format_index(prefix='logstash-foo', timestamp=1408450795) == 'logstash-foo-2014.08.19'
        assert Kibana.format_index(prefix='syslog-ng', timestamp=1408450795, sep="_") == 'syslog-ng_2014.08.19'

    def test_time(self):
        now = int(time.time())

        cases = [
            # till now
            {
                "since": None,
                "expected_since": now - 60,
                "expected_to": now - 5,
                "period": 60
            },
            # strictly defined time period
            {
                "since": 12345,
                "expected_since": 12346,
                "expected_to": now - 5,
                "period": 600
            }
        ]

        for case in cases:
            self.check_time(**case)

    @staticmethod
    def check_time(since, expected_since, expected_to, period):
        instance = Kibana(since, period)

        assert instance._since == expected_since
        assert instance.get_to_timestamp() == expected_to

    @staticmethod
    def test_get_timestamp_filer():
        instance = Kibana(123456, 60)
        res = instance._get_timestamp_filer()

        print(res)

        assert res['range']['@timestamp'] is not None
        assert res['range']['@timestamp']['gte'] == '1970-01-02T10:17:37.000Z'
        assert res['range']['@timestamp']['lte'] is not None
