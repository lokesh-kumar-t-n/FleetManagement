from flask import Flask, render_template, request, jsonify
import hashlib
import base64
import binascii
import json
import datetime
from pathlib import Path
import nexmo
from pymongo import MongoClient
import requests

app = Flask(__name__)
url = "https://www.fast2sms.com/dev/bulk"
myclient = MongoClient("mongodb://localhost:27017/")
mydb = myclient["FleetManagement"]


stopID= ["01PESB2020STP00"]
routeID= "01PESB2020"
studentID = "PES2020STUD0000"
driverID = "PES2020DRIV00"
adminID= "PES2020ADMIN01"
reviewID= "Review00"
guardianID="PES2020GUARD"


@app.route('/GenUserID/<userType>', methods=['GET'])
def gen_userID(userType):
    if request.method!='GET':
      response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
      return response    
    if userType=="0":
       global studentID
       f=studentID.rfind("0",11,14)
       if(f==-1):
         f=11
         num=str(int(studentID[f:])+1)
       else:
         num=str(int(studentID[f+1:])+1)         
       size=len(studentID)-f       
       if(len(num)>size):         
         studentID=studentID[0:f]+num
         response = app.response_class(response=json.dumps({"userID":studentID}), status=200, mimetype='application/json')
         return response 
       else:
         studentID=studentID[0:f+1]+num
         response = app.response_class(response=json.dumps({"userID":studentID}), status=200, mimetype='application/json')
         return response 
    elif userType=="1":
       global driverID
       f=driverID.rfind("0",11,12)
       if(f==-1):
         f=11
         num=str(int(driverID[f:])+1)
       else:
         num=str(int(driverID[f+1:])+1)         
       size=len(driverID)-f
       if(len(num)>size):         
         driverID=driverID[0:f]+num
         response = app.response_class(response=json.dumps({"userID":driverID}), status=200, mimetype='application/json')
         return response 
       else:
         driverID=driverID[0:f+1]+num    
         response = app.response_class(response=json.dumps({"userID":driverID}), status=200, mimetype='application/json')
         return response 
       
              
@app.route('/GenStopID/<routeID>', methods=['GET'])
def gen_stopID(routeID):
    if request.method!='GET':
      response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
      return response  
    global stopID
    g=routeID[0:2].lstrip("0")
    if(int(g)<=len(stopID)):
      i=int(g)-1
      stop_id=stopID[i]
      f=stop_id.rfind("0",13,14)
      if(f==-1):
        f=13
        num=str(int(stop_id[f:])+1)
      else:
        num=str(int(stop_id[f+1:])+1)         
      size=len(stop_id)-f
      if(len(num)>size):         
        stop_id=stop_id[0:f]+num
        stopID[i]=stop_id
        response = app.response_class(response=json.dumps({"stopID":stop_id}), status=200, mimetype='application/json')
        return response 
      else:
        stop_id=stop_id[0:f+1]+num
        stopID[i]=stop_id
        response = app.response_class(response=json.dumps({"stopID":stop_id}), status=200, mimetype='application/json')
        return response 
    else:
      g=routeID[0:2].lstrip("0") 
      if((int(g))<10):        
        stop_id="0"+str(int(g))+"PESB2020STP01"
        stopID.append(stop_id)
        response = app.response_class(response=json.dumps({"stopID":stop_id}), status=200, mimetype='application/json')
        return response   
      else:
        stop_id=str(int(g))+"PESB2020STP01"
        stopID.append(stop_id)
        response = app.response_class(response=json.dumps({"stopID":stop_id}), status=200, mimetype='application/json')
        return response          


@app.route('/GenrouteID', methods=['GET'])
def gen_routeID():
    if request.method!='GET':
      response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
      return response   
    global routeID
    g=routeID[0:2].lstrip("0") 
    if((int(g))<10):        
      routeID="0"+str(int(g))+"PESB2020STP"
      response = app.response_class(response=json.dumps({"routeID":routeID}), status=200, mimetype='application/json')
      routeID="0"+str(int(g)+1)+"PESB2020STP"      
      return response   
    else:
      routeID=str(int(g))+"PESB2020STP"
      response = app.response_class(response=json.dumps({"routeID":routeID}), status=200, mimetype='application/json')
      routeID=str(int(g)+1)+"PESB2020STP"      
      return response
      
  
@app.route('/GenreviewID', methods=['GET'])
def gen_reviewID():
    if request.method!='GET':
      response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
      return response    
    global reviewID
    f=reviewID.rfind("0",6,7)
    if(f==-1):
      f=6
      num=str(int(reviewID[f:])+1)
    else:
      num=str(int(reviewID[f+1:])+1)         
    size=len(reviewID)-f
    if(len(num)>size):         
      reviewID=reviewID[0:f]+num
      response = app.response_class(response=json.dumps({"reviewID":reviewID}), status=200, mimetype='application/json')
      return response 
    else:
      reviewID=reviewID[0:f+1]+num
      response = app.response_class(response=json.dumps({"reviewID":reviewID}), status=200, mimetype='application/json')
      return response 
  

