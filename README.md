elasticsearch-query
===================

[![PyPI](https://img.shields.io/pypi/v/elasticsearch-query.svg)](https://pypi.python.org/pypi/elasticsearch-query)
[![Build Status](https://travis-ci.org/macbre/elasticsearch-query.svg?branch=master)](https://travis-ci.org/macbre/elasticsearch-query)

Run queries against Kibana's Elasticsearch that gets logs from Logstash. Forked from [Wikia's `kibana.py`](https://github.com/Wikia/python-commons/blob/master/wikia/common/kibana/kibana.py).

```
pip install elasticsearch-query
```

## Basic Usage

```python
from elasticsearch_query import ElasticsearchQuery
es_query = ElasticsearchQuery(es_host='es.prod', since=12345, period=900)
```

`es_host` needs to be specified with a host of Elasticsearch instance to connect.

Provide either `since` (absolute timestamp) or `period` (last N seconds):

* `since`: UNIX timestamp data should be fetched since (if None, then period specifies the last n seconds).
* `period`: period (in seconds) before now() to be used when since is empty (defaults to last 15 minutes).

### `get_rows`

> Returns data matching the given query (provided as a `dict`).

```python
es_query.get_rows(match={"tags": 'edge-cache-requestmessage'}, limit=2000)
```

* `match`: query to be run against log messages (ex. {"@message": "Foo Bar DB queries"}).
* `limit`: the number of results (defaults to 10).

### `query_by_string`

> Returns data matching the given query string (provided as a [Lucene query](https://lucene.apache.org/core/2_9_4/queryparsersyntax.html)).

```python
es_query.query_by_string(query='@message:"^PHP Fatal"', limit=2000)
es_query.query_by_string(query='@message:"^PHP Fatal"', fields=['@message', '@es_query_host'], limit=2000)
```

* `query`: query string to be run against log messages (ex. `@message:"^PHP Fatal"`).
* `fields`: optional list of fields to fetch
* `limit`: the number of results (defaults to 10).

### `get_to_timestamp`

> Returns the upper time boundary for the requested data.

```python
es_query.get_to_timestamp()
```
