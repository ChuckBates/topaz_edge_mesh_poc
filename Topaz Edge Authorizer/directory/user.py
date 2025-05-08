#!/usr/bin/env python

from hashlib import blake2b

class User:    
    def __init__(self, directory_connection, relation):
        self.directory_connection = directory_connection
        self.relation = relation

    def create_user(self, user_id, display_name, email, picture, pss_rights):
        user = self.directory_connection.set_object(
            properties={
                "email": email,
                "picture": picture,
                "pss_rights": pss_rights,
                "status": "USER_STATUS_ACTIVE"
            },
            object_type="user",
            object_id=user_id,
            display_name=display_name
        )
        # create email identity
        email_identity = self.create_email_identity(email)
        # create pid identity
        pid = blake2b((user_id + email).encode('utf-8'), digest_size=16).hexdigest()
        pid_identity = self.create_pid_identity("local|" + pid)
        # create relations
        self.relation.set_relation("identity", email_identity["id"], "identifier", "user", user["id"])
        self.relation.set_relation("identity", pid_identity["id"], "identifier", "user", user["id"])
        for pss_right in pss_rights:
            self.relation.set_relation("pss_right", pss_right, "member", "user", user["id"])    

        return user

    def delete_user(self, user_id):
        try:
            user = self.directory_connection.get_object(
                object_type="user",
                object_id=user_id
            )
        except Exception as e:
            return "User not found"
        
        identity_relations = self.directory_connection.get_relations(
            object_type="identity",
            relation="identifier",
            subject_type="user",
            subject_id=user["id"],
            with_objects=True
        )

        self.directory_connection.delete_object(
            object_type="user",
            object_id=user_id,
            with_relations=True
        )

        for identity_relation in identity_relations:
            print(identity_relation)
            if identity_relation["object_type"] == "identity":
                self.directory_connection.delete_object(
                    object_type="identity",
                    object_id=identity_relation["object_id"],
                    with_relations=False
                )

        return "User deleted"


    def create_email_identity(self, identity_id):
        identity = self.directory_connection.set_object(
            properties={
                "kind": "IDENTITY_KIND_EMAIL",
                "provider": "local",
                "verified": True
            },
            object_type="identity",
            object_id=identity_id,
            display_name=identity_id
        )
        return identity

    def create_pid_identity(self, identity_id):
        identity = self.directory_connection.set_object(
            properties={
                "kind": "IDENTITY_KIND_PID",
                "provider": "local",
                "verified": True
            },
            object_type="identity",
            object_id=identity_id,
            display_name=identity_id
        )
        return identity
