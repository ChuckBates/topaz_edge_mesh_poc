#!/usr/bin/env python

class Role:
    def __init__(self, directory_connection, relation):
        self.directory_connection = directory_connection
        self.relation = relation

    def create_role(self, role_id, display_name):
        role = self.directory_connection.set_object(
            properties={},
            object_type="role",
            object_id=role_id,
            display_name=display_name
        )
        return role

    def delete_role(self, role_id):
        try:
            role = self.directory_connection.get_object(
                object_type="role",
                object_id=role_id
            )
        except Exception as e:
            return "Role " + role_id + " not found"
        
        self.directory_connection.delete_object(
            object_type="role",
            object_id=role.id,
            with_relations=True
        )
        return "Role " + role.id + " deleted"
    
    def grant_action(self, action_id, role_id):
        try:
            action = self.directory_connection.get_object(
                object_type="action",
                object_id=action_id
            )
        except Exception as e:
            return "Action " + action_id + " not found"
        
        try:
            role = self.directory_connection.get_object(
                object_type="role",
                object_id=role_id
            )
        except Exception as e:
            return "Role " + role_id + " not found"
        
        self.relation.create_relation("action", action.id, "member", "role", role.id)
        return "Action " + action.id + " granted to role " + role.id
    
    def revoke_action(self, action_id, role_id):
        try:
            action = self.directory_connection.get_object(
                object_type="action",
                object_id=action_id
            )
        except Exception as e:
            return "Action " + action_id + " not found"
        
        try:
            role = self.directory_connection.get_object(
                object_type="role",
                object_id=role_id
            )
        except Exception as e:
            return "Role " + role_id + " not found"
        
        self.relation.delete_relation("action", action.id, "member", "role", role.id)
        return "Action " + action.id + " revoked from role " + role.id