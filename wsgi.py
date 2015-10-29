#!/usr/bin/env python

import os
import bottle
import logging
from bottle import route, get, post, request, template
import json

SCRIPT_ROOT = os.path.join(os.path.dirname(__file__), 'client/scripts')
CSS_ROOT = os.path.join(os.path.dirname(__file__), 'client/content')
IMG_ROOT = os.path.join(os.path.dirname(__file__), 'client/img')
PAGE_ROOT = os.path.join(os.path.dirname(__file__), 'client')
logging.basicConfig()
log = logging.getLogger('python-starter-app')
log.setLevel(logging.DEBUG)

VCAP_SERVICES = os.getenv("VCAP_SERVICES")


'''
view routes
'''

@route('/vcap_services')
def getVcapServices(): 
    log.debug("retrieving VCAP_SERVICES")
    return VCAP_SERVICES
    
@route('/')
def defaultRoute():
    log.debug("default route request")
    return bottle.static_file('index.html', root=PAGE_ROOT)

@route('/<filename>')
def fileRoute(filename):
    log.debug("request for "+filename+", serving from "+PAGE_ROOT)
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
