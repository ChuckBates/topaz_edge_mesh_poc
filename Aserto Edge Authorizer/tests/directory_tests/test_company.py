#!/usr/bin/env python

from directory.company import Company

def test_create_company(mocker):
    company_id = "test_company"
    display_name = "Test Company"

    mock_company_return = type('', (object,), {'id': company_id})()
    mock_directory_connection = mocker.Mock()
    mock_directory_connection.set_object.return_value = mock_company_return

    company = Company(mock_directory_connection)

    result = company.create_company(company_id, display_name)

    assert result == mock_company_return
    mock_directory_connection.set_object.assert_called_once_with(
        properties={},
        object_type="company",
        object_id=company_id,
        display_name=display_name
    )

def test_delete_company_and_the_company_is_not_found(mocker):
    company_id = "test_company"

    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.side_effect = Exception("Company not found")

    company = Company(mock_directory_connection)

    result = company.delete_company(company_id)

    assert result == "Company " + company_id + " not found"

def test_delete_company_and_the_company_is_found(mocker):
    company_id = "test_company"

    mock_company_return = type('', (object,), {'id': company_id})()
    mock_directory_connection = mocker.Mock()
    mock_directory_connection.get_object.return_value = mock_company_return
    mock_directory_connection.delete_object.return_value = {}

    company = Company(mock_directory_connection)

    result = company.delete_company(company_id)

    assert result == "company " + company_id + " deleted"