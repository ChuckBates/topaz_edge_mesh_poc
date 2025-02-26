# Stand Alone OPA Service POC

This POC includes a stand alone OPA service to act as the authorization decision point. This requires no cloud connections, but also relies on the raw open source OPA service which by itself is not easy to work with or scalable. 

Directory Contents:
- `opa_windows_amd64_v1.0.0.exe` A windows executable for running a stand alone OPA service. See [OPA Docs](https://www.openpolicyagent.org/docs/latest/#running-opa) for other options.
- `poc.db` A small sqlite3 database for housing `nomination` and `ticket` data. Initialized by `server.py`.
- `poc.rego` The rego policies used to evaluate authorization decisions. Also contains sample backing data to enable the included insomnia examples.
- `requirements.txt` A set of python packages need to run the Flask API.
- `server.py` The main entry point of the Python server, responsible for handiling API requests and intializing the database.
- `opa.py` The OPA interface to communicate with the OPA service that runs alongside the Python server.
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

The server listens on `:5000` and serves API requests found in the insomnia collection.