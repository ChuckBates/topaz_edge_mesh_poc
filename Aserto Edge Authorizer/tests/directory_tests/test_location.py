#!/usr/bin/env python

from directory.location import Location

def test_create_location(mocker):
    location_id = "test_location"
    display_name = "Test Location"

    mock_location_return = type('', (object,), {'id': location_id})()
    mock_directory_connection = mocker.Mock()
    mock_directory_connection.set_object.return_value = mock_location_return

    location = Location(mock_directory_connection)

    result = location.create_location(location_id, display_name)

    assert result == mock_location_return
    mock_directory_connection.set_object.assert_called_once_with(
        object_type="location",
        object_id=location_id,
        display_name=display_name
    )

def test_delete_location_and_the_location_is_not_found(mocker):
    location_id = "test_location"

    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.side_effect = Exception("Location not found")

    location = Location(mock_directory_connection)

    result = location.delete_location(location_id)

    assert result == "Location " + location_id + " not found"

def test_delete_location_and_the_location_is_found(mocker):
    location_id = "test_location"

    mock_location_return = type('', (object,), {'id': location_id})()
    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.return_value = mock_location_return
    mock_directory_connection.delete_object.return_value = {}

    location = Location(mock_directory_connection)

    result = location.delete_location(location_id)

    assert result == "Location " + location_id + " deleted"