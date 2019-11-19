
#need to implement adjacent() and timeTakenFor() functions
#adjacent(stopa,stopb)-> can you go from stopa to stopb without going through anyother stops
#if yes-> return True, else return False

#timeTakenFor(stopa,stopb) -> ave. time taken to move from stopa to stopb
#routes are same, populated

#reRoutes 
import requests
import json

distancematrix = dict()

API_KEY = "AIzaSyD8E6GoeHBjLGioCJIwcZDZQPdyIZQMCLI"

def bestInsertionForThisStop(currentRouteList,stop,totalTime):
	#print("Best insertion for this stop")
	bestTimeForThis = -1
	position = -1
	'''
	if(adjacent(stop,currentRouteList[0])): #adding stop at the front
		tmp = timeTakenFor(stop, currentRouteList[0])
		tmp += totalTime
		if(bestTimeForThis == -1 or tmp < bestTimeForThis):
			bestTimeForThis = tmp
			position = 0
	'''
	#dont add at the begining

	for index in range(len(currentRouteList)-1):#adding stop at the middle
		if(adjacent(currentRouteList[index], stop) and adjacent(stop, currentRouteList[index+1])):
			tmp = timeTakenFor(currentRouteList[index], stop)
			tmp += timeTakenFor(stop, currentRouteList[index+1])
			tmp -= timeTakenFor(currentRouteList[index], currentRouteList[index+1])
			tmp += totalTime
			if(bestTimeForThis == -1 or tmp < bestTimeForThis):
				bestTimeForThis = tmp
				position = index+1


	if(adjacent(currentRouteList[-1], stop)):#adding stop at the end
		tmp = timeTakenFor(currentRouteList[-1], stop)
		tmp += totalTime
		if(bestTimeForThis == -1 or tmp < bestTimeForThis):
			bestTimeForThis = tmp
			position = len(currentRouteList)
	#print("returned bestTime for this")
	print("in bestInsertionForThisStop: ",len(currentRouteList)," returned ",bestTimeForThis)
	return bestTimeForThis, position


def bestInsertion(currentRouteList, stopLeftList, totalTime, tripTimeLimit=120):#totalTime is the time taken for currentRouteList
	bestTime = -1
	bestStop = ""
	bestStopIndex = -1
	for index in range(len(stopLeftList)):
		stop = stopLeftList[index]
		currentBestTime, positionIndex = bestInsertionForThisStop(currentRouteList,stop,totalTime)
		if((bestTime == -1 and currentBestTime != -1) or currentBestTime < bestTime):
			bestTime = currentBestTime
			bestStopIndex = positionIndex
			bestStop = stop 
	return bestTime, bestStop, bestStopIndex

def bestInsertionTwo(currentRouteList, stopLeftList):
	bestTime = -1
	bestStop = ""
	for stop in stopLeftList:
		tmp = timeTakenFor(currentRouteList[-1],stop)
		if((bestTime == -1) or (bestTime>tmp)):
			bestTime = tmp
			bestStop = stop 

	return bestTime,bestStop

def insertion(currentRouteList,stop,position):
	if(position == 0):
		currentRouteList = [stop] + currentRouteList
	elif(position == len(currentRouteList)):
		currentRouteList = currentRouteList + [stop]
	else:
		currentRouteList = currentRouteList[:position] + [stop] + currentRouteList[position:]
	return currentRouteList


def getRoutesTwo(stopList,college,tripTimeLimit):
	stopList.append(college)
	RouteList = list()
	while(len(stopList)>1):#since the college stop will always be present
		curmax = -1
		start = college
		for stop in stopList:
			tmp = timeTakenFor(stop,college)
			if(tmp>curmax):
				curmax = tmp
				start = stop
		currentRouteTime = 0
		#print("stop list len is ",end="")
		#print(len(stopList))
		currentRoute = list()
		currentRoute.append(start)#the starting should be the college bus stop
		stopList.remove(start)
		while(len(stopList)>1):
			print("time:",currentRouteTime,", left out stops:",len(stopList))
			#print("currentRoute time = ",end="")
			#print(currentRouteTime)
			tmp = currentRouteTime
			currentRouteTime, stop = bestInsertionTwo(currentRoute,stopList)
			#print("current route len = ",end="")
			if((tmp+currentRouteTime)>tripTimeLimit):
				currentRouteTime += timeTakenFor(currentRoute[-1],college)
				currentRoute = insertion(currentRoute,college,len(currentRoute))
				break
			currentRoute = insertion(currentRoute,stop,len(currentRoute))
			if(stop['gps'] != college['gps']):
				stopList.remove(stop)
			else:
				break #when college is the nearest stop
			if(len(currentRoute)>=17):
				currentRouteTime += timeTakenFor(currentRoute[-1],college)
				currentRoute = insertion(currentRoute,college,len(currentRoute))
				break
			currentRouteTime += tmp
		newRoute = dict()
		newRoute["stops"] = currentRoute
		newRoute["time"] = currentRouteTime
		RouteList.append(newRoute)
	return RouteList

