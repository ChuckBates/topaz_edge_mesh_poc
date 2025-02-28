#!/usr/bin/env python

from directory.pss_right import PssRight

def test_create_pss_right(mocker):
    pss_right_id = "test_pss_right"
    display_name = "Test Pss Right"

    mock_pss_right_return = type('', (object,), {'id': pss_right_id})()
    mock_directory_connection = mocker.Mock()
    mock_directory_connection.set_object.return_value = mock_pss_right_return

    pss_right = PssRight(mock_directory_connection)

    result = pss_right.create_pss_right(pss_right_id, display_name)

    assert result == mock_pss_right_return
    mock_directory_connection.set_object.assert_called_once_with(
        object_type="pss_right",
        object_id=pss_right_id,
        display_name=display_name
    )

def test_delete_pss_right_and_the_pss_right_is_not_found(mocker):
    pss_right_id = "test_pss_right"

    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.side_effect = Exception("PssRight not found")

    pss_right = PssRight(mock_directory_connection)

    result = pss_right.delete_pss_right(pss_right_id)

    assert result == "PssRight " + pss_right_id + " not found"

def test_delete_pss_right_and_the_pss_right_is_found(mocker):
    pss_right_id = "test_pss_right"

    mock_pss_right_return = type('', (object,), {'id': pss_right_id})()
    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.return_value = mock_pss_right_return
    mock_directory_connection.delete_object.return_value = {}

    pss_right = PssRight(mock_directory_connection)

    result = pss_right.delete_pss_right(pss_right_id)

    assert result == "PssRight " + pss_right_id + " deleted"
    