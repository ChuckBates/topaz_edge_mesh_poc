#!/usr/bin/env python

class PssRight:
    def __init__(self, directory_connection):
        self.directory_connection = directory_connection

    def create_pss_right(self, pss_right_id, display_name):
        pss_right = self.directory_connection.set_object(
            object_type="pss_right",
            object_id=pss_right_id,
            display_name=display_name
        )
        return pss_right

    def delete_pss_right(self, pss_right_id):
        try:
            pss_right = self.directory_connection.get_object(
                object_type="pss_right",
                object_id=pss_right_id
            )
        except Exception as e:
            return "PssRight " + pss_right_id + " not found"
        
        self.directory_connection.delete_object(
            object_type="pss_right",
            object_id=pss_right.id,
            with_relations=True
        )
        return "PssRight " + pss_right.id + " deleted"