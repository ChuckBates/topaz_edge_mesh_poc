#!/usr/bin/env python

import json
from aserto.client.directory.v3 import Directory
from pathlib import Path

current_dir = Path(__file__).parent.resolve()
with open(str(current_dir) + '/config.json') as file:
    config = json.load(file)

directory_connection = Directory(
    api_key=config["api_key"],
    tenant_id=config["tenant_id"],
    address=config["address"]
)