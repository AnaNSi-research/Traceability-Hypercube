import argparse
import sys
from flask import Flask, request, abort

from config import *
from node import Node, requests
from utils import INSERT, REMOVE, PIN_SEARCH, SUPERSET_SEARCH

app = Flask(APP_NAME)


@app.route(INSERT)
def request_insert():
    app.logger.info("Insert request")
    keyword = request.args.get('keyword')
    if(keyword is None):
        abort(400)

    obj = request.args.get('obj')
    if(obj is None):
        abort(400)
    
    keyword = int(keyword)    
    res = NODE.insert(keyword, obj)
    if type(res) is not str:
        res = res.text
    return res


@app.route(REMOVE)
def request_remove():
    keyword = int(request.args.get('keyword'))
    obj = request.args.get('obj')
    res = NODE.remove(keyword, obj)
    if type(res) is not str:
        res = res.text
    return res


@app.route(PIN_SEARCH)
def request_pin_search():
    keyword = int(request.args.get('keyword'))
    threshold = request.args.get('threshold')
    if threshold is None:
        res = NODE.pin_search(keyword)
    else:
        res = NODE.pin_search(keyword, int(threshold))
    if type(res) is not list:
        res = res.text
    else:
        res = ','.join(res)
    return res


@app.route(SUPERSET_SEARCH)
def request_superset_search():
    keyword = int(request.args.get('keyword'))
    threshold = int(request.args.get('threshold'))
    sender = request.args.get('sender')
    res = NODE.superset_search(keyword, threshold, sender)
    if type(res) is not list:
        res = res.text
    else:
        res = ','.join(res)
    return res


def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'port', type=int, help='Port number to which connect the node')
    return parser.parse_args(argv)


if __name__ == '__main__':
    PORT = parse_arguments(sys.argv[1:]).port
    print("PORT: ", PORT)
    NODE_ID = PORT - INIT_PORT
    NODE = Node(NODE_ID)
    app.run(host=LOCAL_HOST, port=PORT, threaded=True, debug=True)
