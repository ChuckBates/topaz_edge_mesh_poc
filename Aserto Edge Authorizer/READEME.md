# Aserto Edge Authorizer POC

This POC contains the files necessary to have the python server rely on a local [Aserto Edge Authorizer](https://docs.aserto.com/docs/edge-authorizers/overview) to act as the authorization decision point. 

Directory Contents:
- `requirements.txt` A set of python packages need to run the Flask API.
- `server.py` The main entry point of the Python server, responsible for handiling API requests.
- `opa.py` The OPA interface that runs alongside the Python server, used for SQL generation.
- `sql.py` Helper SQL library that aids in the translation of OPA results to SQL where clauses.
- `aserto_edge_authorizer_poc.insomnia.json` Example API requests to interact directly with the edge authorizer

## Install
### Aserto Edge Authorizer
To setup an Aserto Edge Authorizer to connect to the example Aserto Cloud configured with the example T4 data please follow the steps below:
- [Install the Aserto CLI](https://docs.aserto.com/docs/command-line-interface/aserto-cli/installation)
- `aserto login` to connect the CLI to the Aserto Cloud (see @chuckbates for credentials).
- `aserto install` will fetch the edge authorizer (topaz) docker image.
- `aserto config new -n policy-poc --edge-authorizer=82532907-eedc-11ef-a22c-031f1f3ef1c7 --decision-logging` this will create a new aserto config with the connection to the Aserto Cloud that has already been setup.
- The created config (`$HOME/.config/topaz/cfg/policy-poc.yaml` on Widows, likely `usr/home/config/topaz/cfg/policy-poc.yaml` on Mac) has a bug in it. Edit this file and replace `\` with `/` in both the `controller` and `decision_logger` sections
- `aserto config use policy-poc` select the config just created.
- `aserto start`

An edge authorizer (topaz) docker container should now be running and accepting requests. 

### Python Server
Install the dependencies into a virtualenv and start the python server:

```bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt
pip install -e .
source env/bin/activate
python server.py
```

## Use

With the edge authorizer and the python server running, you can interact with the example API requests in the included `opa_poc.insomnia.json` example requests. Additionally if you would like to interact with the edge authorizer directly the included `aserto_edge_authorizer_poc.insomnia.json` example requests can be used. 
