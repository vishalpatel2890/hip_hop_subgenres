import boto3
import botocore
import logging
import time
from bs4 import BeautifulSoup
import json
import requests


log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
logging.basicConfig(
	level=logging.INFO,
	format="%(asctime)s - %(name)s (%(lineno)s) - %(levelname)s: %(message)s",
	datefmt='%Y.%m.%d %H:%M:%S')

def get_artist_id(artist):
    req = requests.get(f"http://www.genius.com/artists/{artist}")
    soup = BeautifulSoup(req.content, 'html.parser')
    meta = soup.find('meta', {'name':'newrelic-resource-path'})
    path = meta.get('content')
    return path

def get_artist_albums_data(artist):
    path = get_artist_id(artist)
    full_path = f'http://www.genius.com/api{path}/albums'
    req = requests.get(full_path)
    return json.loads(req.content)

def get_artist_albums_urls(artist):
    artist_data = get_artist_albums_data(artist)
    urls = [album['url'] for album in artist_data['response']['albums']]
    return urls

import boto3
import botocore
import logging
import time
from bs4 import BeautifulSoup
import json
import requests


log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
logging.basicConfig(
	level=logging.INFO,
	format="%(asctime)s - %(name)s (%(lineno)s) - %(levelname)s: %(message)s",
	datefmt='%Y.%m.%d %H:%M:%S')

def get_artist_id(artist):
    req = requests.get(f"http://www.genius.com/artists/{artist}")
    soup = BeautifulSoup(req.content, 'html.parser')
    meta = soup.find('meta', {'name':'newrelic-resource-path'})
    path = meta.get('content')
    return path

def get_artist_albums_data(artist):
    path = get_artist_id(artist)
    full_path = f'http://www.genius.com/api{path}/albums'
    req = requests.get(full_path)
    return json.loads(req.content)

def get_artist_albums_urls(artist):
    artist_data = get_artist_albums_data(artist)
    urls = [album['url'] for album in artist_data['response']['albums']]
    return urls

def lambda_handler(event, context):
	log.info("Boto3 Version: " + boto3.__version__)
	log.info("Botocore Version: " + botocore.__version__)
	urls = get_artist_albums_urls('Jay-Z')

	sqs = boto3.resource('sqs')
	queue = sqs.get_queue_by_name(QueueName='test-messages')
	for url in urls:
		response = queue.send_message(MessageBody=url)

    # log.info(response)
	return  len(urls)
