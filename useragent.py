'''By default the function returns desktop user agents
	Arguments:
	type = "mobile" to get mobile useragents
'''
import json
import random
import os
ua = json.load(open(os.path.join(os.path.dirname(__file__),'useragents.json')))

def get_ua(type='web'):		
	# print(random.choice(ua[type]))
	return random.choice(ua[type])