#!/usr/bin/env python

from directory.user_permission import UserPermission

def test_create_user_permission(mocker):
    company = "company"
    subscriber = "subscriber"
    locations = ["location1", "location2"]
    product_types = ["product_type1", "product_type2"]
    role = "role"
    user_permission_id = company + "-" + subscriber + "-" + role
    
    mock_user_permission_return = {"id": user_permission_id}
    mock_directory_connection = mocker.Mock()
    mock_directory_connection.set_object.return_value = mock_user_permission_return
    mock_relation = mocker.Mock()

    user_permission = UserPermission(mock_directory_connection, mock_relation)
    result = user_permission.create_user_permission(company, subscriber, locations, product_types, role)

    assert result == mock_user_permission_return
    mock_directory_connection.set_object.assert_called_once_with(
        properties={},
        object_type="user_permission",
        object_id=user_permission_id,
        display_name=user_permission_id
    )
    mock_relation.set_relation.assert_any_call("company", company, "member", "user_permission", mock_user_permission_return["id"])
    mock_relation.set_relation.assert_any_call("subscriber", subscriber, "member", "user_permission", mock_user_permission_return["id"])
    mock_relation.set_relation.assert_any_call("location", "location1", "member", "user_permission", mock_user_permission_return["id"])
    mock_relation.set_relation.assert_any_call("location", "location2", "member", "user_permission", mock_user_permission_return["id"])
    mock_relation.set_relation.assert_any_call("product_type", "product_type1", "member", "user_permission", mock_user_permission_return["id"])
    mock_relation.set_relation.assert_any_call("product_type", "product_type2", "member", "user_permission", mock_user_permission_return["id"])
    mock_relation.set_relation.assert_any_call("role", role, "member", "user_permission", mock_user_permission_return["id"])

def test_delete_user_permission_and_the_permission_is_not_found(mocker):
    permission_id = "permission_id"
    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.side_effect = Exception("User Permission not found")
    mock_relation = mocker.Mock()

    user_permission = UserPermission(mock_directory_connection, mock_relation)

    result = user_permission.delete_user_permission(permission_id)

    assert result == "User Permission " + permission_id + " not found"

def test_delete_user_permission_and_the_permission_is_found(mocker):
    user_permission_id = "user_permission_id"

    mock_user_permission_return = {"id": user_permission_id}
    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.return_value = mock_user_permission_return
    mock_relation = mocker.Mock()

    user_permission = UserPermission(mock_directory_connection, mock_relation)

    result = user_permission.delete_user_permission(user_permission_id)

    assert result == "User Permission " + user_permission_id + " deleted"
    mock_directory_connection.get_object.assert_called_once_with(
        object_type="user_permission",
        object_id=user_permission_id
    )
    mock_directory_connection.delete_object.assert_called_once_with(
        object_type="user_permission",
        object_id=user_permission_id,
        with_relations=True
    )

def test_grant_user_permission_and_the_permission_is_not_found(mocker):
    user_id = "user_id"
    user_permission_id = "user_permission_id"

    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.side_effect = Exception("User Permission not found")
    mock_relation = mocker.Mock()

    user_permission = UserPermission(mock_directory_connection, mock_relation)

    result = user_permission.grant_user_permission(user_id, user_permission_id)

    assert result == "User Permission " + user_permission_id + " not found"
    mock_directory_connection.get_object.assert_called_once_with(
        object_type="user_permission",
        object_id=user_permission_id
    )

def test_grant_user_permission_and_the_user_is_not_found(mocker):
    user_id = "user_id"
    user_permission_id = "user_permission_id"

    mock_user_permission_return = {"id": user_permission_id}
    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.side_effect = [
        mock_user_permission_return,
        Exception("User not found")
    ]
    mock_relation = mocker.Mock()

    user_permission = UserPermission(mock_directory_connection, mock_relation)

    result = user_permission.grant_user_permission(user_id, user_permission_id)

    assert result == "User " + user_id + " not found"
    assert mock_directory_connection.get_object.call_count == 2
    mock_directory_connection.get_object.assert_any_call(
        object_type="user_permission",
        object_id=user_permission_id
    )
    mock_directory_connection.get_object.assert_any_call(
        object_type="user",
        object_id=user_id
    )

def test_grant_user_permission(mocker):
    user_id = "user_id"
    user_permission_id = "user_permission_id"

    mock_user_permission_return = {"id": user_permission_id}
    mock_user_return = {"id": user_id}
    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.side_effect = [
        mock_user_permission_return,
        mock_user_return
    ]
    mock_relation = mocker.Mock()

    user_permission = UserPermission(mock_directory_connection, mock_relation)

    result = user_permission.grant_user_permission(user_id, user_permission_id)

    assert result == "User Permission " + user_permission_id + " granted to user " + user_id
    assert mock_directory_connection.get_object.call_count == 2
    mock_directory_connection.get_object.assert_any_call(
        object_type="user_permission",
        object_id=user_permission_id
    )
    mock_directory_connection.get_object.assert_any_call(
        object_type="user",
        object_id=user_id
    )
    mock_relation.set_relation.assert_called_once_with("user_permission", user_permission_id, "member", "user", user_id)

def test_revoke_user_permission_and_the_permission_is_not_found(mocker):
    user_id = "user_id"
    user_permission_id = "user_permission_id"

    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.side_effect = Exception("User Permission not found")
    mock_relation = mocker.Mock()

    user_permission = UserPermission(mock_directory_connection, mock_relation)

    result = user_permission.revoke_user_permission(user_id, user_permission_id)

    assert result == "User Permission " + user_permission_id + " not found"
    mock_directory_connection.get_object.assert_called_once_with(
        object_type="user_permission",
        object_id=user_permission_id
    )

def test_revoke_user_permission_and_the_user_is_not_found(mocker):
    user_id = "user_id"
    user_permission_id = "user_permission_id"

    mock_user_permission_return = {"id": user_permission_id}
    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.side_effect = [
        mock_user_permission_return,
        Exception("User not found")
    ]
    mock_relation = mocker.Mock()

    user_permission = UserPermission(mock_directory_connection, mock_relation)

    result = user_permission.revoke_user_permission(user_id, user_permission_id)

    assert result == "User " + user_id + " not found"
    assert mock_directory_connection.get_object.call_count == 2
    mock_directory_connection.get_object.assert_any_call(
        object_type="user_permission",
        object_id=user_permission_id
    )
    mock_directory_connection.get_object.assert_any_call(
        object_type="user",
        object_id=user_id
    )

def test_revoke_user_permission(mocker):
    user_id = "user_id"
    user_permission_id = "user_permission_id"

    mock_user_permission_return = {"id": user_permission_id}
    mock_user_return = {"id": user_id}
    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.side_effect = [
        mock_user_permission_return,
        mock_user_return
    ]
    mock_relation = mocker.Mock()

    user_permission = UserPermission(mock_directory_connection, mock_relation)

    result = user_permission.revoke_user_permission(user_id, user_permission_id)

    assert result == "User Permission " + user_permission_id + " revoked from user " + user_id
    assert mock_directory_connection.get_object.call_count == 2
    mock_directory_connection.get_object.assert_any_call(
        object_type="user_permission",
        object_id=user_permission_id
    )
    mock_directory_connection.get_object.assert_any_call(
        object_type="user",
        object_id=user_id
    )
    mock_relation.delete_relation.assert_called_once_with("user_permission", user_permission_id, "member", "user", user_id)
    