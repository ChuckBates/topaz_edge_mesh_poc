#!/usr/bin/env python

class Company:
    def __init__(self, directory_connection):
        self.directory_connection = directory_connection

    def create_company(self, company_id, display_name):
        company = self.directory_connection.set_object(
            properties={},
            object_type="company",
            object_id=company_id,
            display_name=display_name
        )
        return company

    def delete_company(self, company_id):
        try:
            company = self.directory_connection.get_object(
                object_type="company",
                object_id=company_id
            )
        except Exception as e:
            return "Company " + company_id + " not found"
        
        self.directory_connection.delete_object(
            object_type="company",
            object_id=company.id,
            with_relations=True
        )
        return "company " + company.id + " deleted"