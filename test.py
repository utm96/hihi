# (\d+) giờ


# l = "10 phút 2 giờ"
# import re
# hour = float(re.match(".*(\d+) giờ",l).group(1))
# minute = float(re.match("(.*\s|^)(\d+) phút",l).group(2))
# time = + minute*60
# print(f'{hour} --- {minute}')
# print(time)

# # print(str(re.match(".*(\d+) phút",l)))
# time = 999999999
# def parseTime(timeString,time):
#     hour = float(re.match(".*(\d+) giờ",timeString).group(1))
#     minute = float(re.match("(.*\s|^)(\d+) phút",timeString).group(2))
#     time = hour*3600 + minute*60
#     return time


# time = parseTime("1 giờ 50 phút",time)
# print(time)
from pymongo import MongoClient

mongo_uri = 'mongodb://localhost:27017'
mongo_db = 'DataTransport'
client = MongoClient(mongo_uri)
db = client[mongo_db]

from neo4j import GraphDatabase

uri = "bolt://localhost"
driver = GraphDatabase.driver(uri, auth=("neo4j", "123a!@#A"))
# pipeline = [
#     {"$match": {"dia chi" :{ "$ne" : 'null' } } }, 
#     {"$group" : {"_id": "$dia chi", "count": { "$sum": 1 } } },
#     {"$match": {"count" : {"$gt": 1} } }, 
#     {"$project": {"dia chi" : "$_id", "_id" : 0} }
# ]
# lis = list(db['car_station_detail'].aggregate(pipeline))
# print(len(lis))
# response = []
# for doc in lis:
#     del doc["dia chi"][0]
#     for id in doc["dia chi"]:
#         response.append(id)

# coll.remove({"_id": {"$in": response}})

# db['car_station_detail'].ensureIndex({'dia chi':1},{ 'unique':'true', 'dropDups':'true' })
# print(len(list(db['car_station_detail'].find({'dia chi':'Km 9, Đường Phạm Văn Đồng, Phường Hải Thành - Dương Kinh - Hải Phòng'}))))

# "departure": "145 Trường Chinh - Vinh - Nghệ An",
#   "arrival":
# result = db['car_route_detail'].group(['departure','arrival'], None,
#                         {'list': []}, # initial
#                         'function(obj, prev) {prev.list.push(obj)}') 
# print(len(result))


# print(list(db['car_station_detail'].find({'dia chi':'66/7 Quốc lộ 22, Ấp Đông Lân, X. Bà Điểm, H. Hóc Môn - Hóc Môn - Hồ Chí Minh'})))

m = 'Hoàn Kiếm,HaNoi'

# "Region": 1
def get_level(address_components):
    result = {}
    i = 0
    for component in address_components:
        if 'administrative_area_level_1'  in component['types']:
            i += 1
            result['administrative_area_level_1'] = component['long_name']
        if ('locality' in component['types']) or ('administrative_area_level_2' in component['types']) or ('route' in component['types']) or ('sublocality_level_1'  in component['types']):
            i +=1
            result['level_'+str(i)] = component['long_name']
    return result


