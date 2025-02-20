#!/usr/bin/env python
"""
Example library for wrapping the opa.py library with a Flask API. Modified to conform to 
T4 use cases. Source: https://github.com/open-policy-agent/contrib/tree/main/data_filter_example
"""
import json
import sqlite3

import flask
from flask_bootstrap import Bootstrap

import opa

app = flask.Flask(__name__, static_url_path='/static')
Bootstrap(app)

@app.route('/api/nominations', methods=["POST"])
def api_nominations():
    input = flask.request.get_json(force=True)
    return flask.jsonify({'allowed': opa.evaluate(input=input)})

@app.route('/api/nominations/search', methods=["POST"])
def api_search_nominations():
    input = flask.request.get_json(force=True)
    opa_result = opa.compile(q='data.example.allow==true',
                                     input=input,
                                     unknowns=[input.get('unknown')])
    
    if not opa_result.defined:
        return flask.jsonify({'allowed': False})
    
    if opa_result.defined and opa_result.sql is None:
        return flask.jsonify({'allowed': True, 'sql': None})
    
    result = {
        'allowed': opa_result.defined,
        'sql': opa_result.sql.clauses[0].sql()
    }
    return flask.jsonify(result)

def get_db():
    db = getattr(flask.g, '_database', None)
    if db is None:
        db = flask.g._database = sqlite3.connect('poc.db')
    db.row_factory = make_dicts
    return db

@app.teardown_appcontext
def close_connection(e):
    db = getattr(flask.g, '_database', None)
    if db is not None:
        db.close()

def init_schema():
    db = get_db()
    c = db.cursor()
    for table in TABLES:
        c.execute('DROP TABLE IF EXISTS ' + table['name'])
        c.execute(table['schema'])
    db.commit()


def pump_db():
    db = get_db()
    c = db.cursor()
    for table in TABLES:
        for row in table['data']:
            insert_object(table['name'], c, row)
    db.commit()


def init_db():
    with app.app_context():
        init_schema()
        pump_db()

def query_db(query, args=(), one=False):
    print("Resulting query: ", query)
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def insert_object(table, cursor, obj):
    row_keys = sorted(obj.keys())
    keys = '(' + ','.join(row_keys) + ')'
    values = '(' + ','.join(['?'] * len(row_keys)) + ')'
    stmt = 'INSERT INTO {} {} VALUES {}'.format(table, keys, values)
    args = [str(obj[k]) for k in row_keys]
    print(str(stmt), args)
    cursor.execute(stmt, args)

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value) for idx, value in enumerate(row))

NOMINATIONS = [{
    'id': 'nom1',
    'subscriber': 'CPL',
    'company': 'EXN',
    'location': 'DVD',
    'productType': 'GAS'
}, {
    'id': 'nom2',
    'subscriber': 'BPL',
    'company': 'P66',
    'location': 'SAN',
    'productType': 'JET'
}]

TICKETS = [{
    'id': 'tic1',
    'subscriber': 'CPL',
    'company': 'EXN',
    'location': 'DVD',
    'productType': 'GAS'
}, {
    'id': 'tic2',
    'subscriber': 'BPL',
    'company': 'P66',
    'location': 'SAN',
    'productType': 'JET'
}]

TABLES = [
    {
        'name': 'nominations',
        'schema': """CREATE TABLE nominations (
                        id TEXT PRIMARY KEY
                        , subscriber TEXT
                        , company TEXT
                        , location TEXT
                        , productType TEXT)""",
        'data': NOMINATIONS,
    },
    {
        'name': 'tickets',
        'schema': """CREATE TABLE tickets (
                        id TEXT PRIMARY KEY
                        , subscriber TEXT
                        , company TEXT
                        , location TEXT
                        , productType TEXT)""",
        'data': TICKETS,
    }
]

if __name__ == '__main__':
    init_db()
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
