#!/usr/bin/env python

import os
import bottle
import logging
import urlparse
import uuid
from bottle import route, get, post, request, template
import sys

import json
from threading import Thread

SCRIPT_ROOT = os.path.join(os.path.dirname(__file__), 'view/scripts')
CSS_ROOT = os.path.join(os.path.dirname(__file__), 'view/content')
IMG_ROOT = os.path.join(os.path.dirname(__file__), 'view/img')
PAGE_ROOT = os.path.join(os.path.dirname(__file__), 'client')
logging.basicConfig()
log = logging.getLogger('receiver')
log.setLevel(logging.DEBUG)


'''
view routes
'''

@route('/')
def defaultRoute():
    return bottle.static_file('index.html', root=PAGE_ROOT)

@route('/<filename>')
def fileRoute(filename):
    return bottle.static_file(filename, root=PAGE_ROOT)


# @route('/addservice.html')
# def addservice():
#     return bottle.static_file('addservice.html', root=PAGE_ROOT)
    

'''
required to serve static resources
'''
@route('/client/<filepath:path>')
def serve_scripts(filepath):
    log.debug("serving js assets")
    return bottle.static_file(filepath, root=PAGE_ROOT)


'''
service runner code
'''
log.debug("starting web server")
application = bottle.app()
application.catchall = False


# NOTE that these will default to rational values if not set for local run.

assignedHost = os.getenv('VCAP_APP_HOST','127.0.0.1')
assignedPort = os.getenv('VCAP_APP_PORT',8080)

log.debug('launching application at %s:%s'%(assignedHost,assignedPort))
bottle.run(application, host=assignedHost, port=assignedPort)


# this is the last line
