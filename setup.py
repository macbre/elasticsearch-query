from setuptools import setup

VERSION = '2.2.5'

# @see https://github.com/pypa/sampleproject/blob/master/setup.py
setup(
    name='wikia_common_kibana',
    version=VERSION,
    author='Wikia Engineering',
    author_email='techteam-l@wikia-inc.com',
    license='MIT',
    description='Run queries against Kibana\'s Elasticsearch 6',
    url='https://github.com/macbre/wikia-common-kibana',
    py_modules=["wikia_common_kibana"],
    extras_require={
        'dev': [
            'coverage==4.5.1',
            'pylint==1.8.4',
            'pytest==3.5.1',
        ]
    },
    install_requires=[
        "elasticsearch>=6.0.0,<7.0.0",
        "python-dateutil==2.7.2",
    ]
)
