#!/usr/bin/env python

class Subscriber:
    def __init__(self, directory_connection, relation):
        self.directory_connection = directory_connection
        self.relation = relation

    def create_subscriber(self, subscriber_id, display_name):
        subscriber = self.directory_connection.set_object(
            properties={},
            object_type="subscriber",
            object_id=subscriber_id,
            display_name=display_name
        )
        return subscriber

    def delete_subscriber(self, subscriber_id):
        try:
            subscriber = self.directory_connection.get_object(
                object_type="subscriber",
                object_id=subscriber_id
            )
        except Exception as e:
            return "Subscriber " + subscriber_id + " not found"
        
        self.directory_connection.delete_object(
            object_type="subscriber",
            object_id=subscriber.id,
            with_relations=True
        )
        return "subscriber " + subscriber.id + " deleted"
    
    def grant_action_set(self, action_set_id, subscriber_id):
        try:
            action_set = self.directory_connection.get_object(
                object_type="action_set",
                object_id=action_set_id
            )
        except Exception as e:
            return "Action Set " + action_set_id + " not found"
        
        try:
            subscriber = self.directory_connection.get_object(
                object_type="subscriber",
                object_id=subscriber_id
            )
        except Exception as e:
            return "Subscriber " + subscriber_id + " not found"
        
        self.relation.create_relation("action_set", action_set.id, "member", "subscriber", subscriber.id)
        return "Action Set " + action_set.id + " granted to subscriber " + subscriber.id
    
    def revoke_action_set(self, action_set_id, subscriber_id):
        try:
            action_set = self.directory_connection.get_object(
                object_type="action_set",
                object_id=action_set_id
            )
        except Exception as e:
            return "Action Set " + action_set_id + " not found"
        
        try:
            subscriber = self.directory_connection.get_object(
                object_type="subscriber",
                object_id=subscriber_id
            )
        except Exception as e:
            return "Subscriber " + subscriber_id + " not found"
        
        self.relation.delete_relation("action_set", action_set.id, "member", "subscriber", subscriber.id)
        return "Action Set " + action_set.id + " revoked from subscriber " + subscriber.id