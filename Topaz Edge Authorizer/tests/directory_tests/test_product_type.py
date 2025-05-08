#!/usr/bin/env python

from directory.product_type import ProductType

def test_create_product_type(mocker):
    product_type_id = "test_product_type"
    display_name = "Test Product Type"

    mock_product_type_return = {"id": product_type_id}
    mock_directory_connection = mocker.Mock()
    mock_directory_connection.set_object.return_value = mock_product_type_return

    product_type = ProductType(mock_directory_connection)

    result = product_type.create_product_type(product_type_id, display_name)

    assert result == mock_product_type_return
    mock_directory_connection.set_object.assert_called_once_with(
        object_type="product_type",
        object_id=product_type_id,
        display_name=display_name
    )

def test_delete_product_type_and_the_product_type_is_not_found(mocker):
    product_type_id = "test_product_type"

    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.side_effect = Exception("Product type not found")

    product_type = ProductType(mock_directory_connection)

    result = product_type.delete_product_type(product_type_id)

    assert result == "Product Type " + product_type_id + " not found"

def test_delete_product_type_and_the_product_type_is_found(mocker):
    product_type_id = "test_product_type"

    mock_product_type_return = {"id": product_type_id}
    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.return_value = mock_product_type_return
    mock_directory_connection.delete_object.return_value = {}

    product_type = ProductType(mock_directory_connection)

    result = product_type.delete_product_type(product_type_id)

    assert result == "Product Type " + product_type_id + " deleted"