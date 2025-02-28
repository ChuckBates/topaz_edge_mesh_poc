#!/usr/bin/env python

from directory.subscriber import Subscriber

def test_create_subscriber(mocker):
    subscriber_id = "test_subscriber"
    display_name = "Test Subscriber"

    mock_subscriber_return = type('', (object,), {'id': subscriber_id})()
    mock_directory_connection = mocker.Mock()
    mock_directory_connection.set_object.return_value = mock_subscriber_return
    mock_relation = mocker.Mock()

    subscriber = Subscriber(mock_directory_connection, mock_relation)

    result = subscriber.create_subscriber(subscriber_id, display_name)

    assert result == mock_subscriber_return
    mock_directory_connection.set_object.assert_called_once_with(
        properties={},
        object_type="subscriber",
        object_id=subscriber_id,
        display_name=display_name
    )

def test_delete_subscriber_and_the_subscriber_is_not_found(mocker):
    subscriber_id = "test_subscriber"

    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.side_effect = Exception("Subscriber not found")
    mock_relation = mocker.Mock()

    subscriber = Subscriber(mock_directory_connection, mock_relation)

    result = subscriber.delete_subscriber(subscriber_id)

    assert result == "Subscriber " + subscriber_id + " not found"

def test_delete_subscriber_and_the_subscriber_is_found(mocker):
    subscriber_id = "test_subscriber"

    mock_subscriber_return = type('', (object,), {'id': subscriber_id})()
    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.return_value = mock_subscriber_return
    mock_directory_connection.delete_object.return_value = {}
    mock_relation = mocker.Mock()

    subscriber = Subscriber(mock_directory_connection, mock_relation)

    result = subscriber.delete_subscriber(subscriber_id)

    assert result == "subscriber " + subscriber_id + " deleted"

def test_grant_action_set(mocker):
    action_set_id = "action_set_id"
    subscriber_id = "subscriber_id"

    mock_action_set_return = type('', (object,), {'id': action_set_id})()
    mock_subscriber_return = type('', (object,), {'id': subscriber_id})()
    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.side_effect = [mock_action_set_return, mock_subscriber_return]
    mock_relation = mocker.Mock()

    subscriber = Subscriber(mock_directory_connection, mock_relation)

    result = subscriber.grant_action_set(action_set_id, subscriber_id)

    assert result == "Action Set " + action_set_id + " granted to subscriber " + subscriber_id
    mock_directory_connection.get_object.assert_any_call(
        object_type="action_set",
        object_id=action_set_id
    )
    mock_directory_connection.get_object.assert_any_call(
        object_type="subscriber",
        object_id=subscriber_id
    )
    mock_relation.create_relation.assert_called_once_with("action_set", action_set_id, "member", "subscriber", subscriber_id)

def test_grant_action_set_and_the_action_set_is_not_found(mocker):
    action_set_id = "action_set_id"
    subscriber_id = "subscriber_id"

    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.side_effect = Exception("Action Set not found")
    mock_relation = mocker.Mock()

    subscriber = Subscriber(mock_directory_connection, mock_relation)

    result = subscriber.grant_action_set(action_set_id, subscriber_id)

    assert result == "Action Set " + action_set_id + " not found"

def test_grant_action_set_and_the_subscriber_is_not_found(mocker):
    action_set_id = "action_set_id"
    subscriber_id = "subscriber_id"

    mock_action_set_return = type('', (object,), {'id': action_set_id})()
    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.return_value = mock_action_set_return
    mock_directory_connection.get_object.side_effect = [
        mock_action_set_return,
        Exception("Subscriber not found")
    ]
    mock_relation = mocker.Mock()

    subscriber = Subscriber(mock_directory_connection, mock_relation)

    result = subscriber.grant_action_set(action_set_id, subscriber_id)

    assert result == "Subscriber " + subscriber_id + " not found"
    assert mock_directory_connection.get_object.call_count == 2
    mock_directory_connection.get_object.assert_any_call(
        object_type="action_set",
        object_id=action_set_id
    )
    
def test_revoke_action_set(mocker):
    action_set_id = "action_set_id"
    subscriber_id = "subscriber_id"

    mock_action_set_return = type('', (object,), {'id': action_set_id})()
    mock_subscriber_return = type('', (object,), {'id': subscriber_id})()
    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.side_effect = [mock_action_set_return, mock_subscriber_return]
    mock_relation = mocker.Mock()

    subscriber = Subscriber(mock_directory_connection, mock_relation)

    result = subscriber.revoke_action_set(action_set_id, subscriber_id)

    assert result == "Action Set " + action_set_id + " revoked from subscriber " + subscriber_id
    mock_directory_connection.get_object.assert_any_call(
        object_type="action_set",
        object_id=action_set_id
    )
    mock_directory_connection.get_object.assert_any_call(
        object_type="subscriber",
        object_id=subscriber_id
    )
    mock_relation.delete_relation.assert_called_once_with("action_set", action_set_id, "member", "subscriber", subscriber_id)

def test_revoke_action_set_and_the_action_set_is_not_found(mocker):
    action_set_id = "action_set_id"
    subscriber_id = "subscriber_id"

    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.side_effect = Exception("Action Set not found")
    mock_relation = mocker.Mock()

    subscriber = Subscriber(mock_directory_connection, mock_relation)

    result = subscriber.revoke_action_set(action_set_id, subscriber_id)

    assert result == "Action Set " + action_set_id + " not found"

def test_revoke_action_set_and_the_subscriber_is_not_found(mocker):
    action_set_id = "action_set_id"
    subscriber_id = "subscriber_id"

    mock_action_set_return = type('', (object,), {'id': action_set_id})()
    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.return_value = mock_action_set_return
    mock_directory_connection.get_object.side_effect = [
        mock_action_set_return,
        Exception("Subscriber not found")
    ]
    mock_relation = mocker.Mock()

    subscriber = Subscriber(mock_directory_connection, mock_relation)

    result = subscriber.revoke_action_set(action_set_id, subscriber_id)

    assert result == "Subscriber " + subscriber_id + " not found"
    assert mock_directory_connection.get_object.call_count == 2
    mock_directory_connection.get_object.assert_any_call(
        object_type="action_set",
        object_id=action_set_id
    )
    mock_directory_connection.get_object.assert_any_call(
        object_type="subscriber",
        object_id=subscriber_id
    )