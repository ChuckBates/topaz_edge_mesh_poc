#!/usr/bin/env python

import json
import requests

class DirectoryConnection:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
    
    def _headers(self):
        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        return headers

    def set_object(self, object_type, object_id, display_name=None, properties=None):
        url = f"{self.base_url}/api/v3/directory/object"
        payload = {
            "object": {
                "type": object_type,
                "id": object_id,
                "display_name": display_name or object_id,
                "properties": properties or {}
            }
        }
        response = requests.post(url, headers=self._headers(), json=payload, verify=False)
        response.raise_for_status()

        return response.json()["result"]

    def get_object(self, object_type, object_id):
        url = f"{self.base_url}/api/v3/directory/object/{object_type}/{object_id}"
        response = requests.get(url, headers=self._headers(), verify=False)
        response.raise_for_status()
        return response.json()["result"]

    def delete_object(self, object_type, object_id, with_relations=False):
        url = f"{self.base_url}/api/v3/directory/object/{object_type}/{object_id}"
        params = {"with_relations": str(with_relations).lower()}
        response = requests.delete(url, headers=self._headers(), params=params, verify=False)
        response.raise_for_status()
        return response.json()["result"]

    def set_relation(self, object_type, object_id, relation, subject_type, subject_id):
        url = f"{self.base_url}/api/v3/directory/relation"
        payload = {
            "relation": {
                "object_id": object_id,
                "object_type": object_type,
                "relation": relation,
                "subject_id": subject_id,
                "subject_type": subject_type
            }
        }
        response = requests.post(url, headers=self._headers(), json=payload, verify=False)
        response.raise_for_status()
        return response.json()["result"]["relation"]

    def get_relation(self, object_type, object_id, relation, subject_type, subject_id):
        url = f"{self.base_url}/api/v3/directory/relation"
        params = {
            "object_type": object_type,
            "object_id": object_id,
            "relation": relation,
            "subject_type": subject_type,
            "subject_id": subject_id
        }
        response = requests.get(url, headers=self._headers(), params=params, verify=False)
        response.raise_for_status()
        return response.json()["result"]

    def get_relations(self, object_type, relation, subject_type, subject_id, with_objects=False):
        url = f"{self.base_url}/api/v3/directory/relations"
        params = {
            "object_type": object_type,
            "relation": relation,
            "subject_type": subject_type,
            "subject_id": subject_id,
            "with_objects": str(with_objects).lower()
        }
        response = requests.get(url, headers=self._headers(), params=params, verify=False)
        response.raise_for_status()
        return response.json()["results"]
    
    def delete_relation(self, object_type, object_id, relation, subject_type, subject_id):
        url = f"{self.base_url}/api/v3/directory/relation"
        params = {
            "object_type": object_type,
            "object_id": object_id,
            "relation": relation,
            "subject_type": subject_type,
            "subject_id": subject_id
        }
        response = requests.delete(url, headers=self._headers(), params=params, verify=False)
        response.raise_for_status()
        return response.json()['result']
        