@app.route('/GenguardianID/<userID>', methods=['GET'])
def gen_guardianID(userID):
    if request.method!='GET':
      response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
      return response  
    global studentID
    if(int(userID[-4:])>int(studentID[-4:])):  
      response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')
      return response 
    else:
      guardian=guardianID+studentID[-4:]
      response = app.response_class(response=json.dumps({"guardianID": guardian}), status=200, mimetype='application/json')
      return response 

  
@app.route('/Student/GetMobileNumbers/<userID>', methods = ['GET'])
def GetUserID(userID):
    if request.method!='GET':
      response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
      return response    
    mycol = mydb["Users"]
    for x in mycol.find({} ,{"_id": 0, "userID": 1, "phoneNumber": 1}):
        if(x["userID"]==userID):
           response = app.response_class(response=json.dumps({"mobile": x["phoneNumber"]}), status=200, mimetype='application/json')
           return response   
    response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')
    return response  


@app.route('/verifyUser/<userID>', methods = ['GET'])
def verify_user(userID):
    if request.method!='GET':
      response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
      return response    
    mycol = mydb["Users"]  
    for x in mycol.find({} ,{"_id": 0, "userID": 1, "userLevel": 1}):
        if(x["userID"]==userID):
           response = app.response_class(response=json.dumps({"valid":"1","userLevel":x["userLevel"]}), status=200, mimetype='application/json')
           return response     
    response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')
    return response
    
    
@app.route('/User/verifyPassword/<userID>', methods = ['POST'])
def verify_password(userID):
    if request.method!='POST':
      response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
      return response
    content = request.get_json()
    mycol = mydb["Users"]
    for x in mycol.find({} ,{"_id": 0, "userID": 1, "sha1(password)": 1}):
        if(x["userID"]==userID):
          if(x["sha1(password)"]==content["password"]):
            response = app.response_class(response=json.dumps({}), status=200, mimetype='application/json')
            return response
          response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')
          return response          
    response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')
    return response 


@app.route('/GetRouteID/<driverID>', methods = ['GET'])
def get_routeID(driverID):
    if request.method!='GET':
      response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
      return response    
    mycol = mydb["DriverRoute"]
    for x in mycol.find({} ,{"_id": 0, "driverID": 1, "routeID": 1}):
        if(x["driverID"]==driverID):
          l=[]
          l.append(x["routeID"])
          response = app.response_class(response=json.dumps(l), status=200, mimetype='application/json')
          return response     
    response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')
    return response
  
    
@app.route('/sendNotification', methods=['POST'])
def send_message():
    content=request.get_json()
    url = "https://www.fast2sms.com/dev/bulk"
    payload = "sender_id=FSTSMS&message="+str(content["message"])+"&language=english&route=p&numbers="+str(content["mobile"])
    headers = {
    'authorization': "bYEMNI5nKjPhBEZfN4OjD8BUIYmvQQXiiFtP0zkqdjSKfi4INGd6FiEjwfoL",
    'Content-Type': "application/x-www-form-urlencoded", 
    'Cache-Control': "no-cache",
    }
    response1 = requests.request("POST", url, data=payload, headers=headers)
    response = app.response_class(response=json.dumps({}), status=response1.status_code, mimetype='application/json')
    return response
  

@app.route('/Bus/PreviousStopDeparted/<routeID>/<Towards>', methods = ['GET'])
def bus_stop_prev(routeID,Towards):
    if request.method!='GET':
      response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
      return response    
    
    mycol=mydb["PreviousStop"]
    for x in mycol.find({} ,{"_id": 0, "routeID": 1, "prevStopID": 1}):
        if(x["routeID"]==routeID):
          prevstop=x["prevStopID"]
    mycol=mydb["StopSpecifics"]
    for x in mycol.find({} ,{"_id": 0, "stopID": 1, "stopname": 1}):    
        if(x["stopID"]==prevstop):
          d={}
          d["stop"]=x["stopname"]
          response = app.response_class(response=json.dumps(d), status=200, mimetype='application/json')
          return response
    response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')
    return response
  
    
@app.route('/Student/GetRouteNumber/<userID>', methods = ['GET'])
def get_route_number(userID):
    if request.method!='GET':
      response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
      return response    
    mycol = mydb["Attendence"]
    for x in mycol.find({} ,{"_id": 0, "userID": 1, "routeID": 1}): 
        if(x["userID"]==userID):
          response = app.response_class(response=json.dumps({"routeID":x["routeID"]}), status=200, mimetype='application/json')
          return response
    response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')
    return response  


