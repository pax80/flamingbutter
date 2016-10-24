import requests
import logging
from settings import neo4j_url
import py2neo

import settings

def make_request(from_node, to_node):
    port_url = neo4j_url + '/' + from_node.ref + '/paths'
    request_body = {
        "to": str(to_node.resource.uri),  # destination node uri
        "cost_property": "metric",  # name of cost property
        "relationships": {
            "type": "LINK",  # relationship type
            "direction": "out"
        },
        "algorithm": "dijkstra"
    }
    result = requests.post(port_url, json=request_body)
    if result.status_code == 200:
        response = result.json()
        return response
    logging.error('SPF Error, code %s, message %s', result.status_code, result.content)





if __name__ == '__main__':
    """ this is to test the spf between 2 nodes"""
    graph = py2neo.Graph(neo4j_url)
    routers = {}
    start_node = graph.find_one('Router', property_key='name', property_value='ie-dub01a-ri1-re0.00')
    routers['src'] = start_node
    end_node = graph.find_one('Router', property_key='name', property_value='nl-ams09b-ri1-re0.00')
    routers['dst'] = end_node
    r = make_request(start_node, end_node)
    print("done {}".format(r))