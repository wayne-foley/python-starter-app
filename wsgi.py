#!/usr/bin/env python

import os
import bottle
import logging
from bottle import route, get, post, request, template
import MySQLdb
import json

SCRIPT_ROOT = os.path.join(os.path.dirname(__file__), 'client/scripts')
CSS_ROOT = os.path.join(os.path.dirname(__file__), 'client/content')
IMG_ROOT = os.path.join(os.path.dirname(__file__), 'client/img')
PAGE_ROOT = os.path.join(os.path.dirname(__file__), 'client')
logging.basicConfig()
log = logging.getLogger('receiver')
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

@route('/mysql/<brokername>')
def testMySQL(brokername):
    log.debug("testing mysql connection using parameters from %s"%brokername)
    loadedVcapServices  = json.loads(VCAP_SERVICES)
    
    for obj in loadedVcapServices:
        if obj == "user-provided":
            
            userProvided = loadedVcapServices[obj]
            
            for broker in userProvided:
                if brokername == broker["name"]:
                    credentials = broker['credentials']
                
                    
                    return mysqlConnect(credentials)
                                     
        elif obj == brokername:
            credentials = loadedVcapServices[brokername][0]['credentials']
            
            return mysqlConnect(credentials)
                     

def mysqlConnect(credentials):
    # expected variables
    hostname = credentials['hostname']
    username = credentials['user']
    password = credentials['password']
    portNum = credentials['port']
    dbName = credentials['name']
    dbInstance = None
    
    try: 
        log.debug("attempting to connect to jdbc:mysql://%s:%s@%s:%d/%s"%(username,password,hostname,int(portNum),dbName))
        
        dbInstance = MySQLdb.connect(host=hostname,user=username,passwd=password,db=dbName, port=int(portNum)) 
        
        log.debug("creating a table in database %s"%dbName)
        testTableCreate = 'CREATE TABLE IF NOT EXISTS testtable( test_id int not null, test_value char(100),PRIMARY KEY(test_id));'

        cur = dbInstance.cursor()
        log.debug('executing fibdata table create')
        cur.execute(testTableCreate)
        dbInstance.commit()
        
    except MySQLdb.Error, e:
        log.error("unable to connect to database")
        return(json.loads('{"result":"failure","description":"failed during mysql table creation"}'))
    
    try:
        log.debug("inserting a value in database %s"%dbName)
        testTableInsert = "INSERT INTO testtable(test_id, test_value) values(1,'foo')";
        cur = dbInstance.cursor()
        cur.execute(testTableInsert)
        dbInstance.commit() 
    except MySQLdb.Error, e:
        log.error("unable to insert data into database")
        return(json.loads('{"result":"failure","description":"failed during row insertion"}'))
    
    
    try:
        log.debug("removing created table from  database %s"%dbName)
        testTableInsert = "DROP TABLE testtable";
        cur = dbInstance.cursor()
        cur.execute(testTableInsert)
        dbInstance.commit() 
    except MySQLdb.Error, e:
        log.error("unable to drop table")
        return(json.loads('{"result":"failure","description":"failed during mysql table deletion"}'))              
         
    ret = json.loads('{"result":"success","description":"all mysql connectivity tests passed"}')            
    
    return(ret)                    
            
    


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
