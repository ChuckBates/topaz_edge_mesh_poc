# OPA Proof Of Concept

This is intended as a proof of concept only! This is *NOT* a finished product nor anything more than an example on how OPA *might* handle T4 authorization requests.

This directory contains a sample server that uses OPA's Compile API to perform
data filtering and authorization:
- When the server receives a data filter API request it asks OPA for a set of conditions to apply to the SQL query that serves the request. 
- When the server recieves an authorization request it asks OPA to make an authorization decision based on the rego policies.

The server itself is implemented in Python using Flask and sqlite3.

Contents:
- `OPA POC.postman_collection.json` A collect of preconfigured postman requests to test the expected behaviors.
- `opa_windows_amd64_v1.0.0.exe` A windows executable for running a stand alone OPA service. See [OPA Docs](https://www.openpolicyagent.org/docs/latest/#running-opa) for other options.
- `poc.db` A small sqlite3 database for housing `nomination` and `ticket` data. Initialized by `server.py`.
- `poc.rego` The rego policies used to evaluate authorization decisions. Also contains sample backing data to enable the included postman examples.
- `requirements.txt` A set of python packages need to run the Flask API.
- `server.py` The main entry point of the Python server, responsible for handiling API requests and intializing the database.
- `opa.py` The OPA interface to communicate with the OPA service that runs alongside the Python service.
- `sql.py` Helper SQL library that aids in the translation of OPA results to SQL where clauses.

## Install

Install the dependencies into a virtualenv:

```bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Running
### Start the OPA Service:
Open a new terminal in the repo directory and run OPA:

```bash
.\opa_windows_amd64_v1.0.0.exe run -s .\poc.rego
```

### Start the Python Service:
Open another terminal in the repo directory and start the server:
```
source env/bin/activate
python server.py
```

The server listens on `:5000` and serves API requests found in the postman collection.

