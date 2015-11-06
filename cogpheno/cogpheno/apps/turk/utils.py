#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import datetime

from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
from boto.mturk.price import Price
import os

from django.conf import settings

PRODUCTION_HOST = u'mturk.com/mturk/externalSubmit'
SANDBOX_HOST = u'workersandbox.mturk.com/mturk/externalSubmit'

# TODO: this will need to be where our app is hosted
PRODUCTION_WORKER_URL = u'https://www.mturk.com'
SANDBOX_WORKER_URL = u'https://workersandbox.mturk.com'


class InvalidTurkSettings(Exception):
    """Connection settings for Turk are invalid"""
    def __init__(self, value):
        self.parameter = value

    def __unicode__(self):
        return repr(self.parameter)
    __str__ = __unicode__


def amazon_string_to_datetime(amazon_string):
    """Return datetime from passed Amazon format datestring"""

    amazon_iso_format = '%Y-%m-%dT%H:%M:%SZ'
    return datetime.datetime.strptime(
            amazon_string,
            amazon_iso_format)


def get_host():
    """Read configuration file and get proper host

    The host returned will be the contents of either PRODUCTION_HOST or
    PRODUCTION_HOST as defined in this module. Because the host
    parameter is optional, if it is omitted, the PRODUCTION_HOST is
    returned. Therefore, to use the sandbox, one has to explicitly set
    the host parameter to 'mechanicalturk.sandbox.amazonaws.com' in
    either the TURK or TURK_CONFIG_FILE parmeters/files.
    """
    host = PRODUCTION_HOST

    if hasattr(settings, 'TURK') and settings.TURK is not None:

        # Determine if we are in debug mode, set host appropriately
        if "debug" in settings.TURK:
            if settings.TURK["debug"] == 1:
                if "sandbox_host" in settings.TURK:                
                    host = settings.TURK["sandbox_host"]
            else:
                if 'host' in settings.TURK:
                    host = settings.TURK['host']


    # A settings file will just be used in production, no debug option
    elif hasattr(settings, 'TURK_CONFIG_FILE') and\
                          settings.TURK_CONFIG_FILE is not None:
        config = ConfigParser.ConfigParser()
        config.read(settings.TURK_CONFIG_FILE)
        if config.has_option('Connection', 'host'):
            host = config.get('Connection', 'host')

    # We don't want any custom URL addresses
    if host.startswith('http://'):
        host = host.replace('http://', '', 1)

    if host.startswith('https://'):
        host = host.replace('https://', '', 1)

    # This will trigger error if user is not using external submit
    assert host in [SANDBOX_HOST, PRODUCTION_HOST]

    return host


def is_sandbox():
    """Return True if configuration is configured to connect to sandbox"""

    host = get_host()
    return host == SANDBOX_HOST


def get_worker_url():
    """Get proper URL depending upon sandbox settings"""

    if is_sandbox():
        return SANDBOX_WORKER_URL
    else:
        return PRODUCTION_WORKER_URL


def get_connection():
    """Create connection based upon settings/configuration parameters

    The object returned from this function is a Mechanical Turk
    connection object. If the Mechanical Turk Connection object could
    not be created, an InvalidTurkSettings exception is raised.

    The Django settings file should have either the TURK or
    TURK_CONFIG_FILE parameters defined (and not set to None). If both
    are defined (and not None), the TURK parameter takes precedent.
    However, we encourage the use of the TURK_CONFIG_FILE parameter
    instead -- as the settings.py file is often checked into a
    repository.  The connection parameters used by Turk, especially
    the 'aws_secret_access_key' parameter, should be kept private.
    Thus, the TURK_CONFIG_FILE parameter indicates a file that should
    not be checked into a repository. Care should be taken that this
    file is not readable by other users/processes on the system.

    If the TURK parameter is used in the settings file, it will have a
    syntax similar to the following:

    TURK = {
        'aws_access_key_id': 'BJLBD8MOPC4ZDEB37QFB',
        'aws_secret_access_key': 'g8Xw/sCOLY5WYtS091kcVdy0cMUZgdSdS',
        'host': 'mturk.com/mturk/externalSubmit',
        'sandbox_host':'workersandbox.mturk.com/mturk/externalSubmit'
        'app_url': 'brainmeta.org'
        'debug': 1
    }

    The host and debug parameters are optional and, if omitted,
    defaults are used. The host is the Amazon Mechanical Turk host with
    which to connect. There are two choices, production or sandbox. If
    omitted, production is used.  Debug is the level of debug
    information printed by the boto library.

    If the TURK_CONFIG_FILE Django settings parameter is used, it
    should point to a file name that is parsable by ConfigParser. An
    example of these contents follow:

    [Connection]
    aws_access_key_id: 'BJLBD8MOPC4ZDEB37QFB'
    aws_secret_access_key: 'g8Xw/sCOLY5WYtS091kcVdy0cMUZgdSdS'
    host: 'mturk.com/mturk/externalSubmit'
    app_url: 'brainmeta.org'
    debug: 1
    """

    host = get_host()
    debug = 1

    if hasattr(settings, 'TURK') and settings.TURK is not None:
        aws_access_key_id = settings.TURK['aws_access_key_id']
        aws_secret_access_key = settings.TURK['aws_secret_access_key']
        if 'debug' in settings.TURK:
            debug = settings.TURK['debug']
    elif hasattr(settings, 'TURK_CONFIG_FILE') and\
                          settings.TURK_CONFIG_FILE is not None:
        config = ConfigParser.ConfigParser()
        config.read(settings.TURK_CONFIG_FILE)

        aws_access_key_id = config.get('Connection',
                                       'aws_access_key_id')
        aws_secret_access_key = config.get('Connection',
                                           'aws_secret_access_key')
        if config.has_option('Connection', 'debug'):
            debug = config.get('Connection', 'debug')
    else:
        raise InvalidTurkSettings("Turk settings not found")

    return MTurkConnection(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        host=host,
        debug=debug)


def get_app_url():
    if hasattr(settings, 'TURK') and settings.TURK is not None:
        if "app_url" in settings.TURK:
            return settings.TURK["app_url"]


def make_hit(title,description,keywords,amount=0.0,frame_height=800,number_hits=60):
    """make_hit
    make a set of hits to send to Amazon
    """
 
    connection = get_connection()
    url = get_app_url()

    if isinstance(keywords,str):
        keywords = [keywords]

    questionform = ExternalQuestion(url, frame_height)

    for _ in xrange(60):
        create_hit_result = connection.create_hit(
            title=title,
            description=description,
            keywords=keywords,
            max_assignments=1,
            question=questionform,
            reward=Price(amount=amount),
            response_groups=('Minimal', 'HITDetail'),  # I don't know what response groups are
        )


def save_worker(worker_id):
    """
    We need to keep track of worker's we've already seen
    """
    return "WRITEME"

def get_worker_ids_past_tasks():
    return "WRITE ME"
