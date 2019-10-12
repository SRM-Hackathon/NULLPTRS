import pandas as pd
#from fuzzywuzzy import process

item_db = pd.read_csv('items.csv')
#item_db[item_db['item_name']].str.match('musk')

test = item_db[item_db['item_name'].str.contains('Onion')]
print((test['sku']).to_string(index=False))
