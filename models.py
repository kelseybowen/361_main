from db_connector import connectToMySQL


class User:
    db = "361_main"
    def __init__(self, user_data):
        self.id = user_data['id']
        self.name = user_data['name']
    
    @classmethod
    def create_user(cls, user_data):
        query = "INSERT INTO Users (name) VALUES ( %(name)s );"
        return connectToMySQL(cls.db).query_db(query, user_data)
    
    @classmethod
    def get_user_by_name(cls, user_data):
        query = "SELECT * FROM Users WHERE name = %(name)s;"
        return connectToMySQL(cls.db).query_db(query, user_data)

    @classmethod
    def get_user_id_by_name(cls, user_data):
        query = "SELECT id FROM Users WHERE name = %(name)s;"
        return connectToMySQL(cls.db).query_db(query, user_data)


class Destination:
    db = "361_main"
    def __init__(self, dest_data):
        self.id = dest_data['id']
        self.zip = dest_data['zip']
        self.name = dest_data['name']
        self.lat = dest_data['lat']
        self.lon = dest_data['lon']

    @classmethod
    def save_destination_with_zip(cls, dest_data):
        query = "INSERT INTO Destinations (zip, name, lat, lon) VALUES (%(zip)s, %(name)s, %(lat)s, %(lon)s);"
        return connectToMySQL(cls.db).query_db(query, dest_data)

    @classmethod
    def save_destination_without_zip(cls, dest_data):
        query = "INSERT INTO Destinations (name, lat, lon) VALUES (%(name)s, %(lat)s, %(lon)s);"
        return connectToMySQL(cls.db).query_db(query, dest_data)
    
    @classmethod
    def get_destination_by_id(cls, dest_data):
        query = "SELECT * FROM Destinations WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, dest_data)
    
    @classmethod
    def get_destination_by_zip(cls, dest_data):
        query = "SELECT * FROM Destinations WHERE zip = %(zip)s;"
        return connectToMySQL(cls.db).query_db(query, dest_data)

    @classmethod
    def delete_destination(cls, dest_data):
        query = "DELETE FROM Destinations WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, dest_data)


class Search:
    db = "361_main"
    def __init__(self, search_data):
        self.user_id = search_data['user_id']
        self.destination_id = search_data['destination_id']

    @classmethod
    def save_search(cls, search_data):
        query = "INSERT INTO Searches (user_id, destination_id) VALUES (%(user_id)s, %(destination_id)s);"
        return connectToMySQL(cls.db).query_db(query, search_data)

    @classmethod
    def get_user_saved_searches(cls, data):
        query = "SELECT zip, name, lat, lon, id FROM Destinations JOIN Searches ON destination_id = Destinations.id WHERE user_id = %(user_id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete_search(cls, search_data):
        query = "DELETE FROM Searches WHERE user_id = %(user_id)s AND destination_id = %(destination_id)s;"
        return connectToMySQL(cls.db).query_db(query, search_data)