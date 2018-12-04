"""
Set of unit tests for elastic_search.py
"""
import time

from elasticsearch_query import ElasticsearchQuery


def test_indexes():
    es_query = ElasticsearchQuery(es_host='foo')
    assert es_query._index.startswith('logstash-')


def test_indexes_prefix():
    es_query = ElasticsearchQuery(es_host='foo', index_prefix='syslog-ng')
    assert es_query._index.startswith('syslog-ng-')


def test_indexes_prefix_with_separator():
    es_query = ElasticsearchQuery(es_host='foo', index_prefix='syslog-ng', index_sep="_")
    assert es_query._index.startswith('syslog-ng_')
    assert ',syslog-ng_' in es_query._index


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
    es_query = ElasticsearchQuery('foo.host.net', since, period)

    assert es_query._since == expected_since
    assert es_query.get_to_timestamp() == expected_to


def test_get_timestamp_filer():
    es_query = ElasticsearchQuery(es_host='foo', since=123456, period=60)
    res = es_query._get_timestamp_filer()

    print(res)

    assert res['range']['@timestamp'] is not None
    assert res['range']['@timestamp']['gte'] == '1970-01-02T10:17:37.000Z'
    assert res['range']['@timestamp']['lte'] is not None
