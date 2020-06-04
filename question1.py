"""
1. Count high speeds: Find the number of speeds > 100 in the data set.
"""
from connectmongo import loop

count_high_speed_one_hour = loop.count_documents({'speed': {'$gt': 100}})  # cannot use > in mongoDB

print("Question 1:")
print("Count high speed in data: {}\n".format(count_high_speed_one_hour))