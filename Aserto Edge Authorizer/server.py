#!/usr/bin/env python
"""
Example library for wrapping the opa.py library with a Flask API. Modified to conform to 
T4 use cases. Source: https://github.com/open-policy-agent/contrib/tree/main/data_filter_example
"""
import requests
import flask
from flask_bootstrap import Bootstrap
from directory.user import User
from directory.user_permission import UserPermission
from directory.relation import Relation
from directory.company import Company
from directory.directory_connection import directory_connection
import opa

app = flask.Flask(__name__, static_url_path='/static')
Bootstrap(app)
relation = Relation(directory_connection)
user = User(directory_connection, relation)
user_permission = UserPermission(directory_connection, relation)

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

@app.route('/api/user', methods=["POST"])
def api_user_post():
    # Create user object
    # Create both identity objects
    # Create user_permission objects
    # Create pss_right objects
    # Create relations between all objects

    input = flask.request.get_json(force=True)
    
    created_user = user.create_user(
        user_id=input.get('user_id'),
        display_name=input.get('display_name'),
        email=input.get('email'),
        picture=input.get('picture'),
        pss_rights=input.get('pss_rights')
    )

    return flask.jsonify(
        {
            "user_created": created_user is not None,
            "user": created_user.id
        }
    )

@app.route('/api/user', methods=["DELETE"])
def api_user_delete():
    input = flask.request.get_json(force=True)
    user_id = input.get('user_id')
    result = user.delete_user(user_id=user_id)

    return flask.jsonify(
        {
            "user_deleted": result
        }
    )

@app.route('/api/user_permission', methods=["POST"])
def api_user_permission_post():
    input = flask.request.get_json(force=True)
    
    created_user_permission = user_permission.create_user_permission(
        company=input.get('company'),
        subscriber=input.get('subscriber'),
        locations=input.get('locations'),
        product_types=input.get('product_types'),
        role=input.get('role')
    )

    return flask.jsonify(
        {
            "user_permission_created": created_user_permission is not None,
            "user_permission": created_user_permission.id
        }
    )

@app.route('/api/user_permission', methods=["DELETE"])
def api_user_permission_delete():
    input = flask.request.get_json(force=True)
    user_permission_id = input.get('user_permission_id')
    result = user_permission.delete_user_permission(permission_id=user_permission_id)

    return flask.jsonify(
        {
            "user_permission_deleted": result
        }
    )

@app.route('/api/user_permission/grant', methods=["POST"])
def api_user_permission_grant():
    input = flask.request.get_json(force=True)
    
    result = user_permission.grant_user_permission(
        user_id=input.get('user_id'),
        user_permission_id=input.get('user_permission_id')
    )

    return flask.jsonify(
        {
            "user_permission_granted": result
        }
    )

@app.route('/api/user_permission/grant', methods=["DELETE"])
def api_user_permission_revoke():
    input = flask.request.get_json(force=True)
    
    result = user_permission.revoke_user_permission(
        user_id=input.get('user_id'),
        user_permission_id=input.get('user_permission_id')
    )

    return flask.jsonify(
        {
            "user_permission_revoked": result
        }
    )

@app.route('/api/company', methods=["POST"])
def api_company_post():
    input = flask.request.get_json(force=True)

    created_company = Company(directory_connection).create_company(
        company_id=input.get('company_id'),
        display_name=input.get('display_name')
    )
    
    return flask.jsonify(
        {
            "company_created": created_company is not None,
            "company": created_company.id
        }
    )

@app.route('/api/company', methods=["DELETE"])
def api_company_delete():
    input = flask.request.get_json(force=True)
    
    company_id = input.get('company_id')
    result = Company(directory_connection).delete_company(company_id)

    return flask.jsonify(
        {
            "company_deleted": result
        }
    )

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