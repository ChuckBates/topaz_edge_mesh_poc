#!/usr/bin/env python

class Action:
    def __init__(self, directory_connection):
        self.directory_connection = directory_connection

    def create_action(self, action_id, display_name):
        action = self.directory_connection.set_object(
            object_type="action",
            object_id=action_id,
            display_name=display_name
        )
        return action

    def delete_action(self, action_id):
        try:
            action = self.directory_connection.get_object(
                object_type="action",
                object_id=action_id
            )
        except Exception as e:
            return "Action " + action_id + " not found"
        
        self.directory_connection.delete_object(
            object_type="action",
            object_id=action["id"],
            with_relations=True
        )
        return "Action " + action["id"] + " deleted"
        