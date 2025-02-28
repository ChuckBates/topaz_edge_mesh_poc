#!/usr/bin/env python

from directory.action import Action

def test_create_action(mocker):
    action_id = "test_action"
    display_name = "Test Action"

    mock_action_return = type('', (object,), {'id': action_id})()
    mock_directory_connection = mocker.Mock()
    mock_directory_connection.set_object.return_value = mock_action_return

    action = Action(mock_directory_connection)

    result = action.create_action(action_id, display_name)

    assert result == mock_action_return
    mock_directory_connection.set_object.assert_called_once_with(
        object_type="action",
        object_id=action_id,
        display_name=display_name
    )

def test_delete_action_and_the_action_is_not_found(mocker):
    action_id = "test_action"

    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.side_effect = Exception("Action not found")

    action = Action(mock_directory_connection)

    result = action.delete_action(action_id)

    assert result == "Action " + action_id + " not found"

def test_delete_action_and_the_action_is_found(mocker):
    action_id = "test_action"

    mock_action_return = type('', (object,), {'id': action_id})()
    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.return_value = mock_action_return
    mock_directory_connection.delete_object.return_value = {}

    action = Action(mock_directory_connection)

    result = action.delete_action(action_id)

    assert result == "Action " + action_id + " deleted"
