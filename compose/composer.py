import yaml
import json
import requests
import datetime as dt


def run_conf():
    with open('../conf/pipeline.yml') as f:
        userconf = yaml.load(f)
    userjobs = []
    for userjob in userconf['jobs']:
        userjobs.append(userjob['job_name'])
        print("post: "+userjob['job_name'])

        url = userjob['agent_address']

        body = {'pipeline_name': userjob['pipeline_name'],
            'job_name': userjob['job_name'],
            'agent_address': userjob['agent_address'],
            'source_broker': userjob['source_broker'],
            'sink_broker': userjob['sink_broker'],
            'source_topic': userjob['source_topic'],
            'sink_topic': userjob['sink_topic'],
            'entry_class': userjob['entry_class']
            }
        
        files = [
            ('jar', ('test.jar', open(userjob['job_path'], 'rb'), 'application/octet')),
            ('data', ('data', json.dumps(body), 'application/json')),
        ]
        
        req = requests.post(url + ":5001/upload", files=files)
        print(req)


run_conf()