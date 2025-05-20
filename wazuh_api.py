#!/usr/bin/env python3

import json
import requests
from requests.auth import HTTPBasicAuth
import urllib3
from base64 import b64encode
import datetime

#Disable insecure https warnings (for self-signed SSL certificates)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Configuration
protocol = 'https'
host = 'localhost'
today = datetime.datetime.now().strftime("%Y.%m.%d")
url = f"https://localhost:9200/wazuh-alerts-4.x-{today}/_search?pretty&size=10000&sort=timestamp:desc&q=rule.level:(7%20OR%208%20OR%209%20OR%2010%20OR%2011)"
auth = HTTPBasicAuth("admin", "SecretPassword")
port = 55000
user = 'wazuh-wui'
password = 'MyS3cr37P450r.*-'
login_endpoint = 'security/user/authenticate'

def connect():

    login_url = f"{protocol}://{host}:{port}/{login_endpoint}"
    basic_auth = f"{user}:{password}".encode()
    login_headers = {'Content-Type': 'application/json',
                    'Authorization': f'Basic {b64encode(basic_auth).decode()}'}


    print("\nLogin request ...\n")
    response = requests.post(login_url, headers=login_headers, verify=False)
    token = json.loads(response.content.decode())['data']['token']
    print(token)

    #New authorization header with the JWT we got
    requests_headers = {'Content-Type': 'application/json',
                        'Authorization': f'Bearer {token}'}
    return requests_headers


def api_info():
    requests_headers = connect()
    print("\n- API calls with TOKEN environment variable ...\n")

    print("Getting API information:")

    response = requests.get(f"{protocol}://{host}:{port}/?pretty=true", headers=requests_headers, verify=False)
    print(response.text)

    print("\nGetting agents status summary:")

    response = requests.get(f"{protocol}://{host}:{port}/agents/summary/status?pretty=true", headers=requests_headers, verify=False)
    print(response.text)

def get_agent_info():
    requests_headers = connect()
    print("\nGetting agents information:")

    response = requests.get(f"{protocol}://{host}:{port}/agents/?pretty=true", headers=requests_headers, verify=False)
    print(response.text)

    print("\nGetting API Configuration:")
    response = requests.get(f"{protocol}://{host}:{port}/manager/api/config?pretty=true", headers=requests_headers, verify=False)
    print(response.text)

def get_alerts_file():
    print("\nGetting Alert Events:")
    response = requests.get(url, auth=auth, verify=False)
    # Copy result to a file
    with open('syscheck_events.json', 'w') as f:
        f.write(response.text)


if __name__ == "__main__":
    get_alerts_file()
    print("Done")