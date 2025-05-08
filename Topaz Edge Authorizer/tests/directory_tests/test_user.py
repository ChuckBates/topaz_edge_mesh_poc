#!/usr/bin/env python

from directory.user import User

def test_create_user(mocker):
    user_id = "user_id"
    display_name = "display_name"
    email = "email@email.com"
    picture = "picture.url.com"
    pss_rights = ["pss_right_1", "pss_right_2"]
    user_type = "user"

    mock_user_return = {"id": user_id}
    mock_email_identity_return = {"id": email}
    mock_pid_identity_return = {"id": "local|pid"}

    mock_directory_connection = mocker.Mock()
    mock_directory_connection.set_object.return_value = mock_user_return
    mock_relation = mocker.Mock()
    mock_relation.set_relation.return_value = {}
    
    user = User(mock_directory_connection, mock_relation)
    
    mocker.patch.object(user, 'create_email_identity', return_value=mock_email_identity_return)
    mocker.patch.object(user, 'create_pid_identity', return_value=mock_pid_identity_return)
    
    mock_blake2b = mocker.patch('hashlib.blake2b')
    mock_blake2b.return_value.hexdigest.return_value = "pid"
    
    result = user.create_user(user_id, display_name, email, picture, pss_rights)
    
    assert result["id"] == user_id
    mock_directory_connection.set_object.assert_any_call(
        properties={
            "email": email,
            "picture": picture,
            "pss_rights": pss_rights,
            "status": "USER_STATUS_ACTIVE"
        },
        object_type=user_type,
        object_id=user_id,
        display_name=display_name
    )
    
    mock_relation.set_relation.assert_any_call("identity", email, "identifier", "user", user_id)
    mock_relation.set_relation.assert_any_call("identity", 'local|pid', "identifier", "user", user_id)

def test_delete_user_and_the_user_is_not_found(mocker):
    user_id = "user_id"
    user_type = "user"

    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.side_effect = Exception("User not found")

    mock_relation = mocker.Mock()

    user = User(mock_directory_connection, mock_relation)
    
    result = user.delete_user(user_id)

    assert result == "User not found"
    mock_directory_connection.get_object.assert_called_once_with(
        object_type=user_type,
        object_id=user_id
    )

def test_delete_user_and_the_user_is_found(mocker):
    user_id = "user_id"
    user_type = "user"

    mock_user_return = {"id": user_id}
    mock_identity_relation = {"object_id": "identity_id","object_type": "identity"}
    mock_identity_relations = [mock_identity_relation]

    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.return_value = mock_user_return
    mock_directory_connection.get_relations.return_value = mock_identity_relations
    mock_directory_connection.delete_object.return_value = {}

    mock_relation = mocker.Mock()
    mock_relation.set_relation.return_value = {}

    user = User(mock_directory_connection, mock_relation)

    result = user.delete_user(user_id)  

    assert result == "User deleted"
    mock_directory_connection.get_object.assert_called_once_with(   
        object_type=user_type,
        object_id=user_id
    )
    mock_directory_connection.get_relations.assert_called_once_with(
        object_type="identity",
        relation="identifier",
        subject_type="user",
        subject_id=user_id,
        with_objects=True
    )
    mock_directory_connection.delete_object.assert_any_call(
        object_type=user_type,
        object_id=user_id,
        with_relations=True
    )
    mock_directory_connection.delete_object.assert_any_call(
        object_type="identity",
        object_id=mock_identity_relation["object_id"],
        with_relations=False
    )
    

def test_create_email_identity(mocker):
    email_identity_id = "email@email.com"
    type = "identity"

    mock_directory_connection = mocker.Mock()
    mock_directory_connection.set_object.return_value = {
        "id": email_identity_id,
        "type": type
    }
    mock_relation = mocker.Mock()

    user = User(mock_directory_connection, mock_relation)
    result = user.create_email_identity(email_identity_id)

    assert result["id"] == email_identity_id
    mock_directory_connection.set_object.assert_called_once_with(
        properties={
            "kind": "IDENTITY_KIND_EMAIL",
            "provider": "local",
            "verified": True
        },
        object_type=type,
        object_id=email_identity_id,
        display_name=email_identity_id
    )
    
def test_create_pid_identity(mocker):
    pid_identity_id = "SGH5DSF8FG61SDF894SA6DFSJT"
    type = "identity"

    mock_directory_connection = mocker.Mock()
    mock_directory_connection.set_object.return_value = {
        "id": pid_identity_id,
        "type": type
    }
    mock_relation = mocker.Mock()

    user = User(mock_directory_connection, mock_relation)
    result = user.create_pid_identity(pid_identity_id)

    assert result["id"] == pid_identity_id
    mock_directory_connection.set_object.assert_called_once_with(
        properties={
            "kind": "IDENTITY_KIND_PID",
            "provider": "local",
            "verified": True
        },
        object_type=type,
        object_id=pid_identity_id,
        display_name=pid_identity_id
    )