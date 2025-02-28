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
from directory.subscriber import Subscriber
from directory.action_set import ActionSet
from directory.role import Role
from directory.action import Action
from directory.directory_connection import directory_connection
import opa

app = flask.Flask(__name__, static_url_path='/static')
Bootstrap(app)
relation = Relation(directory_connection)
user = User(directory_connection, relation)
user_permission = UserPermission(directory_connection, relation)
company = Company(directory_connection)
subscriber = Subscriber(directory_connection, relation)
action_set = ActionSet(directory_connection, relation)
role = Role(directory_connection, relation)
action = Action(directory_connection)

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

@app.route('/api/user_permission/revoke', methods=["POST"])
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

    created_company = company.create_company(
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
    result = company.delete_company(company_id)

    return flask.jsonify(
        {
            "company_deleted": result
        }
    )

@app.route('/api/subscriber', methods=["POST"])
def api_subscriber_post():
    input = flask.request.get_json(force=True)

    created_subscriber = subscriber.create_subscriber(
        subscriber_id=input.get('subscriber_id'),
        display_name=input.get('display_name')
    )
    
    return flask.jsonify(
        {
            "subscriber_created": created_subscriber is not None,
            "subscriber": created_subscriber.id
        }
    )

@app.route('/api/subscriber', methods=["DELETE"])
def api_subscriber_delete():
    input = flask.request.get_json(force=True)

    subscriber_id = input.get('subscriber_id')
    result = subscriber.delete_subscriber(subscriber_id)

    return flask.jsonify(
        {
            "subscriber_deleted": result
        }
    )

@app.route('/api/subscriber/grant_action_set', methods=["POST"])
def api_subscriber_grant():
    input = flask.request.get_json(force=True)
    
    result = subscriber.grant_action_set(
        action_set_id=input.get('action_set_id'),
        subscriber_id=input.get('subscriber_id')
    )

    return flask.jsonify(
        {
            "action_set_granted": result
        }
    )

@app.route('/api/subscriber/revoke_action_set', methods=["POST"])
def api_subscriber_revoke():
    input = flask.request.get_json(force=True)
    
    result = subscriber.revoke_action_set(
        action_set_id=input.get('action_set_id'),
        subscriber_id=input.get('subscriber_id')
    )

    return flask.jsonify(
        {
            "action_set_revoked": result
        }
    )

@app.route('/api/action_set', methods=["POST"])
def api_action_set_post():
    input = flask.request.get_json(force=True)

    created_action_set = action_set.create_action_set(
        action_set_id=input.get('action_set_id'),
        display_name=input.get('display_name')
    )
    
    return flask.jsonify(
        {
            "action_set_created": created_action_set is not None,
            "action_set": created_action_set.id
        }
    )

@app.route('/api/action_set', methods=["DELETE"])
def api_action_set_delete():
    input = flask.request.get_json(force=True)

    action_set_id = input.get('action_set_id')
    result = action_set.delete_action_set(action_set_id)

    return flask.jsonify(
        {
            "action_set_deleted": result
        }
    )

@app.route('/api/action_set/grant_action', methods=["POST"])
def api_action_set_grant():
    input = flask.request.get_json(force=True)
    
    result = action_set.grant_action(
        action_id=input.get('action_id'),
        action_set_id=input.get('action_set_id')
    )

    return flask.jsonify(
        {
            "action_granted": result
        }
    )

@app.route('/api/action_set/revoke_action', methods=["POST"])
def api_action_set_revoke():
    input = flask.request.get_json(force=True)
    
    result = action_set.revoke_action(
        action_id=input.get('action_id'),
        action_set_id=input.get('action_set_id')
    )

    return flask.jsonify(
        {
            "action_revoked": result
        }
    )

@app.route('/api/role', methods=["POST"])
def api_role_post():
    input = flask.request.get_json(force=True)

    created_role = role.create_role(
        role_id=input.get('role_id'),
        display_name=input.get('display_name')
    )
    
    return flask.jsonify(
        {
            "role_created": created_role is not None,
            "role": created_role.id
        }
    )

@app.route('/api/role', methods=["DELETE"])
def api_role_delete():
    input = flask.request.get_json(force=True)

    role_id = input.get('role_id')
    result = role.delete_role(role_id)

    return flask.jsonify(
        {
            "role_deleted": result
        }
    )

@app.route('/api/role/grant_action', methods=["POST"])
def api_role_grant():
    input = flask.request.get_json(force=True)
    
    result = role.grant_action(
        action_id=input.get('action_id'),
        role_id=input.get('role_id')
    )

    return flask.jsonify(
        {
            "action_granted": result
        }
    )

@app.route('/api/role/revoke_action', methods=["POST"])
def api_role_revoke():
    input = flask.request.get_json(force=True)
    
    result = role.revoke_action(
        action_id=input.get('action_id'),
        role_id=input.get('role_id')
    )

    return flask.jsonify(
        {
            "action_revoked": result
        }
    )

@app.route('/api/action', methods=["POST"])
def api_action_post():
    input = flask.request.get_json(force=True)

    created_action = action.create_action(
        action_id=input.get('action_id'),
        display_name=input.get('display_name')
    )
    
    return flask.jsonify(
        {
            "action_created": created_action is not None,
            "action": created_action.id
        }
    )

@app.route('/api/action', methods=["DELETE"])
def api_action_delete():
    input = flask.request.get_json(force=True)

    action_id = input.get('action_id')
    result = action.delete_action(action_id)

    return flask.jsonify(
        {
            "action_deleted": result
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