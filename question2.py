"""
2. Volume: Find the total volume for the station Foster NB for Sept 21, 2011.
"""
from connectmongo import loop
import re

# Hyper parameter
location = 'Foster NB'
date = '2011-09-21'

pat = re.compile(r'{}'.format(date),re.I)
condition = [{'locationtext':location},{'starttime':{'$regex':pat}}]
pipe = [{'$match': {'$and': condition}},{'$group': {'_id': None,'total': {'$sum': '$volume'}}}]
forster_sept_21_2011_volume = loop.aggregate(pipe)

print("Question 2:")
for p in forster_sept_21_2011_volume:
    print("The total volume in {} at {}: {}\n".format(date,location,p['total']))