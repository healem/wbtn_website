#!../bin/python

import logging
import logging.config

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s'
        },
    },
    'handlers': {
        'file':{
            'class': 'logging.handlers.RotatingFileHandler',
            'mode': 'a',
            'maxBytes': 10485760,
            'backupCount': 5,
            'level':'DEBUG',
            'formatter': 'default',
            'filename': '/home/bythenum/logs/wbtn/wbtn-front.log',
            'encoding': 'utf-8',
        },
        'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'default',
        },
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'DEBUG',
    },
}

TEST_LOGGING = {
'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s'
        },
    },
    'handlers': {
        'file':{
            'class': 'logging.handlers.RotatingFileHandler',
            'mode': 'a',
            'maxBytes': 10485760,
            'backupCount': 5,
            'level':'DEBUG',
            'formatter': 'default',
            'filename': '/home/bythenum/logs/wbtn/wbtn-front-test.log',
            'encoding': 'utf-8',
        },
        'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'default',
        },
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'DEBUG',
    },
}

def initLogging():
    logging.config.dictConfig(LOGGING)

def initTestLogging():
    logging.config.dictConfig(TEST_LOGGING)
