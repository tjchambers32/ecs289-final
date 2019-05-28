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