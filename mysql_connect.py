'''
Created on Oct 17, 2015

@author: arunjacob
'''
import MySQLdb
import logging
import json

log = logging.getLogger('python-starter-app')
log.setLevel(logging.DEBUG)


def mysqlConnect(credentials):
    
    testStatus = {}
    testStatus['test-name'] = 'mysql-validation'
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
        testStatus['connection-test'] = 1
        
    except MySQLdb.Error, e:
        testStatus['connection-test'] = 0
        log.error("unable to connect to database")
        return(json.dumps(testStatus))
        
    try:
        log.debug("creating a table in database %s"%dbName)
        testTableCreate = 'CREATE TABLE IF NOT EXISTS testtable( test_id int not null, test_value char(100),PRIMARY KEY(test_id));'

        cur = dbInstance.cursor()
        log.debug('executing fibdata table create')
        cur.execute(testTableCreate)
        dbInstance.commit()
        testStatus['table-create-test'] = 1
    except MySQLdb.Error, e:
        testStatus['table-create-test'] = 0
        log.error("unable to create a table")
        return(json.dumps(testStatus))
    
    try:
        log.debug("inserting a value in database %s"%dbName)
        testTableInsert = "INSERT INTO testtable(test_id, test_value) values(1,'foo')";
        cur = dbInstance.cursor()
        cur.execute(testTableInsert)
        dbInstance.commit() 
        testStatus['insert-test'] = 1
    except MySQLdb.Error, e:
        log.error("unable to insert data into database")
        testStatus['insert-test'] = 0
        return(json.dumps(testStatus))
    
    try:
        log.debug("removing created table from  database %s"%dbName)
        testTableInsert = "DROP TABLE testtable";
        cur = dbInstance.cursor()
        cur.execute(testTableInsert)
        dbInstance.commit()
        testStatus['drop-table-test'] = 1 
    except MySQLdb.Error, e:
        log.error("unable to drop table")
        testStatus['drop-table-test'] = 0
        return(json.loads('{"result":"failure","description":"failed during mysql table deletion"}'))              
         
    
    return(json.dumps(testStatus))     