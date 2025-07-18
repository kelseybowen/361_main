from db_connector import connectToMySQL


class User:
    db = "361_main"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
    
    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO Users ( name ) VALUES ( %(name)s );"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_user_by_name(cls, data):
        query = "SELECT * FROM Users WHERE name = %(name)s;"
        return connectToMySQL(cls.db).query_db(query, data)


class Destination:
    db = "361_main"
    def __init__(self, data):
        self.id = data['id']
        self.zip_code = data['zip_code']
        self.city_name = data['city_name']

    @classmethod
    def create_destination(cls, data):
        query = "INSERT INTO Destinations (zip_code, city_name) VALUES (%(zip_code)s, %(city_name)s);"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_destination_by_zip(cls, data):
        query = "SELECT * FROM Destinations WHERE zip_code = %(zip_code)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete_destination(cls, data):
        query = "DELETE FROM Destinations WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)


class Search:
    db = "361_main"
    def __init__(self, data):
        self.user_id = data['user_id']
        self.destination_id = data['destination_id']

    def save_search(cls, data):
        query = "INSERT INTO Searches (user_id, destination_id) VALUES (%(user_id)s, %(destination_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    def delete_search(cls, data):
        query = "DELETE FROM Searches WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)