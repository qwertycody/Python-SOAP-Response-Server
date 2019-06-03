#!/usr/bin/python3

import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import os as os
import utils as utils
import threading
import debug as debug
import constants as constants

class LogEntry:
	def __init__(self, time, path, request, response, filePath):
		self.time = time
		self.response = response
		self.path = path
		self.request = request
		self.filePath = filePath

listOfLogs = []

def addLog(self, logEntry):
	if "favicon.ico" not in self.path:
		listOfLogs.append(logEntry)

class MyServer(BaseHTTPRequestHandler):

	def doWork(self):
		try:
			debugRequest = debug.debugRouter(self, listOfLogs)

			if debugRequest == True:
				return
		except Exception as e:
			utils.printStackTrace(e)

		logEntry = LogEntry(utils.getTimestamp(), self.path, self.request, None, None)		

		try:

			path = self.path
			path = path.replace("/Main", "")
			path = path.replace("/", "")

			folderExists = utils.getDirectories_Match(path)

			if folderExists == True:
				pathPattern = "./" + path + "/*"
				fileObject = utils.getFiles_LatestModified(pathPattern)
				
				self.send_response(200)
				self.send_header('Content-Type', "text/xml; charset=UTF-8")
				self.end_headers()

				logEntry.filePath = fileObject 

				with open(fileObject, 'rb') as file:
					self.wfile.write(file.read()) # Read the file and send the contents 

				with open(fileObject, 'rb') as file:
					logEntry.response = file.read() 

				addLog(self, logEntry)
			else:
				self.send_response(404)
				self.send_EmptyResponse()
				addLog(self, logEntry)
		except Exception as e:
			utils.printStackTrace(e)
			self.send_response(500)
			self.send_EmptyResponse()
			addLog(self, logEntry)
	
	def send_EmptyResponse(self):
		self.wfile.write(bytes("", "utf-8"))

	def do_POST(self):
		self.doWork()

	def do_GET(self):
		self.doWork()
		
myServer = HTTPServer((constants.hostName, constants.hostPort), MyServer)
print(time.asctime(), "Server Starts - %s:%s" % (constants.hostName, constants.hostPort))

try:
	thread = threading.Thread(target=myServer.serve_forever)
	thread.start()
except KeyboardInterrupt:
	pass

#myServer.server_close()
#print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))