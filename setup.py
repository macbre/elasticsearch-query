from setuptools import setup

VERSION = '2.2.7'

# @see https://github.com/pypa/sampleproject/blob/master/setup.py
setup(
    name='elasticsearch-query',
    version=VERSION,
    author='Maciej Brencz',
    author_email='macbre@wikia-inc.com',
    license='MIT',
    description='Run queries against Kibana\'s Elasticsearch that gets logs from Logstash.',
    keywords='logstash kibana elasticsearch logging',
    url='https://github.com/macbre/elasticsearch-query',
    py_modules=["elasticsearch_query"],
    extras_require={
        'dev': [
            'coverage==4.5.1',
            'pylint==1.9.2',  # 2.x branch is for Python 3
            'pytest==3.9.3',
        ]
    },
    install_requires=[
        "elasticsearch>=6.0.0,<7.0.0",
        "python-dateutil==2.7.5",
    ]
)
