#!/usr/bin/python

##############################################################################################################################################

##	Description: Retrieving public ip's of AWS instances from VMware CloudHealth

##	Version: 1.0

##	Basic usage: ./aws_instances.py

##	Verbose mode: ./aws_instances.py -v

##	Author: Alvaro Trigo

#############################################################################################################################################

import urllib3
import json
import argparse
import sys
import subprocess
import csv
import time

## Defining arguments

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', help='Verbose mode', action='store_true')
args = parser.parse_args()

## Disabling https warnings

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

## Configuring csv

timestamp = str(time.time())
timestamp = timestamp[:(len(timestamp))-3]
if(args.verbose):
	myData = [['public_ip','private_ip','dns','is_active','name','created_at','instance_id']]
else:
	myData = [['public_ip']]
myFile = open('aws_instances_' + timestamp + '.csv', 'w')
with myFile:
	writer = csv.writer(myFile)
	writer.writerows(myData)

## Configuring request

headers = {'Authorization':'Bearer <YOUR_API_KEY>'}
fields={'api_version': '2','name': 'AwsInstance', 'page': '1', 'per_page': '500', 'query': 'is_active=1'}

http = urllib3.PoolManager()

r = http.request('GET', 'https://chapi.cloudhealthtech.com/api/search', headers=headers, fields=fields)
json_data = json.loads(r.data.decode('utf-8'))
for data in json_data:
	if(str(data['ip']) != 'None' and str(data['is_active']) == 'True'):
		if(args.verbose):
			myData = [[str(data['ip']),str(data['private_ip']),str(data['dns']),str(data['is_active']),str(data['name']),str(data['created_at']),str(data['instance_id'])]]
			myFile = open('aws_instances_' + timestamp + '.csv', 'a')
			with myFile:
				writer = csv.writer(myFile)
				writer.writerows(myData)
			print(str(data['ip']) + ',' + str(data['private_ip']) + ',' + str(data['dns']) + ',' + str(data['is_active']) + ',' + str(data['name']) + ',' + str(data['created_at']) + ',' + str(data['instance_id']))
		else:
			myData = [[str(data['ip'])]]
			myFile = open('aws_instances_' + timestamp + '.csv', 'a')
			with myFile:
				writer = csv.writer(myFile)
				writer.writerows(myData)
			print(str(data['ip']))
