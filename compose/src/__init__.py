import markdown
import os
import shelve
import logging
import json
import uuid
import requests
import socket
import time
from threading import Lock

from flask import Flask, g, redirect, render_template, url_for
from flask_restful import Resource, Api, reqparse
from flask import request
from flask.logging import create_logger
from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from flask import jsonify
from . import net_graph
from bokeh.embed import components



logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
api = Api(app)
log = create_logger(app)


@app.route("/")
def index():
    """Present some documentation"""
    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:
        content = markdown_file.read()
        return markdown.markdown(content)


@app.route('/status', methods=['GET'])
def stat_request():
    #ipaddr = '10.188.166.98'
    ipaddr = '131.254.161.252'
    res = requests.get("http://"+ipaddr+":5001/stat_response")
    if res.status_code == 200:
        log.debug(res)
        log.debug(res.headers)
        log.debug(res.content)
        log.debug(res.status_code)
        #log.debug(res.content['data'])
        jason = json.loads(res.content)
        log.debug(jason['data'])

        headings = ('jobname', 'node', 'status')
        data = (
            ('job A', 'node X', 'running'),
            ('job B', 'node Y', 'waiting'),
            ('job C', 'node Z', 'running'),
            ('job A', 'node X', 'running'),
            ('job B', 'node Y', 'waiting'),
            ('job C', 'node Z', 'running')
        )
        
        return render_template('table.html', headings=headings, data=data)

        #return {'message': 'Success'}, 200
    return {'message': 'Failed'}, 500


@app.route('/graph', methods=['GET'])
def draw_graph():
    shelf = get_db()
    plot = net_graph.draw_graph(shelf)
    script, div = components(plot)
    return render_template("graph.html", script=script, div=div)


#def test_job():
#    log.debug("I'm fencing")


def test_job():
    with open(os.path.dirname(app.root_path) + '/config/iplist.txt', 'r') as iplist:
        lines = iplist.readlines()
    
    for line in lines:
        log.debug(line)


#scheduler = BackgroundScheduler()
#job = scheduler.add_job(test_job, 'interval', minutes=0.1)
#scheduler.start()