def create_level(graphDB_Session,name,long_name,short_name,lat,lng,level):
    query_create  = ['CREATE (',"",":"+level+" { name:'","","',lat : ","",", lng:","",", long_name:'","","', short_name:'","","'})"]
    query_car  = ['CREATE (',"",":CarStation { name:'","","', long_name:'","","', short_name:'","","'})"]
    query_train  = ['CREATE (',"",":TrainStation { name:'","","', long_name:'","","', short_name:'","","'})"]
    query_plane  = ['CREATE (',"",":PlaneStation { name:'","","', long_name:'","","', short_name:'","","'})"]
    # query_car  = ['CREATE (',"",":BoardStation { name:'","","'})"]

    query_car_relation ="MATCH (a:"+level+"),(b:CarStation) WHERE a.name = b.name CREATE (a)-[r:route { min_price: 0, price : 0, ave_price : 0 ,min_time: 0, time : 0, ave_time : 0 }]->(b)"
    query_train_relation ="MATCH (a:"+level+"),(b:TrainStation) WHERE a.name = b.name CREATE (a)-[r:route { min_price: 0, price : 0, ave_price : 0 ,min_time: 0, time : 0, ave_time : 0 }]->(b)"
    query_plane_relation ="MATCH (a:"+level+"),(b:PlaneStation) WHERE a.name = b.name CREATE (a)-[r:route { min_price: 0, price : 0, ave_price : 0 ,min_time: 0, time : 0, ave_time : 0 }]->(b)"
    query_car1_relation ="MATCH (a:"+level+"),(b:CarStation) WHERE a.name = b.name CREATE (a)<-[r:route { min_price: 0, price : 0, ave_price : 0 ,min_time: 0, time : 0, ave_time : 0 }]-(b)"
    query_train1_relation ="MATCH (a:"+level+"),(b:TrainStation) WHERE a.name = b.name CREATE (a)<-[r:route { min_price: 0, price : 0, ave_price : 0 ,min_time: 0, time : 0, ave_time : 0 }]-(b)"
    query_plane1_relation ="MATCH (a:"+level+"),(b:PlaneStation) WHERE a.name = b.name CREATE (a)<-[r:route { min_price: 0, price : 0, ave_price : 0 ,min_time: 0, time : 0, ave_time : 0 }]-(b)"

    #1 :node, 3 : tên , 5 :lat , 7 :lng , 9 : long_name, 11: short_name
    query_create[1] = name.replace(" ","").replace("-","_")
    query_create[3] = name
    query_create[5] = lat 
    query_create[7] = lng
    query_create[9] = long_name
    query_create[11] = short_name

    query_car[1] = name.replace(" ","").replace("-","_").replace("-","_")+'_car'
    query_car[3] = name
    query_car[5] = long_name
    query_car[7] = short_name

    query_train[1] = name.replace(" ","").replace("-","_").replace("-","_")+'_train'
    query_train[3] = name       
    query_train[5] = long_name
    query_train[7] = short_name


    query_plane[1] = name.replace(" ","").replace("-","_").replace("-","_")+'_plane'
    query_plane[3] = name
    query_plane[5] = long_name
    query_plane[7] = short_name

    print(''.join(query_car))
    graphDB_Session.run(''.join(query_create))

    graphDB_Session.run(''.join(query_plane))
    graphDB_Session.run(''.join(query_train))
    graphDB_Session.run(''.join(query_car))
    graphDB_Session.run(query_car_relation)
    graphDB_Session.run(query_car1_relation)
    graphDB_Session.run(query_train_relation)
    graphDB_Session.run(query_train1_relation)
    graphDB_Session.run(query_plane_relation)
    graphDB_Session.run(query_plane1_relation)


collection = 'region1'
c = 'test'
# s = list(db[collection].find({}))
# print(len(s))

import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyD4n_B9MKx7XooJ6kaXkLFe-JMPhkVMsGg')

# s = ['Hà Nội','Thành phố Hồ Chí Minh','Hải Phòng','Cần Thơ','Đà Nẵng']
# for station in s:
geocode_result = gmaps.geocode(m)

x = (get_level(reversed(geocode_result[0]['address_components'])))
print(x)
# match (lv1:administrative_area_level_1) -[:parent]-(lv2:lv2 {long_name :'HaNoi'}) return lv2
with driver.session() as graphDB_Session:
    geocode_string = " x['administrative_area_level_1']"
    query = "match (lv1:administrative_area_level_1 {long_name :'"+ x['administrative_area_level_1']+"'})"
    for i in range(2,len(x)+1):
        query +=  "-[:parent]-(lv'"+str(i)+"':level_"+str(i)+"{long_name:'"+x['level_'+str(i)]+"')"
        results = graphDB_Session.run(query + "return lv"+str(i))
        records = []
        for record in results:
            records.append(record)
            if(len(record == 0)):
                geocode_string = x['level_'+str(i)] +', '+ geocode_string
                info = gmaps.geocode(geocode_string)[0]
                long_name = info['address_components'][0]['long_name']
                short_name = info['address_components'][0]['short_name']
                lat = info['geometry']['location']['lat']
                lng = info['geometry']['location']['lng']






