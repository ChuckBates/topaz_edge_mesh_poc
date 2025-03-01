#!/usr/bin/env python

class Relation:
    def __init__(self, directory_connection):
        self.directory_connection = directory_connection

    def create_relation(self, object_type, object_id, relation, subject_type, subject_id):
        relation = self.directory_connection.set_relation(
            object_type=object_type,
            object_id=object_id,
            relation=relation,
            subject_type=subject_type,
            subject_id=subject_id
        )
        return relation

    def delete_relation(self, object_type, object_id, relation, subject_type, subject_id):
        try:
            self.directory_connection.get_relation(
                object_type=object_type,
                object_id=object_id,
                relation=relation,
                subject_type=subject_type,
                subject_id=subject_id
            )
        except Exception as e:
            return "Relation " + object_id + " - " + subject_id + " not found"
        
        self.directory_connection.delete_relation(
            object_type=object_type,
            object_id=object_id,
            relation=relation,
            subject_type=subject_type,
            subject_id=subject_id
        )
        return "Relation " + object_id + " - " + subject_id + " deleted"