#
# This file is now defunct, since I didn't end up using the 
# ETH Zurich python dataset, since it didn't contain any
# python code with type annotations
#
# Leaving in the repo just to show an attempt was made.
#
import pandas as pd
import ijson

JSON_FILE = 'dataset/python100k_train.json'

parser = ijson.parse(open(JSON_FILE))

count = 0
print('prefix :: event :: value')
for prefix, event, value in parser:
    count += 1
    if count >= 500:
        break
    print(f'{prefix} :: {event} :: {value}')