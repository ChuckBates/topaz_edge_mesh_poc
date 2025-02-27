#!/usr/bin/env python

from hashlib import blake2b
from Directory import Relation
from Directory.DirectoryConnection import directory_connection

def create_user(user_id, display_name, email, picture, pss_rights, status):
    user = directory_connection.set_object(
        properties={
            "email": email,
            "picture": picture,
            "pss_rights": pss_rights,
            "status": status
        },
        object_type="user",
        object_id=user_id,
        display_name=display_name
    )
    # create email identity
    email_identity = create_email_identity(email)
    # create pid identity
    pid = blake2b((user_id + email).encode('utf-8'), digest_size=16).hexdigest()
    pid_identity = create_pid_identity("local|" + pid)
    # create relations
    Relation.create_relation("identity", email_identity.id, "identifier", "user", user.id)
    Relation.create_relation("identity", pid_identity.id, "identifier", "user", user.id)
    for pss_right in pss_rights:
        Relation.create_relation("pss_right", pss_right, "member", "user", user.id)    

    return user

def delete_user(user_id):
    try:
        user = directory_connection.get_object(
            object_type="user",
            object_id=user_id
        )
    except Exception as e:
        return "User not found"
    
    identity_relations = directory_connection.get_relations(
        object_type="identity",
        relation="identifier",
        subject_type="user",
        subject_id=user.id,
        with_objects=True
    )

    directory_connection.delete_object(
        object_type="user",
        object_id=user_id,
        with_relations=True
    )

    for identity_relation in identity_relations.objects:
        if identity_relation.type == "identity":
            directory_connection.delete_object(
                object_type="identity",
                object_id=identity_relation.id,
                with_relations=False
            )

    return "User deleted"


def create_email_identity(identity_id):
    identity = directory_connection.set_object(
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

def create_pid_identity(identity_id):
    identity = directory_connection.set_object(
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
