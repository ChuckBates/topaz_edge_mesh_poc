#!/usr/bin/env python

from directory.action_set import ActionSet

def test_create_action_set(mocker):
    action_set_id = "test_action_set"
    display_name = "Test Action Set"

    mock_action_set_return = {"id": action_set_id}
    mock_directory_connection = mocker.Mock()
    mock_directory_connection.set_object.return_value = mock_action_set_return
    mock_relation = mocker.Mock()

    action_set = ActionSet(mock_directory_connection, mock_relation)

    result = action_set.create_action_set(action_set_id, display_name)

    assert result == mock_action_set_return
    mock_directory_connection.set_object.assert_called_once_with(
        object_type="action_set",
        object_id=action_set_id,
        display_name=display_name
    )

def test_delete_action_set_and_the_action_set_is_not_found(mocker):
    action_set_id = "test_action_set"

    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.side_effect = Exception("Action set not found")
    mock_relation = mocker.Mock()

    action_set = ActionSet(mock_directory_connection, mock_relation)

    result = action_set.delete_action_set(action_set_id)

    assert result == "Action set " + action_set_id + " not found"

def test_delete_action_set_and_the_action_set_is_found(mocker):
    action_set_id = "test_action_set"

    mock_action_set_return = {"id": action_set_id}
    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.return_value = mock_action_set_return
    mock_directory_connection.delete_object.return_value = {}
    mock_relation = mocker.Mock()

    action_set = ActionSet(mock_directory_connection, mock_relation)

    result = action_set.delete_action_set(action_set_id)

    assert result == "Action set " + action_set_id + " deleted"

def test_grant_action_and_the_action_is_not_found(mocker):
    action_id = "action_id"
    action_set_id = "action_set_id"

    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.side_effect = Exception("Action not found")
    mock_relation = mocker.Mock()

    action_set = ActionSet(mock_directory_connection, mock_relation)

    result = action_set.grant_action(action_id, action_set_id)

    assert result == "Action " + action_id + " not found"

def test_grant_action_and_the_action_set_is_not_found(mocker):
    action_id = "action_id"
    action_set_id = "action_set_id"

    mock_action_return = {"id": action_id}
    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.return_value = mock_action_return
    mock_directory_connection.get_object.side_effect = [
        mock_action_return,
        Exception("Action Set not found")
    ]
    mock_relation = mocker.Mock()

    action_set = ActionSet(mock_directory_connection, mock_relation)

    result = action_set.grant_action(action_id, action_set_id)

    assert result == "Action Set " + action_set_id + " not found"

def test_grant_action_and_the_action_and_action_set_are_found(mocker):
    action_id = "action_id"
    action_set_id = "action_set_id"

    mock_action_return = {"id": action_id}
    mock_action_set_return = {"id": action_set_id}
    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.side_effect = [mock_action_return, mock_action_set_return]
    mock_relation = mocker.Mock()

    action_set = ActionSet(mock_directory_connection, mock_relation)

    result = action_set.grant_action(action_id, action_set_id)

    assert result == "Action " + action_id + " granted to action set " + action_set_id
    mock_directory_connection.get_object.assert_any_call(
        object_type="action",
        object_id=action_id
    )
    mock_directory_connection.get_object.assert_any_call(
        object_type="action_set",
        object_id=action_set_id
    )
    mock_relation.set_relation.assert_called_once_with("action", action_id, "member", "action_set", action_set_id)

def test_revoke_action_and_the_action_is_not_found(mocker):
    action_id = "action_id"
    action_set_id = "action_set_id"

    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.side_effect = Exception("Action not found")
    mock_relation = mocker.Mock()

    action_set = ActionSet(mock_directory_connection, mock_relation)

    result = action_set.revoke_action(action_id, action_set_id)

    assert result == "Action " + action_id + " not found"

def test_revoke_action_and_the_action_set_is_not_found(mocker):
    action_id = "action_id"
    action_set_id = "action_set_id"

    mock_action_return = {"id": action_id}
    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.return_value = mock_action_return
    mock_directory_connection.get_object.side_effect = [
        mock_action_return,
        Exception("Action Set not found")
    ]
    mock_relation = mocker.Mock()

    action_set = ActionSet(mock_directory_connection, mock_relation)

    result = action_set.revoke_action(action_id, action_set_id)

    assert result == "Action Set " + action_set_id + " not found"

def test_revoke_action_and_the_action_and_action_set_are_found(mocker):
    action_id = "action_id"
    action_set_id = "action_set_id"

    mock_action_return = {"id": action_id}
    mock_action_set_return = {"id": action_set_id}
    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.side_effect = [mock_action_return, mock_action_set_return]
    mock_relation = mocker.Mock()

    action_set = ActionSet(mock_directory_connection, mock_relation)

    result = action_set.revoke_action(action_id, action_set_id)

    assert result == "Action " + action_id + " revoked from action set " + action_set_id
    mock_directory_connection.get_object.assert_any_call(
        object_type="action",
        object_id=action_id
    )
    mock_directory_connection.get_object.assert_any_call(
        object_type="action_set",
        object_id=action_set_id
    )
    mock_relation.delete_relation.assert_called_once_with("action", action_id, "member", "action_set", action_set_id)