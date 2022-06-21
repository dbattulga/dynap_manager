from __future__ import absolute_import, annotations

import grequests
import time
import random
import json
import requests
import csv
import os

file1 = open('../results/migration_result.csv', 'a+')
writer = csv.writer(file1)
if os.stat("../results/migration_result.csv").st_size == 0:
    writer.writerow(["migration_start", "migration_end"])


def migrate(urls: list):
    """
    gets the list of json data of the migration of the jobs
        "address_from": "192.168.1.4",
        "address_to": "192.168.1.5",
        "job_id": "uuid"
    sends migration request asynchronously
    """
    results = []
    for job in urls:
        job_id = job.get("job_id")
        data = {"migration_address": job.get("address_to")}
        # TODO change mock to migrate
        # url = "http://" + job.get("address_from") + ":5001/mock/" + job_id
        url = "http://" + job.get("address_from") + ":5001/migrate/" + job_id
        results.append(grequests.post(url, json=data))
    res = grequests.map(results)
    print(res)


def get_available_task_slots(agent_address: str) -> int:
    """
    get available task slots from certain agent
        not used for now. Assume there's only one job running on each agent
    """
    url = 'http://' + agent_address + ":5001/taskslots"
    print(f"Getting available task slots from: {url}")
    req = requests.get(url)
    data = req.json()
    slots = data.get("slots_available")
    print(slots)
    return slots


def select_jobid(agent_address: str) -> str:
    """
    from a single agent address
        select a single job from multiple jobs
            should be one with lower sequence number
            should not be migrating
            chose randomly if sequence number is the same
    send back only one jobid
    """
    url = 'http://' + agent_address + ":5001/job"
    print(f"Getting running jobs from: {url}")
    req = requests.get(url)
    jobs = req.json()

    if len(jobs):
        candidate_job = jobs[0]
        for job in jobs:
            if not job.get("requesting_cs") and job.get("sequence_number") <= candidate_job.get("sequence_number"):
                candidate_job = job
        return candidate_job.get("job_id")
    else:
        print(f"Error! No running job on {agent_address}")
        return "no_job"


def prepare_migration(nodes: list, job_count: int) -> list:
    """
    gets agent addresses with related latency, and length of a list (how many jobs to migrate per round)
    ask some nodes their job is available for migration,
    ask some lower latency nodes for their availability
    returns list of json data for migration
    """

    migrate_from = random.choice(nodes)
    migrate_to = random.choice(nodes)
    urls = []
    if int(migrate_to["role"]) <= int(migrate_from["role"]) and migrate_to["host"] != migrate_from["host"]:
        job_id = select_jobid(migrate_from["host"])
        if job_id != "no_job":
            job = {
                "address_from": migrate_from["host"],
                "address_to": migrate_to["host"],
                "job_id": job_id
            }
            urls.append(job)
    return urls


def main():

    with open('../nodes_list.json') as f:
        data = json.load(f)
    nodes = data["nodes"]
    eligible_nodes = []
    for node in nodes:
        if node["role"] == "start" or node["role"] == "end":
            pass
        else:
            eligible_nodes.append(node)

    test_duration = 1200  # SECONDS
    next_migration_duration_from = 30  # SECONDS
    next_migration_duration_to = 40  # SECONDS
    start_time = time.time()
    end_time = start_time + test_duration

    # while True:
    #     next_run = random.randint(next_migration_duration_from, next_migration_duration_to)
    #     print(f"next run will be in {next_run} seconds")
    #     time.sleep(next_run)
    #
    #     migration_data = prepare_migration(eligible_nodes, 1)
    #     if len(migration_data):
    #         print(migration_data)
    #         ts1 = time.time()
    #         migrate(migration_data)
    #         ts2 = time.time()
    #         timestamps = [str(ts1), str(ts2)]
    #         writer.writerow(timestamps)
    #     else:
    #         print("no eligible node is chosen")
    #
    #     if time.time() > end_time:
    #         print(f"{test_duration} seconds is ended")
    #         break


    migration_data = prepare_migration(eligible_nodes, 1)
    if len(migration_data):
        print(migration_data)
        ts1 = time.time()
        migrate(migration_data)
        ts2 = time.time()
        timestamps = [str(ts1), str(ts2)]
        writer.writerow(timestamps)
    else:
        print("no eligible node is chosen")


if __name__ == "__main__":
    main()
