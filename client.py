import server as server
import http.client
import constants as constants

connection = http.client.HTTPConnection(constants.hostName + ":" + str(constants.hostPort))
connection.request("GET", "/ExampleFolder")
response = connection.getresponse()
print("Status: {} and reason: {}".format(response.status, response.reason))

connection.close()