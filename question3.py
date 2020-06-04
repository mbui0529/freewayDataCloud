"""
3. Find travel time for station Foster NB for 5-minute intervals for Sept 22, 2011.
"""
from utility import round_up_five_minutes
from connectmongo import loop, stations
import time
import re

location = 'Foster NB'
date = '2011-09-22'
start = time.time()
pat = re.compile(r'{}'.format(date),re.I)  # regex

# Get length from stations because stations collection is much smaller than loop:
street_length_find = stations.find({'locationtext':location},{'length':1})
street_length = 0 # This length use for 3 & 4 question
for p in street_length_find:
    street_length = p['length']  # miles

speed_in_one_day = loop.find({'$and':[{'locationtext':location},{'starttime':{'$regex':pat}}]},{'speed':1,'starttime':1}).sort('starttime')

speed_list = {}
speed_count = {}

for d in speed_in_one_day:
    t = round_up_five_minutes(d['starttime'])
    if d['speed'] or d['speed'] == 0:
        if t not in speed_list:
            speed_list[t] = 0
            speed_count[t] = 0
        speed_list[t] += int(d['speed'])
        speed_count[t] += 1
end = time.time()

print ("Question 3:")
for s in speed_list:
    average_speed = speed_list[s]/speed_count[s]
    if average_speed != 0:
        result = round((street_length/average_speed) * 3600,2)
        result = str(result)
    else:
        result = ''
    print("Average travel time at {} is {} second(s)".format(s,result))

#print("Execution time: {}".format(end-start))

print("\n")