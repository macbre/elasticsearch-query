"""
Set of integration tests. They're run on elasticsearch instance.

1. You need to ES_TEST_HOST environment variable when running tests to run them.
2. Files from fixtures/ directory will be enumerated and indices filled with data (one file per one index).
3. Enjoy.
"""
from os import getenv
from pytest import raises
from unittest import TestCase

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from elasticsearch_query import ElasticsearchQuery


class IntegrationTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.es_test_host = getenv('ES_TEST_HOST')

        # TODO: setup indices data
        pass

    def setUp(self):
        if self.es_test_host is None:
            self.skipTest('You need to pass ES_TEST_HOST env variable to run it')

    def test_connect(self):
        es = Elasticsearch(hosts=self.es_test_host)
        info = es.info()

        print(info)
        assert info['tagline'] == 'You Know, for Search'

    def test_not_existing_index(self):
        es_query = ElasticsearchQuery(es_host=self.es_test_host, index_prefix='not-existing-one')

        with raises(NotFoundError):
            es_query.query_by_string('*')
