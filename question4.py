"""
4. Peak Period Travel Times: Find the average travel time for 7-9AM and 4-6PM
on September 22, 2011 for the Foster NB. Report travel time in minutes.
"""
from connectmongo import freeway,loop,stations
import re

date = '2011-09-22'
location = 'Foster NB'

start_time_am = '07:00:00'
end_time_am = '09:00:00'
start_time_pm = '16:00:00'
end_time_pm = '18:00:00'
time_string = ['7-9AM','4-6PM']
average_travel_speed = {}

# Get length from stations because stations collection is much smaller than loop:
street_length_find = stations.find({'locationtext':location},{'length':1})
street_length = 0 # This length use for 3 & 4 question
for p in street_length_find:
    street_length = p['length']  # miles

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


