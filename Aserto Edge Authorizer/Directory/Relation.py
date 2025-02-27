#!/usr/bin/env python

from Directory.DirectoryConnection import directory_connection

def create_relation(object_type, object_id, relation, subject_type, subject_id):
    relation = directory_connection.set_relation(
        object_type=object_type,
        object_id=object_id,
        relation=relation,
        subject_type=subject_type,
        subject_id=subject_id
    )
    return relation

def delete_relation(object_type, object_id, relation, subject_type, subject_id):
    relation = directory_connection.delete_relation(
        object_type=object_type,
        object_id=object_id,
        relation=relation,
        subject_type=subject_type,
        subject_id=subject_id
    )
    return relation