#!/usr/bin/env python

class ProductType:
    def __init__(self, directory_connection):
        self.directory_connection = directory_connection

    def create_product_type(self, product_type_id, display_name):
        product_type = self.directory_connection.set_object(
            object_type="product_type",
            object_id=product_type_id,
            display_name=display_name
        )
        return product_type

    def delete_product_type(self, product_type_id):
        try:
            product_type = self.directory_connection.get_object(
                object_type="product_type",
                object_id=product_type_id
            )
        except Exception as e:
            return "Product Type " + product_type_id + " not found"
        
        self.directory_connection.delete_object(
            object_type="product_type",
            object_id=product_type.id,
            with_relations=True
        )
        return "Product Type " + product_type.id + " deleted"