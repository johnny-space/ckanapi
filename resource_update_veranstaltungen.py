import os
import argparse
import certifi
import requests
import json
from ckanapi import RemoteCKAN

# --- parse command-line args ---
parser = argparse.ArgumentParser(description="Update a CKAN resource via API")
parser.add_argument(
    "--apikey", "-k",
    required=True,
    help="Your CKAN API key"
)
parser.add_argument(
    "--file", "-f",
    required=True,
    help="Path to the file to upload"
)
args = parser.parse_args()

# --- build a session and force SSL off (dev only) ---
session = requests.Session()
session.verify    = False            # dev only; prod: certifi.where()
session.trust_env = True             # allow reading env vars

# --- only configure proxies if env-vars are non-empty ---
proxies = {}
if os.getenv("HTTP_PROXY"):
    proxies["http"] = os.environ["HTTP_PROXY"]
if os.getenv("HTTPS_PROXY"):
    proxies["https"] = os.environ["HTTPS_PROXY"]

if proxies:
    session.proxies = proxies

# --- connect to CKAN using provided key ---
ckan = RemoteCKAN(
    'https://opendata.muenchen.de',
    apikey=args.apikey,
    session=session
)

# --- resource metadata for update ---
resource_dict = {
    'id':         'b698829c-b051-4092-a276-9ba1afdc12f3',
    'package_id': 'ef068a1c-315c-4262-8cf1-903767831225',
    'name':       'Updated Resource Name',
    'format':     'CSV',
}

# --- perform the resource_update call with file upload ---
with open(args.file, 'rb') as fp:
    result = ckan.call_action(
        'resource_update',
        data_dict=resource_dict,
        files={'upload': fp}
    )

# --- pretty-print the response ---
print(json.dumps(result, indent=2, ensure_ascii=False))
