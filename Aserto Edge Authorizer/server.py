#!/usr/bin/env python
"""
Example library for wrapping the opa.py library with a Flask API. Modified to conform to 
T4 use cases. Source: https://github.com/open-policy-agent/contrib/tree/main/data_filter_example
"""
import requests

import flask
from flask_bootstrap import Bootstrap

import opa

app = flask.Flask(__name__, static_url_path='/static')
Bootstrap(app)

@app.route('/api/nomination/check', methods=["POST"])
def api_check_nominations():
    input = flask.request.get_json(force=True)
    url = 'https://localhost:8383/api/v2/authz/is'
    body = {
        "identity_context": {
            "identity": "bob",
            "type": "IDENTITY_TYPE_NONE"
        },
        "policy_context": {
            "decisions": [
                "allow"
            ],
            "path": "rebac.check"
        },
        "policy_instance": {
            "instance_label": "policy-poc",
            "name": "policy-poc"
        },
        "resource_context": input
    }

    edge_response = requests.post(url, json = body, verify=False)

    return edge_response.json()

@app.route('/api/nomination/search', methods=["POST"])
def api_search_nominations():
    input = flask.request.get_json(force=True)
    result = invoke_search(input, "nominations")
    return flask.jsonify(result)

@app.route('/api/ticket/search', methods=["POST"])
def api_search_tickets():
    input = flask.request.get_json(force=True)
    result = invoke_search(input, "tickets")    
    return flask.jsonify(result)
def invoke_search(input, unknown):
    url = 'https://localhost:8383/api/v2/authz/compile'
    body = {
        "identity_context": {
            "identity": "bob@transport4.com",
            "type": "IDENTITY_TYPE_NONE"
        },
        "options": {
            "instrument": False,
            "metrics": False,
            "trace": "TRACE_LEVEL_UNKNOWN",
            "trace_summary": False
        },
        "policy_context": {
            "decisions": [
                "allow"
            ],
            "path": "rebac.check"
        },
        "policy_instance": {
            "instance_label": "policy-poc",
            "name": "policy-poc"
        },
        "query": "data.rebac.check.allow==true",
        "resource_context": input,
        "unknowns": [
            "data." + unknown
        ]
    }

    edge_response = requests.post(url, json = body, verify=False)
    queries_result = opa.generate_queries(body=edge_response.json())
       
    if not queries_result.defined:
        return {'allowed': False}
    
    if queries_result.defined and queries_result.sql is None:
        return {'allowed': True, 'sql': None}
    
    return {
        'allowed': queries_result.defined,
        'sql': queries_result.sql.clauses[0].sql()
    }

@app.teardown_appcontext
def close_connection(e):
    db = getattr(flask.g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