def getRoutes(stopList,start,tripTimeLimit):
	RouteList = list()
	
	while(len(stopList)>0):
		currentRouteTime = 0
		#print("stop list len is ",end="")
		#print(len(stopList))
		currentRoute = list()
		currentRoute.append(start)#the starting should be the college bus stop
		while(len(stopList)>0 and (currentRouteTime < tripTimeLimit)):
			print("time:",currentRouteTime,", left out stops:",len(stopList))
			#print("currentRoute time = ",end="")
			#print(currentRouteTime)
			tmp = currentRouteTime
			currentRouteTime, stop, index = bestInsertion(currentRoute,stopList,currentRouteTime)
			#print("current route len = ",end="")
			
			if((currentRouteTime + tmp) >tripTimeLimit):
				print("exit because of duration")
				currentRouteTime = tmp
				break
			stopList.remove(stop)
			currentRoute = insertion(currentRoute,stop,index)
			print(len(currentRoute))
			
			currentRouteTime += tmp
			if(len(currentRoute) > 19):
				print("exit because of number of stops")
				break
			

			
		newRoute = dict()
		newRoute["stops"] = currentRoute
		newRoute["time"] = currentRouteTime
		RouteList.append(newRoute)
	return RouteList

def Reroute(currentRouteList,routeToBeRemoved,startingPlace):
	feasibleRouteList = list()
	for route in currentRouteList:
		if(startingPlace in route):
			feasibleRouteList.append(route)
	if(len(feasibleRouteList)==0):
		return 403#none of the rerouting can be feasible, better to continue with a new bus
	while(len(routeToBeRemoved)>0):
		stop = routeToBeRemoved[0]
		for route in feasibleRouteList:
			currentBestTime, currentPosition = bestInsertionForThisStop(route.stops, stop, route.totalTime)
			if(bestTime == -1 or currentBestTime < bestTime):
				bestTime = currentBestTime
				position = currentPosition
				bestRoute = route 
		newRoute = insertion(bestRoute,stop,position)
		currentRouteList.remove(bestRoute)#remove the previous route
		newRoute = dict()
		newRoute["stops"] = currentRoute
		newRoute["time"] = currentRouteTime
		RouteList.append(newRoute)
		currentRouteList.append(tuple(newRoute,bestTime))# add the new one

	return currentRouteList

def timeTakenFor(source,destination):
	#global distancematrix
	if(source['gps'][-1]=='\n'):
		source['gps'] = source['gps'][:len(source['gps'])-1]
	if(destination['gps'][-1]=='\n'):
		destination['gps'] = destination['gps'][:len(destination['gps'])-1]
	if(source['gps']+':'+destination['gps'] in distancematrix.keys()):
		return distancematrix[source['gps']+':'+destination['gps']]
	URL = 'https://maps.googleapis.com/maps/api/distancematrix/json'
	#print(source['gps'])
	PARAMS = {
		'units' : 'imperial',
		'origins' : source['gps'],
		'destinations' : destination['gps'],
		'key':API_KEY
	}
	r = requests.get(url = URL, params = PARAMS) 
	data = r.json()
	#print(data)
	time = data['rows'][0]['elements'][0]['duration']['text']
	#global distancematrix
	distancematrix[source['gps']+':'+destination['gps']] = timeInMinutes(time)#get only the duration, not 'mins'
	return distancematrix[source['gps']+':'+destination['gps']]

def timeInMinutes(t):
	time= t.split(' ')
	length = len(time)
	length -=2;
	mins= 0
	if(length>=0):
		mins += int(time[length])
	length -= 2;
	if(length>=0):
		mins += int(time[length])*60 #hours to mins
	length-=2;
	if(length>=0):
		mins += int(time[length])*60*24 #days to mins
	return mins


def adjacent(stopa,stopb):
	return 1


fileread = open("stopNames_lat_log.txt","r")
line = fileread.readline()
pes = "12.9344948,77.5345164"
PESU = dict()
PESU["name"]="pes University,Bangalore"
PESU["gps"]=pes
stops = list()
while line:
	tmp = line.split('|')
	tmp[2] = tmp[2].split("\n")[0]
	stop = tmp[1]+','+tmp[2]
	curStop=dict()
	curStop["name"]=tmp[0]
	curStop["gps"]=stop
	if(pes != stop):
		stops.append(curStop)
	line = fileread.readline()

if(PESU in stops):
    print("objective not achieved")
else:
    print("everything is fine")
print("calling get routes")
routes = getRoutesTwo(stopList = stops,college = PESU,tripTimeLimit=100)

filewrite = open("generatedRoutesStopLimits17.txt","w")
for i in range(len(routes)):
	for stop in routes[i]["stops"]:
		filewrite.write(stop['name']+"|"+stop['gps'])
		filewrite.write("\n")
	#filewrite.write(str(len(routes[i]["stops"]))+" stops takes "+str(routes[i]["time"]))
	#filewrite.write("\n")
	filewrite.write("\n")
	#print("-----------------------------------------------------------------------------")

'''
source['gps']= "13.3033023,77.1300145"
destination['gps'] = "12.9344948,77.5345164"
time = timeTakenFor(source,destination)
print(time)

This method fails because the first couple of routes route to all the nearest stop, and the rest are left with very far off and less dense stops.
So to move from one to the other stops, it takes more time

Next intuition: pic the files which takes the longest and then keep moving until, pes is the nearest stop
'''