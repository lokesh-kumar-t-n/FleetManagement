fileread = 'stopNames_lat_log.txt'

fileread1 = 'stopNames.txt'

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

mydb = client["fleetManagement"]

StopSpecifics = mydb["StopSpecifics"]

fileread = open(fileread,"r")
stopname = open(fileread1,"r")


#[StopID, Stopname, FullStopName, latitude, longitude]

routeList = list()
currentRoute = list()
stopcount = 1
routeNumber = 1
line = fileread.readline()
while line:
	line_list = line.split('|')
	curjson = dict()
	if(routeNumber<10):
		stopid = '0'+str(routeNumber)
	else:
		stopid = str(routeNumber)
	if(stopcount<10):
		stopid = stopid + 'PESB2020STP0'+ str(stopcount)
	else:
		stopid =  stopid + 'PESB2020STP'+ str(stopcount)

	currentRoute.append(stopid)

	stopcount += 1

	curjson["StopID"] = stopid
	curjson["FullStopName"] = line_list[0]
	line_list[2] = line_list[2].split('\n')[0]
	curjson["GPS"] = line_list[1]+','+line_list[2]

	line = stopname.readline()
	curjson["Stopname"] = str(line)

	StopSpecifics.insert_one(curjson)

	print(stopid)
	if (line_list[0] == 'Outer Ring Rd, Banashankari 3rd Stage, Banashankari, Bengaluru, Karnataka 560085, India'):
		stopcount = 1
		routeNumber += 1
		routeList.append(currentRoute)
		currentRoute = list()
		stopname.readline() #read the empty line

	line = fileread.readline()



print("starting RouteDetails")

routes = mydb["RouteDetails"]
for i in range(len(routeList)):
	print(i)
	if(i<9):
		routeId = '0'+str(i+1)+'PESB2020'
	else:
		routeId = str(i+1)+'PESB2020'
	curjson = {
		"routeID":routeId,
		"StopIDList":routeList[i]
	}
	routes.insert_one(curjson)
	print(routeId)



print("done")