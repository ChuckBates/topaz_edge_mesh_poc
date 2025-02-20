# Aserto Edge Authorizer POC

This POC contains the files necessary to have the python server rely on a local [Aserto Edge Authorizer](https://docs.aserto.com/docs/edge-authorizers/overview) to act as the authorization decision point. 

Directory Contents:
- `policy-poc.yaml` Example aserto config for connecting to the example Aserto Cloud.
- `requirements.txt` A set of python packages need to run the Flask API.
- `server.py` The main entry point of the Python server, responsible for handiling API requests.
- `opa.py` The OPA interface that runs alongside the Python server, used for SQL generation.
- `sql.py` Helper SQL library that aids in the translation of OPA results to SQL where clauses.

## Install
For steps to setup a local Aserto Edge Authorizer, please see the Aserto [Docs](https://docs.aserto.com/docs/edge-authorizers/deployment-and-operation).

Depending on your preferred install, you might be asked to login to the Aserto CLI, which will require credentials to the Aserto Cloud. Please see @chuckbates for credentials to connect to the example Aserto Cloud. 

If you wish to use the example config rather than creating your own, place the `policy-poc.yaml` file in your `config/topaz/cfg` directory (`$HOME/.config/topaz/cfg` on Widows, likely `usr/home/config/topaz/cfg` on Mac)