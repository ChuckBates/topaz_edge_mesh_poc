#!/usr/bin/env python

class Location:
    def __init__(self, directory_connection):
        self.directory_connection = directory_connection

    def create_location(self, location_id, display_name):
        location = self.directory_connection.set_object(
            object_type="location",
            object_id=location_id,
            display_name=display_name
        )
        return location

    def delete_location(self, location_id):
        try:
            location = self.directory_connection.get_object(
                object_type="location",
                object_id=location_id
            )
        except Exception as e:
            return "Location " + location_id + " not found"
        
        self.directory_connection.delete_object(
            object_type="location",
            object_id=location.id,
            with_relations=True
        )
        return "Location " + location.id + " deleted"