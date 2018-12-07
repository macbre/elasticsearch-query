from setuptools import setup

VERSION = '2.4.0'

# @see https://packaging.python.org/tutorials/packaging-projects/#creating-setup-py
with open("README.md", "r") as fh:
    long_description = fh.read()

# @see https://github.com/pypa/sampleproject/blob/master/setup.py
setup(
    name='elasticsearch-query',
    version=VERSION,
    author='Maciej Brencz',
    author_email='macbre@wikia-inc.com',
    license='MIT',
    description='Run queries against Kibana\'s Elasticsearch that gets logs from Logstash.',
    keywords='logstash kibana elasticsearch logging',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/macbre/elasticsearch-query',
    py_modules=["elasticsearch_query"],
    extras_require={
        'dev': [
            'coverage==4.5.2',
            'pylint>=1.9.2, <=2.1.1',  # 2.x branch is for Python 3
            'pytest==4.0.0',
            'PyYAML==3.13',
            'twine==1.12.1',
        ]
    },
    install_requires=[
        "elasticsearch>=6.0.0,<7.0.0",
        "python-dateutil==2.7.5",
    ]
)
