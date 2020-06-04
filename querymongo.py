# pprint library is used to make the output look more pretty
from pprint import pprint
from utility import round_up_five_minutes,convert_string
from connectmongo import freeway,loop,stations
import re

# Hyper parameter
location = 'Foster NB'
# answer question
"""
1. Count high speeds: Find the number of speeds > 100 in the data set.
"""
count_high_speed_one_hour = loop.count_documents({'speed': {'$gt': 100}})  # cannot use > in mongoDB
print("Question 1:")
print("Count high speed in one hour: {}\n".format(count_high_speed_one_hour))

"""
2. Volume: Find the total volume for the station Foster NB for Sept 21, 2011.
"""

date = '2011-09-21'

pat = re.compile(r'{}'.format(date),re.I)
condition = [{'locationtext':location},{'starttime':{'$regex':pat}}]
pipe = [{'$match': {'$and': condition}},{'$group': {'_id': None,'total': {'$sum': '$volume'}}}]
forster_sept_21_2011_volume = loop.aggregate(pipe)

print("Question 2:")
for p in forster_sept_21_2011_volume:
    print("The total volume in {} at {}: {}\n".format(date,location,p['total']))

"""
3. Find travel time for station Foster NB for 5-minute intervals for Sept 22, 2011.
"""

date = '2011-09-22'

# Get length from stations because stations collection is much smaller than loop:
street_length_find = stations.find({'locationtext':location},{'length':1})
street_length = 0 # This length use for 3 & 4 question
for p in street_length_find:
    street_length = p['length']  # miles

speed_in_one_day = loop.find({'$and':[{'locationtext':location},{'starttime':{'$regex':pat}}]},{'speed':1,'starttime':1}).sort('starttime')

speed_list = {}
speed_count = {}

for d in speed_in_one_day:
    time = round_up_five_minutes(d['starttime'])
    if d['speed'] or d['speed'] == 0:
        if time not in speed_list:
            speed_list[time] = 0
            speed_count[time] = 0
        speed_list[time] += int(d['speed'])
        speed_count[time] += 1


print ("Question 3:")
for s in speed_list:
    average_speed = speed_list[s]/speed_count[s]
    if average_speed != 0:
        result = round((street_length/average_speed) * 3600,2)
        result = str(result)
    else:
        result = ''
    print("Average travel time at {} is {} second(s)".format(s,result))

print("\n")

"""
4. Peak Period Travel Times: Find the average travel time for 7-9AM and 4-6PM
on September 22, 2011 for the Foster NB. Report travel time in minutes.
"""
date = '2011-09-22'
start_time_am = '07:00:00'
end_time_am = '09:00:00'
start_time_pm = '16:00:00'
end_time_pm = '18:00:00'
time_string = ['7-9AM','4-6PM']
average_travel_speed = {}

# Extract average speed data from loop.
pipe = [{'$match': {'$and':[{'locationtext':location},
                            {'starttime': {'$gte': '{} {}'.format(date,start_time_am)}},
                            {'starttime': {'$lt': '{} {}'.format(date,end_time_am)}}]}}, {'$group': {'_id': None,'average_speed': {'$avg': '$speed'}}}]
average_travel_foster_find= loop.aggregate(pipe)

for d in average_travel_foster_find:
    average_travel_speed['7-9AM'] = d['average_speed']  # mph

pipe = [{'$match': {'$and':[{'locationtext':location},
                           {'starttime': {'$gte': '{} {}'.format(date,start_time_pm)}},
                            {'starttime': {'$lt': '{} {}'.format(date,end_time_pm)}}]}}, {'$group': {'_id': None,'average_speed': {'$avg': '$speed'}}}]
average_travel_foster_find= loop.aggregate(pipe)

for d in average_travel_foster_find:
    average_travel_speed['4-6PM'] = d['average_speed']  # mph

print ("Question 4:")
for t in time_string:
    if t in average_travel_speed:
        result = round(street_length / average_travel_speed[t] * 3600, 2)
        print_string = 'Travel time for {}: {} seconds'.format(t, result)
        print(print_string)
    else:
        print('Result Not Found')


