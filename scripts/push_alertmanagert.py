#!/usr/bin/python
import os
import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('config_file', help='config file to push.')
parser.add_argument('-s', '--consul_host_port', help='consul host address:port.', default='localhost:8500')
args = parser.parse_args()

CONSUL_BASE_URL = 'http://%s/v1/kv/' % args.consul_host_port
CONSUL_BASE_KEY = 'monitoring/configs/alertmanager'

def main():
  base_file_name = os.path.basename(args.config_file)
  print '=== About to push configs for %s service ===' % base_file_name
  consul_key_path = CONSUL_BASE_URL+CONSUL_BASE_KEY
  print '=== Pushing to consul key %s ===' % consul_key_path
 
  data = None
  with open(args.config_file) as f:
    data = f.read()

  url = consul_key_path
  r = requests.put(url, data=data)
  if r.status_code != 200:
    print 'Return status is non 200.'  
    return
  print 'Done.'

if __name__ == '__main__':
 main()
