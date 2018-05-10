wikia-common-kibana
===================

.. image:: https://travis-ci.org/macbre/wikia-common-kibana.svg?branch=master
    :target: https://travis-ci.org/macbre/wikia-common-kibana

Run queries against Kibana's Elasticsearch.

::

	pip install wikia-common-kibana


Basic Usage
-----------

.. code-block:: python

	from wikia_common_kibana import Kibana
	source = Kibana(since=12345, period=900)

`since`: UNIX timestamp data should be fetched since (if None, then period specifies the last n seconds).
`period`: period (in seconds) before now() to be used when since is empty (defaults to last 15 minutes).

.. code-block:: python

	source.get_rows(match={"tags": 'edge-cache-requestmessage'}, limit=2000)

Returns data matching the given query.

`match`: query to be run against Kibana log messages (ex. {"@message": "Foo Bar DB queries"}).
`limit`: the number of results (defaults to 10).

.. code-block:: python

	source.query_by_string(query='@message:"^PHP Fatal"', limit=2000)
	source.query_by_string(query='@message:"^PHP Fatal"', fields=['@message', '@source_host'], limit=2000)

Returns data matching the given query string.

`query`: query string to be run against Kibana log messages (ex. @message:"^PHP Fatal").
`fields`: optional list of fields to fetch
`limit`: the number of results (defaults to 10).

.. code-block:: python

	source.get_to_timestamp()

Returns the upper time boundary for the requested data.