@app.route('/Student/markAbsent/<userID>', methods = ['PUT'])
def mark_absent(userID):
    if request.method!='PUT':
      response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
      return response    
    mycol = mydb["Attendence"]
    for x in mycol.find({} ,{"_id": 0, "userID": 1, "IsAbsent": 1}): 
       if(x["userID"]==userID):
         if(x["IsAbsent"]=="1"):
           response = app.response_class(response=json.dumps({}), status=200, mimetype='application/json')
           return response
         elif(x["IsAbsent"]=="0"):
           myquery = { "userID": userID }
           newvalues = { "$set": { "IsAbsent": "1" } }
           mycol.update_one(myquery, newvalues)
           response = app.response_class(response=json.dumps({}), status=200, mimetype='application/json')
           return response      
    response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')
    return response
  

@app.route('/Student/getUserIDsAtLocation/<stop_id>', methods = ['GET'])
def get_users_at_Location(stop_id):
    if request.method!='GET':
      response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
      return response    
    l=[]
    mycol = mydb["StopCollection"]        
    for x in mycol.find({} ,{"_id": 0, "StopID": 1,"userID": 1}): 
        if(x["StopID"]==stop_id):
          l.append(x["userID"])   
    if(len(l)==0):
      response = app.response_class(response=json.dumps(l), status=400, mimetype='application/json')
      return response  
    mydoc1={}
    mydoc1["userIDs"]=l
    mycol=mydb["Attendence"]
    for x in mycol.find({} ,{"_id": 0, "userID": 1, "routeID": 1}): 
        if(x["userID"] in l):
          route=x["routeID"]
          mycol2=mydb["PreviousStop"]
          myquery = { "routeID": route}    
          newvalues = { "$set": { "prevStopID": stop_id } }
          mycol2.update_one(myquery, newvalues)      
          response = app.response_class(response=json.dumps(mydoc1), status=200, mimetype='application/json')
          return response
  
    
@app.route('/Student/setStopID/<stop_id>', methods = ['PUT'])
def set_stopID(stop_id):
    if request.method!='PUT':
      response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
      return response
    content = request.get_json()
    mycol = mydb["StopSpecifics"]
    if(len(content)==1):
      stop={}
      stop["StopID"]=stop_id
      stop["stopname"]=content["stop"]
      mycol.insert_one(stop)
      response = app.response_class(response=json.dumps({}), status=200, mimetype='application/json')
      return response
    else:
      response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')
      return response 
  

@app.route('/Bus/Feedbacks/<routeID>/<reviewID>', methods = ['POST'])
def Bus_Review(reviewID,routeID):
    if request.method!='POST':
      response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
      return response    
    content = request.get_json()
    review= content["description"]
    mycol = mydb["RouteDetails"]
    for x in mycol.find({} ,{"_id": 0, "routeID": 1}):     
        if(x["routeID"]==routeID):
           mycol1= mydb["Feedbacks"]  
           d={"routeID": routeID, "reviewID": reviewID, 
                    "description": review, "Comment": [], "nov": 0,
                    "userLike": 0, "Dislike": 0, "userDislike": 0 }     
           mycol1.insert_one(d)    
           response = app.response_class(response=json.dumps({}), status=200, mimetype='application/json')
           return response
    response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')
    return response 
  
    
@app.route('/Bus/GetBusNumber/<routeID>', methods = ['GET'])
def get_BusNumber(routeID):
    if request.method!='GET':
      response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
      return response
    mycol = mydb["RouteDetails"]
    for x in mycol.find({} ,{"_id": 0, "routeID": 1, "BusNumber": 1}): 
        if(x["routeID"]==routeID):
          d={}
          d["BusNumber"]=x["BusNumber"]
          response = app.response_class(response=json.dumps(d), status=200, mimetype='application/json')
          return response 
    response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')
    return response


@app.route('/Bus/Feedbacks/<reviewID>/Like/<userID>', methods = ['PUT'])
def Like_review(reviewID,userID):
    if request.method!='PUT':
      response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
      return response    
    myquery = {"reviewID":  reviewID} 
    mycol = mydb["Feedbacks"]
    for x in mycol.find({} ,{"_id": 0, "reviewID": 1, "nov": 1, "userLike": 1}): 
      if(x["reviewID"]==reviewID):
        a= int(x["nov"])
        l= x["userLike"]
        if userID not in l:
           newvalues = { "$set": { "nov": str(a+1) } }
           mycol.update_one(myquery, newvalues) 
           l.append(userID)
           newvalues = { "$set": { "userLike": l } }
           mycol.update_one(myquery, newvalues) 
           response = app.response_class(response=json.dumps({}), status=200, mimetype='application/json')
           return response
        else:
           response = app.response_class(response=json.dumps({}), status=200, mimetype='application/json')
           return response
    
    response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')
    return response 
  

