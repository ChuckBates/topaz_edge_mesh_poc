#!/usr/bin/env python

from directory.relation import Relation

def test_set_relation(mocker):
    object_type = "object_type"
    object_id = "object_id"
    relation = "relation"
    subject_type = "subject_type"
    subject_id = "subject_id"

    mock_directory_connection = mocker.Mock()
    mock_directory_connection.set_relation.return_value = {}
    relation = Relation(mock_directory_connection)

    result = relation.set_relation(object_type, object_id, relation, subject_type, subject_id)

    assert result == {}
    mock_directory_connection.set_relation.assert_called_once_with(
        object_type=object_type,
        object_id=object_id,
        relation=relation,
        subject_type=subject_type,
        subject_id=subject_id
    )

def test_delete_relation_and_the_relation_is_not_found(mocker):
    object_type = "object_type"
    object_id = "object_id"
    relation = "relation"
    subject_type = "subject_type"
    subject_id = "subject_id"

    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_relation.side_effect = Exception("Relation not found")
    relation = Relation(mock_directory_connection)

    result = relation.delete_relation(object_type, object_id, relation, subject_type, subject_id)

    assert result == "Relation " + object_id + " - " + subject_id + " not found"
    mock_directory_connection.get_relation.assert_called_once_with(
        object_type=object_type,
        object_id=object_id,
        relation=relation,
        subject_type=subject_type,
        subject_id=subject_id
    )

def test_delete_relation_and_the_relation_is_found(mocker):
    object_type = "object_type"
    object_id = "object_id"
    relation_type = "relation"
    subject_type = "subject_type"
    subject_id = "subject_id"

    mock_relation_return = {"id": object_id}
    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_relation.return_value = mock_relation_return
    mock_directory_connection.delete_relation.return_value = {}
    relation = Relation(mock_directory_connection)

    result = relation.delete_relation(object_type, object_id, relation_type, subject_type, subject_id)

    assert result == "Relation " + object_id + " - " + subject_id + " deleted"
    mock_directory_connection.get_relation.assert_called_once_with(
        object_type=object_type,
        object_id=object_id,
        relation=relation_type,
        subject_type=subject_type,
        subject_id=subject_id
    )
    mock_directory_connection.delete_relation.assert_any_call(
        object_type=object_type,
        object_id=object_id,
        relation=relation_type,
        subject_type=subject_type,
        subject_id=subject_id
    )
    