#!/usr/bin/env python

from Directory.DirectoryConnection import directory_connection
from Directory import Relation

def create_user_permission(company, subscriber, locations, product_types, role):
    user_permission = directory_connection.set_object(
        properties={},
        object_type="user_permission",
        object_id=company + "-" + subscriber + "-" + role,
        display_name=company + "-" + subscriber + "-" + role
    )
    # create user relation
    # Relation.create_relation("user_permission", user_permission.id, "member", "user", user_id)
    # create company relation
    Relation.create_relation("company", company, "member", "user_permission", user_permission.id)
    # create subscriber relation
    Relation.create_relation("subscriber", subscriber, "member", "user_permission", user_permission.id)
    # create locations relations
    for location in locations:
        Relation.create_relation("location", location, "member", "user_permission", user_permission.id)
    # create product_types relations
    for product_type in product_types:
        Relation.create_relation("product_type", product_type, "member", "user_permission", user_permission.id)
    # create role relation
    Relation.create_relation("role", role, "member", "user_permission", user_permission.id)
    return user_permission


def delete_user_permission(permission_id):
    try:
        user_permission = directory_connection.get_object(
            object_type="user_permission",
            object_id=permission_id
        )
    except Exception as e:
        return "User Permission " + permission_id + " not found"

    directory_connection.delete_object(
        object_type="user_permission",
        object_id=user_permission.id,
        with_relations=True
    )

    return "User Permission " + user_permission.id + " deleted"

def grant_user_permission(user_id, user_permission_id):
    try:
        user_permission = directory_connection.get_object(
            object_type="user_permission",
            object_id=user_permission_id
        )
    except Exception as e:
        return "User Permission " + user_permission_id + " not found"
    
    try:
        user = directory_connection.get_object(
            object_type="user",
            object_id=user_id
        )
    except Exception as e:
        return "User " + user_id + " not found"

    # create user relation
    Relation.create_relation("user_permission", user_permission.id, "member", "user", user_id)

    return "User Permission " + user_permission.id + " granted to user " + user_id

def revoke_user_permission(user_id, user_permission_id):
    try:
        user_permission = directory_connection.get_object(
            object_type="user_permission",
            object_id=user_permission_id
        )
    except Exception as e:
        return "User Permission " + user_permission_id + " not found"
    try:
        user = directory_connection.get_object(
            object_type="user",
            object_id=user_id
        )
    except Exception as e:
        return "User " + user_id + " not found"
    
    # delete user relation
    Relation.delete_relation("user_permission", user_permission.id, "member", "user", user_id)

    return "User Permission " + user_permission.id + " revoked from user " + user_id