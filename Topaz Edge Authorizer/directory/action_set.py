#!/usr/bin/env python

class ActionSet:
    def __init__(self, directory_connection, relation):
        self.directory_connection = directory_connection
        self.relation = relation

    def create_action_set(self, action_set_id, display_name):
        action_set = self.directory_connection.set_object(
            object_type="action_set",
            object_id=action_set_id,
            display_name=display_name
        )
        return action_set

    def delete_action_set(self, action_set_id):
        try:
            action_set = self.directory_connection.get_object(
                object_type="action_set",
                object_id=action_set_id
            )
        except Exception as e:
            return "Action set " + action_set_id + " not found"
        
        self.directory_connection.delete_object(
            object_type="action_set",
            object_id=action_set["id"],
            with_relations=True
        )
        return "Action set " + action_set_id + " deleted"
    
    def grant_action(self, action_id, action_set_id):
        try:
            action = self.directory_connection.get_object(
                object_type="action",
                object_id=action_id
            )
        except Exception as e:
            return "Action " + action_id + " not found"
        
        try:
            action_set = self.directory_connection.get_object(
                object_type="action_set",
                object_id=action_set_id
            )
        except Exception as e:
            return "Action Set " + action_set_id + " not found"
        
        self.relation.set_relation("action", action["id"], "member", "action_set", action_set["id"])
        return "Action " + action["id"] + " granted to action set " + action_set["id"]
    
    def revoke_action(self, action_id, action_set_id):
        try:
            action = self.directory_connection.get_object(
                object_type="action",
                object_id=action_id
            )
        except Exception as e:
            return "Action " + action_id + " not found"
        
        try:
            action_set = self.directory_connection.get_object(
                object_type="action_set",
                object_id=action_set_id
            )
        except Exception as e:
            return "Action Set " + action_set_id + " not found"
        
        self.relation.delete_relation("action", action["id"], "member", "action_set", action_set["id"])
        return "Action " + action["id"] + " revoked from action set " + action_set["id"]