@app.route('/Bus/Feedbacks/<reviewID>/Dislike/<userID>', methods = ['PUT'])
def Unlike_review(reviewID,userID):
    if request.method!='PUT':
      response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
      return response    
    myquery ={ "reviewID":  reviewID }
    mycol = mydb["Feedbacks"]
    for x in mycol.find({} ,{"_id": 0, "reviewID": 1, "Dislike": 1, "userDislike": 1}): 
      if(x["reviewID"]==reviewID):
        a= int(x["Dislike"])
        l= x["userDislike"]
        if userID not in l:
           newvalues = { "$set": { "Dislike": str(a+1) } }
           mycol.update_one(myquery, newvalues) 
           l.append(userID)
           newvalues = { "$set": { "userDislike": l } }
           mycol.update_one(myquery, newvalues) 
           response = app.response_class(response=json.dumps({}), status=200, mimetype='application/json')
           return response
        else:
           response = app.response_class(response=json.dumps({}), status=200, mimetype='application/json')
           return response    
    response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')
    return response 
  
    
@app.route('/Bus/Feedbacks/Comment/<reviewID>', methods = ['POST'])
def Comment_Review(reviewID):
    if request.method!='POST':
      response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
      return response    
    content = request.get_json()
    mycol = mydb["Feedbacks"]
    for x in mycol.find({} ,{"_id": 0, "reviewID": 1, "Comment": 1}): 
        if(x["reviewID"]==reviewID):
          l=x["Comment"]
          l.append(content["comment"])
          myquery ={"reviewID":  reviewID}
          newvalues = { "$set": { "Comment": l} }
          mycol.update_one(myquery, newvalues)    
          response = app.response_class(response=json.dumps({}), status=200, mimetype='application/json')
          return response    
    response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')
    return response     

  
@app.route('/Bus/markBoarding/<userID>', methods = ['PUT'])
def mark_boarding(userID):
    if request.method!='PUT':
      response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
      return response    
    mycol = mydb["Attendence"]
    for x in mycol.find({} ,{"_id": 0, "userID": 1, "isBoarded": 1}): 
       if(x["userID"]==userID):
         if(x["isBoarded"]==1):
           response = app.response_class(response=json.dumps({}), status=200, mimetype='application/json')
           return response
         elif(x["isBoarded"]==0):
           myquery = { "userID": userID }
           newvalues = { "$set": { "isBoarded": 1 } }
           mycol.update_one(myquery, newvalues)
           response = app.response_class(response=json.dumps({}), status=200, mimetype='application/json')
           return response      
    response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')
    return response 
  
  
@app.route('/Bus/markDeBoarding/<userID>', methods = ['PUT'])
def mark_Deboarding(userID):
    if request.method!='PUT':
      response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
      return response    
    mycol = mydb["Attendence"]
    for x in mycol.find({} ,{"_id": 0, "userID": 1, "isBoarded": 1}): 
       if(x["userID"]==userID):
         if(x["isBoarded"]==0):
           response = app.response_class(response=json.dumps({}), status=200, mimetype='application/json')
           return response
         elif(x["isBoarded"]==1):
           myquery = { "userID": userID }
           newvalues = { "$set": { "isBoarded": 0 } }
           mycol.update_one(myquery, newvalues)
           response = app.response_class(response=json.dumps({}), status=200, mimetype='application/json')
           return response      
    response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')
    return response  
     
    
@app.route('/addUsers', methods = ['POST'])
def add_Users():
    if request.method!='POST':
      response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
      return response      
    mycol = mydb["Users"]
    content = request.get_json()
    mycol.insert_one(content)
    response = app.response_class(response=json.dumps({}), status=200, mimetype='application/json')
    return response

   
@app.route('/Student/getPhoneNumbers', methods = ['POST'])
def return_phonenumbers():
    if request.method!='POST':
      response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
      return response      
    content = request.get_json()
    mycol = mydb["Users"]
    l=content["u"]
    d=[]
    for i in l:
        for x in mycol.find({} ,{"_id": 0, "userID": 1, "phoneNumber": 1}):   
            if(x["userID"]==i):
              d.append(x["phoneNumber"])
    if(len(d)==0):
      response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')
      return response         
    response = app.response_class(response=json.dumps(d), status=200, mimetype='application/json')
    return response


if __name__ == '__main__':
   app.run(host='localhost',port="5000")

    

    



  

  

