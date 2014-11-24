#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import socket
import MySQLdb
import json
import datetime


config = ConfigParser.ConfigParser()
config.read('config.ini')

stations = []

for section in config.sections():
	station = {}
	for option in config.options(section):
		station[option]=config.get(section,option)
	stations.append(station)


for station in stations:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.connect((station['host'], int(station['port'])))
	s.send('values')
	station['values']=s.recv(1024)
	s.send('close')
	#print json
	s.close()

print stations
db = MySQLdb.connect(user="yatm",passwd="yatm",db="yatm",unix_socket="/opt/lampp/var/mysql/mysql.sock")
cursor = db.cursor()
for station in stations:
	values=json.loads(station['values'])
	for value in values:
		cursor.execute("INSERT INTO `yatm`.`data` (`station`, `probe`, `time`, `value`) VALUES ('"+station['name']+"', '"+value['name']+"', '"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"', '"+value['value']+"')")

db.commit()
db.close()



