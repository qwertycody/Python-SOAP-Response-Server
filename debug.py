def debugRouter(self, listOfLogs):
		path = self.path

		if ("/debug" in path) == False:
			return False
		
		if ("/request" in path) == True:
			id = getId(path)
			content = listOfLogs[int(id)].request
			xmlViewer(self, content)
			return True

		if ("/response" in path) == True:
			id = getId(path)
			content = listOfLogs[int(id)].response
			xmlViewer(self, content)
			return True

		mainDebugScreen(self, listOfLogs)
		return True

def getId(path):
	path = path.replace("debug", "")
	path = path.replace("request", "")
	path = path.replace("response", "")
	path = path.replace("/", "")
	return path

def mainDebugScreen(self, listOfLogs):
	self.send_response(200)
	self.send_header('Content-Type', "text/html; charset=UTF-8")
	self.end_headers()

	dataToDisplay = "<meta http-equiv=\"refresh\" content=\"5\">"

	for id_substring, logEntry  in enumerate(listOfLogs):
		headerRow=  getRowString("Data:", "Value:", True)
		timeRow = getRowString("Time:", str(logEntry.time), False)
		pathRow = getRowString("Path:", str(logEntry.path), False)
		requestRow = getFullDebugRow("Request:", "request", id_substring)
		filePathRow = getRowString("Response File Path:", str(logEntry.filePath), False)
		responseRow = getFullDebugRow("Response:", "response", id_substring)

		table = "<table border='1'>" + headerRow + timeRow + pathRow + requestRow + filePathRow + responseRow + "</table>"
		dataToDisplay = table + "<br />" + dataToDisplay

	self.wfile.write(bytes("<html><body>"+ dataToDisplay + "</body></html>", "utf-8"))

def getFullDebugRow(text, endpoint, id_substring):
	link = "/debug/" + str(id_substring) + "/" + endpoint
	text = getLink(text, link)
	value = getIframe("", link)
	row = getRowString(text, value, False)
	return row

def getIframe(text, link):
	return "<iframe src=" + '"' + link + '"' + ">" + text + "<iframe></iframe>"

def getLink(text, link):
	return "<a href=" + '"' + link + '"' + ">" + text + "</a>"

def getRowString(label, value, header):
	if header == True:
		return "<tr><th>"+ label  +"</th><th>"+ value +"</th></tr>"
	else:
		return "<tr><td>"+ label  +"</td><td>"+ value +"</td></tr>"

def xmlViewer(self, content):
	self.send_response(200)
	self.send_header('Content-Type', "text/xml; charset=UTF-8")
	self.end_headers()

	try:
		self.wfile.write(content)
	except Exception:
		print("Bad XML Caught - Not Outputting")