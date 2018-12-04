"""
Set of unit tests for kibana.py
"""
import time

from elasticsearch_query import ElasticsearchQuery


def test_indexes():
    instance = ElasticsearchQuery()
    assert instance._index.startswith('logstash-')


def test_indexes_prefix():
    instance = ElasticsearchQuery(index_prefix='syslog-ng')
    assert instance._index.startswith('syslog-ng-')


def test_indexes_prefix_with_separator():
    instance = ElasticsearchQuery(index_prefix='syslog-ng', index_sep="_")
    assert instance._index.startswith('syslog-ng_')
    assert ',syslog-ng_' in instance._index


def test_format_index():
    assert ElasticsearchQuery.format_index(prefix='logstash', timestamp=1) == 'logstash-1970.01.01'
    assert ElasticsearchQuery.format_index(prefix='logstash', timestamp=1408450795) == 'logstash-2014.08.19'
    assert ElasticsearchQuery.format_index(prefix='logstash-foo', timestamp=1408450795) == 'logstash-foo-2014.08.19'
    assert ElasticsearchQuery.format_index(prefix='syslog-ng', timestamp=1408450795, sep="_") == 'syslog-ng_2014.08.19'


def test_time():
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
        check_time(**case)


def check_time(since, expected_since, expected_to, period):
    instance = ElasticsearchQuery(since, period)

    assert instance._since == expected_since
    assert instance.get_to_timestamp() == expected_to


def test_get_timestamp_filer():
    instance = ElasticsearchQuery(123456, 60)
    res = instance._get_timestamp_filer()

    print(res)

    assert res['range']['@timestamp'] is not None
    assert res['range']['@timestamp']['gte'] == '1970-01-02T10:17:37.000Z'
    assert res['range']['@timestamp']['lte'] is not None
