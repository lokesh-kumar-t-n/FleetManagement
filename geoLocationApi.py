# importing the requests library 
import requests 

fileread = open("tmp.txt","r",encoding='utf8')
filewrite = open("stopNames_lat_log_tmp.txt","w")
# api-endpoint 
URL = "https://maps.googleapis.com/maps/api/geocode/json"
  
# location given here 
location = "kyathsandra, Tumkur"
API_KEY = "AIzaSyD8E6GoeHBjLGioCJIwcZDZQPdyIZQMCLI"
PARAMS = {'address':location,'key':API_KEY}

r = requests.get(url=URL, params = PARAMS)
data = r.json()
print(data)
exit(0)

# defining a params dict for the parameters to be sent to the API 
# Lakshmipura, Chinmaya Mission Hospital Road, laksmipuram, ಇಂದಿರಾ ನಗರ, Bengaluru, Karnataka 560038, India"
line = fileread.readline()
count = 0
exmpt = [7]
while line:
	count += 1
	if(len(line)>0):
		location = line[:len(line)-1]
		PARAMS = {'address':location,
			  	  'key':API_KEY} 
		#print(location)
		r = requests.get(url=URL, params = PARAMS)
		data = r.json()
		latitude = data['results'][0]['geometry']['location']['lat'] 
		longitude = data['results'][0]['geometry']['location']['lng']
		formatted_address = data['results'][0]['formatted_address']
		try:
			filewrite.write("%s | %s | %s\n"%(formatted_address,latitude,longitude))
		except:
			filewrite.write("%s | %s | %s\n"%(location,latitude,longitude))
			print("unable to print ",end="")
			print(count)
		
		print(location,end=" : ")

	line = fileread.readline()
	print(count)
  
print("done")
  
# extracting latitude, longitude and formatted address  
# of the first matching location 
