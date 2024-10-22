import os
import http.client
import json
import logging
from jwt import decode, PyJWKClient, exceptions
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Initialize logging for error tracing
logging.basicConfig(level=logging.DEBUG)

# Set up the connection
conn = http.client.HTTPConnection("localhost:5000")

# JWT (Bearer) token provided
ASSISTANT_TOKEN=os.environ.get('ASSISTANT_TOKEN')
DIRECTOR_TOKEN=os.environ.get('CASTING_DIRECTOR_TOKEN')
PRODUCER_TOKEN=os.environ.get('EXECUTIVE_PRODUCER_TOKEN')
token = ASSISTANT_TOKEN
print(token)

headers = {
    'authorization': f'Bearer {token}'
}

# Endpoint for the Auth0 JWKS
jwks_url = "https://dev-8his2amisscpohz8.us.auth0.com/.well-known/jwks.json"

try:
    conn.request("GET", "/actors", headers=headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
except Exception as e:
    logging.error(f"Error during HTTP request: {e}")