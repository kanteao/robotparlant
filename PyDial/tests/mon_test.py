import requests
r = requests.post('http://localhost:8082/newcall?', data='{"session":"wesh"}')
print r
while(True):
	i = raw_input("Say :")
	if (i == 'q'):
		break
	r = requests.post('http://localhost:8082/next?', data='{"session":"wesh", "result":{"resultType":"Partial","alts":[{"transcript":"' + i + '", "confidence":1}]} }')
	print r.json()['text']