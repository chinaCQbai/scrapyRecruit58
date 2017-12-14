# -*- coding: utf-8 -*-

import MySQLdb
import datetime

dbuser = ''
dbpass = ''
dbname = 'cqhrsp'
dbhost = ''
dbport = '3306'

class T58PositionPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(user=dbuser, passwd=dbpass, db=dbname, host=dbhost, charset="utf8",
                                    use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        curTime = datetime.datetime.now()
        try:

            self.cursor.execute("""INSERT INTO positions (positionurl,agenturl,positionname,salary,location,education,
            experience,headcount, updatetime) VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s)""",
                                (item['positionurl'],
                                 item['agenturl'],
                                 item['positionname'],
                                 item['salary'],
                                 item['location'],
                                 item['education'],
                                 item['experience'],
                                 item['headcount'],
                                 item['updatetime']
                                 )
                                )

            self.conn.commit()

        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
        return item

class T58AgentPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(user=dbuser, passwd=dbpass, db=dbname, host=dbhost, charset="utf8",
                                    use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        curTime = datetime.datetime.now()
        try:

            self.cursor.execute("""INSERT INTO agents (agentname, source, sourceurl) VALUES (%s, %s, %s)""",
                                (item['agentname'],
                                 item['source'],
                                 item['sourceurl']
                                 )
                                )

            self.conn.commit()

        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
        return item
