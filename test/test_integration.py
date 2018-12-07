"""
Set of integration tests. They're run on elasticsearch instance.

1. You need to ES_TEST_HOST environment variable when running tests to run them.
2. Files from fixtures/ directory will be enumerated and indices filled with data (one file per one index).
3. Enjoy.
"""
import time
from os import getenv, path, walk
from pytest import raises
from unittest import TestCase

import elasticsearch_query
import yaml

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError, RequestError

# useful for test failures debugging
import logging
logging.basicConfig(level=logging.DEBUG)


class ElasticsearchQuery(elasticsearch_query.ElasticsearchQuery):
    """
    ElasticsearchQuery sub-class that does not append timestamp to index names.
    Quite handy for tests.
    """
    @staticmethod
    def format_index(prefix, timestamp, sep='-'):
        return prefix


def set_up_fixtures(es_host):
    """
    :type es_host str
    """
    fixtures_directory = path.join(path.dirname(__file__), 'fixtures')

    for _, _, files in walk(fixtures_directory):
        for file in sorted(files):
            set_up_using_fixture_file(es_host, fixture_file=path.join(fixtures_directory, file))


def set_up_using_fixture_file(es_host, fixture_file):
    """
    :type es_host str
    :type fixture_file str
    """
    es = Elasticsearch(hosts=es_host)

    with open(fixture_file, 'rt') as handler:
        fixture = yaml.load(handler)

    index_name = fixture['index']
    entries = fixture.get('entries', [])

    # @see https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-create-index.html
    if es.indices.exists(index_name):
        es.indices.delete(index_name)

    es.indices.create(index_name)

    # fill with data
    # @see https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-index_.html
    # @see http://127.0.0.1:9200/app-logs,app-logs/_search

    # set @timestamp field 15 seconds in the past
    timestamp = ElasticsearchQuery.format_timestamp(int(time.time()) - 15)

    for entry in entries:
        entry['@timestamp'] = timestamp

        logging.info('%s: indexing %s', index_name, entry)
        es.index(index=index_name, doc_type='log', body=entry, refresh='wait_for')


class IntegrationTests(TestCase):
    EMPTY_INDEX_NAME = 'empty-index'  # see fixtures/00-empty-index.yml
    APP_LOGS_INDEX_NAME = 'app-logs'  # see fixtures/01-app-logs.yml

    @classmethod
    def setUpClass(cls):
        cls.es_test_host = getenv('ES_TEST_HOST')

        if cls.es_test_host:
            # setup indices data
            set_up_fixtures(cls.es_test_host)

    def setUp(self):
        if self.es_test_host is None:
            self.skipTest('You need to pass ES_TEST_HOST env variable to run it')

    def test_connect(self):
        es = Elasticsearch(hosts=self.es_test_host)
        info = es.info()

        print(info)
        assert info['tagline'] == 'You Know, for Search'

    def test_invalid_query(self):
        es_query = ElasticsearchQuery(es_host=self.es_test_host, index_prefix=self.EMPTY_INDEX_NAME)

        res = es_query.query_by_string('SELECT foo FROM bar')
        assert len(res) == 0, 'Result is an empty list'

    def test_get_rows(self):
        es_query = ElasticsearchQuery(es_host=self.es_test_host, index_prefix=self.APP_LOGS_INDEX_NAME)

        # @see https://www.elastic.co/guide/en/elasticsearch/reference/current/search.html#search-routing
        res = es_query.get_rows(match={'host': 'prod'})
        assert len(res) == 3, 'All entries are returned'
        assert str(res[0]['host']).endswith('.prod')

        res = es_query.get_rows(match={'host': 'app2'})
        assert len(res) == 1, 'Matching entries are returned'
        assert res[0]['host'] == 'app2.prod'

    def test_query(self):
        es_query = ElasticsearchQuery(es_host=self.es_test_host, index_prefix=self.APP_LOGS_INDEX_NAME)

        # @see https://www.elastic.co/guide/en/elasticsearch/reference/current/search.html#search-routing
        res = es_query.query_by_string('*')
        assert len(res) == 3, 'All entries are returned'

        res = es_query.query_by_string('host: "app2"')
        assert len(res) == 1, 'Matching entries are returned'
        assert res[0]['host'] == 'app2.prod'

    def test_query_with_fields(self):
        es_query = ElasticsearchQuery(es_host=self.es_test_host, index_prefix=self.APP_LOGS_INDEX_NAME)

        res = es_query.query_by_string('host: "app2"', fields=['host'])
        assert res == [{'host': 'app2.prod'}]

        res = es_query.query_by_string('host: "app2"', fields=['appname', 'host'])
        assert res == [{'appname': 'foo', 'host': 'app2.prod'}]

    def test_get_aggregations(self):
        es_query = ElasticsearchQuery(es_host=self.es_test_host, index_prefix=self.APP_LOGS_INDEX_NAME)

        res = es_query.get_aggregations(
            query='*', stats_field='time', group_by='appname.keyword')
        assert res == {'foo': {'count': 3, '50.0': 210.0, '95.0': 320.0, '99.0': 320.0, '99.9': 320.0}}

        res = es_query.get_aggregations(
            query='*', stats_field='time', group_by='appname.keyword', percents=(25, 50, 75))
        assert res == {'foo': {'count': 3, '25.0': 142.5, '50.0': 210.0, '75.0': 292.5}}

    def test_count(self):
        es_query = ElasticsearchQuery(es_host=self.es_test_host, index_prefix=self.APP_LOGS_INDEX_NAME)

        assert es_query.count(query='*') == 3
        assert es_query.count(query='host: "app2"') == 1
        assert es_query.count(query='host: "foo"') == 0

        es_query = ElasticsearchQuery(es_host=self.es_test_host, index_prefix=self.EMPTY_INDEX_NAME)
        assert es_query.count(query='*') == 0

    def test_query_by_sql(self):
        es_query = ElasticsearchQuery(es_host=self.es_test_host, index_prefix=self.EMPTY_INDEX_NAME)

        res = es_query.query_by_sql(
            sql='SELECT host FROM "{index}" WHERE host = \'app2.prod\''.format(index=self.APP_LOGS_INDEX_NAME))
        assert res == [{'host': 'app2.prod'}]

        res = es_query.query_by_sql(
            sql='SELECT appname, host FROM "{index}" WHERE host = \'app2.prod\''.format(index=self.APP_LOGS_INDEX_NAME))
        assert res == [{'appname': 'foo', 'host': 'app2.prod'}]

        res = es_query.query_by_sql(
            sql='SELECT appname, host FROM "{index}" WHERE host = \'none\''.format(index=self.APP_LOGS_INDEX_NAME))
        assert res == []

        res = es_query.query_by_sql(
            sql='SELECT host FROM "{index}" ORDER BY host LIMIT 1'.format(index=self.APP_LOGS_INDEX_NAME))
        assert res == [{'host': 'app1.prod'}]

        res = es_query.query_by_sql(
            sql='SELECT count(*) AS cnt, MAX(time) FROM "{index}"'.format(index=self.APP_LOGS_INDEX_NAME))
        assert res == [{'MAX(time)': 320.0, 'cnt': 3}]

    def test_query_by_invalid_sql(self):
        es_query = ElasticsearchQuery(es_host=self.es_test_host, index_prefix=self.EMPTY_INDEX_NAME)

        with raises(RequestError):
            es_query.query_by_sql('FOO BAR')

    def test_not_existing_index(self):
        es_query = ElasticsearchQuery(es_host=self.es_test_host, index_prefix='not-existing-one')

        with raises(NotFoundError):
            es_query.query_by_string('*')
