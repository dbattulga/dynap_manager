from __future__ import absolute_import, annotations

import grequests
import string
import time
import random
import json
import requests
import os
import json
from pprint import pprint


def prepare_nodes_to_deploy(nodes: list) -> list:
    """
    gets list of node info
    prepares nodes in order for deployment
        start
        shuffle with various ping
        end
    """
    shuffle_nodes = []
    ordered_nodes = []
    start_node = None
    end_node = None
    for node in nodes:
        if node["role"] == "start":
            start_node = node
        elif node["role"] == "end":
            end_node = node
        else:
            shuffle_nodes.append(node)
    random.shuffle(shuffle_nodes)
    ordered_nodes.append(start_node)
    for node in shuffle_nodes:
        ordered_nodes.append(node)
    ordered_nodes.append(end_node)
    print(f"start node: \n{start_node['host']}")
    print(f"end node: \n{end_node['host']}")
    return ordered_nodes


def prepare_job_dict(job_name: str, agent_address: str, upstream_address: str, downstream_address: str,
                     upstream_topic: str, downstream_topic: str) -> dict:
    """
    to_repr type of method of preparing job description dict
    """
    data = {
        "job_name": job_name,
        "agent_address": agent_address,
        "entry_class": "agentpackage.MultiSourceTest",
        "upstream": [
            {
                "address": upstream_address,
                "topic": upstream_topic,
                "sequence_number": 0,
                "requesting_cs": False
            }
        ],
        "downstream": [
            {
                "address": downstream_address,
                "topic": downstream_topic,
                "sequence_number": 0,
                "requesting_cs": False
            }
        ],
        "sequence_number": 0
    }
    return data


def prepare_jobs_to_deploy(nodes: list) -> list:
    """
    from list of nodes
    builds a list of job dictionary desctiption with
        assigning a unique job names, and topic names
    """
    jobs = []
    for i in range(len(nodes)):
        count = i + 1
        job_name = string.ascii_uppercase[i] + "_JOB"
        agent_address = nodes[i]["host"]
        upstream_topic = "T-" + str(count)
        downstream_topic = "T-" + str(count+1)
        if i == 0:
            upstream_address = nodes[i]["host"]
        else:
            upstream_address = nodes[i-1]["host"]
        if i != len(nodes)-1:
            downstream_address = nodes[i+1]["host"]
        else:
            downstream_address = nodes[i]["host"]
        job_dict = prepare_job_dict(job_name, agent_address, upstream_address, downstream_address, upstream_topic, downstream_topic)
        jobs.append(job_dict)
    return jobs


def deploy_jobs(userjobs: list):
    """
    gets a dict description of a job and deploys it on an agent
    """
    results = []
    for userjob in userjobs:
        absolute_path = os.path.dirname(os.path.abspath(__file__))
        print(f"deploying a job on: {absolute_path}")

        url = 'http://' + userjob['agent_address'] + ":5001/job"
        print(f"posting: {userjob['job_name']} on {url}")
        files = [
            ('file', ('test.jar', open(f"{absolute_path}/flinktest-1.jar", 'rb'), 'application/java-archive'))
        ]
        results.append(grequests.post(url, files=files, data={"data": json.dumps(userjob)}))
        #req = requests.post(url, files=files, data={"data": json.dumps(userjob)})
    res = grequests.map(results)
    print(res)


def main():

    with open('../nodes_list.json') as f:
        data = json.load(f)
    nodes = data["nodes"]

    ordered_nodes = prepare_nodes_to_deploy(nodes)
    jobs = prepare_jobs_to_deploy(ordered_nodes)
    pprint(jobs)
    deploy_jobs(jobs)


if __name__ == "__main__":
    main()
