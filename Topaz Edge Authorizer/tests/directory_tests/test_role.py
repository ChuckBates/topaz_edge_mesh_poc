#!/usr/bin/env python

from directory.role import Role

def test_create_role(mocker):
    role_id = "test_role"
    display_name = "Test Role"

    mock_role_return = {"id": role_id}
    mock_directory_connection = mocker.Mock()
    mock_directory_connection.set_object.return_value = mock_role_return
    mock_relation = mocker.Mock()

    role = Role(mock_directory_connection, mock_relation)

    result = role.create_role(role_id, display_name)

    assert result == mock_role_return
    mock_directory_connection.set_object.assert_called_once_with(
        properties={},
        object_type="role",
        object_id=role_id,
        display_name=display_name
    )

def test_delete_role_and_the_role_is_not_found(mocker):
    role_id = "test_role"

    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.side_effect = Exception("Role not found")
    mock_relation = mocker.Mock()

    role = Role(mock_directory_connection, mock_relation)

    result = role.delete_role(role_id)

    assert result == "Role " + role_id + " not found"

def test_delete_role_and_the_role_is_found(mocker):
    role_id = "test_role"

    mock_role_return = {"id": role_id}
    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.return_value = mock_role_return
    mock_directory_connection.delete_object.return_value = {}
    mock_relation = mocker.Mock()

    role = Role(mock_directory_connection, mock_relation)

    result = role.delete_role(role_id)

    assert result == "Role " + role_id + " deleted"

def test_grant_action_and_the_action_is_not_found(mocker):
    action_id = "action_id"
    role_id = "role_id"

    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.side_effect = Exception("Action not found")
    mock_relation = mocker.Mock()

    role = Role(mock_directory_connection, mock_relation)

    result = role.grant_action(action_id, role_id)

    assert result == "Action " + action_id + " not found"

def test_grant_action_and_the_role_is_not_found(mocker):
    action_id = "action_id"
    role_id = "role_id"

    mock_action_return = {"id": action_id}
    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.return_value = mock_action_return
    mock_directory_connection.get_object.side_effect = [
        mock_action_return,
        Exception("Role not found")
    ]
    mock_relation = mocker.Mock()

    role = Role(mock_directory_connection, mock_relation)

    result = role.grant_action(action_id, role_id)

    assert result == "Role " + role_id + " not found"

def test_grant_action(mocker):
    action_id = "action_id"
    role_id = "role_id"

    mock_action_return = {"id": action_id}
    mock_role_return = {"id": role_id}
    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.side_effect = [
        mock_action_return,
        mock_role_return
    ]
    mock_relation = mocker.Mock()
    mock_relation.set_relation.return_value = {}

    role = Role(mock_directory_connection, mock_relation)

    result = role.grant_action(action_id, role_id)

    assert result == "Action " + action_id + " granted to role " + role_id

def test_revoke_action_and_the_action_is_not_found(mocker):
    action_id = "action_id"
    role_id = "role_id"

    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.side_effect = Exception("Action not found")
    mock_relation = mocker.Mock()

    role = Role(mock_directory_connection, mock_relation)

    result = role.revoke_action(action_id, role_id)

    assert result == "Action " + action_id + " not found"

def test_revoke_action_and_the_role_is_not_found(mocker):
    action_id = "action_id"
    role_id = "role_id"

    mock_action_return = {"id": action_id}
    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.return_value = mock_action_return
    mock_directory_connection.get_object.side_effect = [
        mock_action_return,
        Exception("Role not found")
    ]
    mock_relation = mocker.Mock()

    role = Role(mock_directory_connection, mock_relation)

    result = role.revoke_action(action_id, role_id)

    assert result == "Role " + role_id + " not found"

def test_revoke_action(mocker):
    action_id = "action_id"
    role_id = "role_id"

    mock_action_return = {"id": action_id}
    mock_role_return = {"id": role_id}
    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.side_effect = [
        mock_action_return,
        mock_role_return
    ]
    mock_relation = mocker.Mock()
    mock_relation.delete_relation.return_value = {}

    role = Role(mock_directory_connection, mock_relation)

    result = role.revoke_action(action_id, role_id)

    assert result == "Action " + action_id + " revoked from role " + role_id