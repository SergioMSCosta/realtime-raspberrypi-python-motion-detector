import ortc, requests, json, re

APP_KEY = 'YOUR_APP_KEY'
PVT_KEY = 'YOUR_PRIVATE_KEY'
AUTHENTICATION_TOKEN = 'your_random_token_here'
CHANNEL = 'motion:cam1'
BALANCER_URL = 'https://ortc-developers.realtime.co/server/2.1/'

# First we need to get the ORTC datacenter with the best latency for us
# To do so, we perform a GET request to the balancer server
req = requests.get(BALANCER_URL)

# If everything goes ok we'll get the string 'var SOCKET_SERVER = "http://ortx-developers-xxxx-xxxx.realtime.co";'
# Obviously, we're only interested in the server address, so we need to extract it. Regular expressions are our friend!
ortc_url_match = re.search('var SOCKET_SERVER = "(.+?)";', req.text)

if ortc_url_match:
	# Right on, we seem to have our server address
	ortc_url = ortc_url_match.group(1)
	print('Got server: ' + ortc_url);

	# All right, it's time to send our message then
	# In case we have authentication enabled on ORTC, we'll need to authenticate first
	# We do so by performing a POST request to the ORTC server that was provided to us by the balancer
	# If you don't have authentication enabled, you can ignore the next lines
	# For this request, we will need to send some data
	print('Authorizing')
	payload = {"AK": APP_KEY, "PK": PVT_KEY, "AT": AUTHENTICATION_TOKEN, "PVT": 0, "TTL": 3600, "TP": "1", "Channel": CHANNEL + "=w"}
	req = requests.post(ortc_url + '/authenticate/', payload)
	print 'Authorization response: ' + req.text
    
    # So did we get authorized?
	if 'Created' in req.text:
		# Seems like it! We're good to go!
		print('Authorization OK')

		# Let's send our message then!
		print('Sending message')
		payload = {"AK": APP_KEY, "PK": PVT_KEY, "AT": AUTHENTICATION_TOKEN, "C": CHANNEL, "M": "HELLO WORLD!"}
		req = requests.post(ortc_url + '/send/', payload)
		print(req.text)

	else:
		# Something went wrong with the authorization
		print('Authorization NOT OK')

else:
	# Uh-oh...?
	print("Seems like we have no server...?")