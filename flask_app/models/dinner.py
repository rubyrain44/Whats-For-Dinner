from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Dinner:
    def __init__(self, data):
        self.name = data['name']
        self.type = data['type']
        self.difficulty = data['difficulty']
        self.price = data['price']
        self.description = data['description']
        self.ingredients = data['ingredients']
        self.steps = data['steps']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None


    @classmethod
    def get_all_dinners(cls):
        query= '''
            SELECT * FROM dinners 
            LEFT JOIN users 
            ON users.id = dinners.user_id;
            '''
        results = connectToMySQL('wfd').query_db(query)
        all_dinners_with_creator = []
        for row in results:
            one_dinner = cls(row)
            dinner_creator = {
                'id': row['users.id'],
                'username': row['username'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            one_dinner.creator = user.User(dinner_creator)
            all_dinners_with_creator.append(one_dinner)
        return all_dinners_with_creator


    @classmethod
    def get_dinner(cls, data):
        query= """
                SELECT * FROM dinners
                LEFT JOIN users
                ON dinners.user_id = users.id
                WHERE dinners.id = %(id)s;
                """
        results = connectToMySQL('wfd').query_db(query, data)
        dinner = cls(results[0])
        dinner_creator = {
                'id': results[0]['users.id'],
                'username': results[0]['username'],
                "email": results[0]['email'],
                "password": results[0]['password'],
                "created_at": results[0]['users.created_at'],
                "updated_at": results[0]['users.updated_at']
            }
        dinner.creator = user.User(dinner_creator)
        return dinner

    @classmethod
    def save_dinner(cls, data):
        query = """
                INSERT INTO dinners (name, type, difficulty, price, description, ingredients, steps, user_id) 
                VALUES (%(name)s, %(type)s, %(difficulty)s, %(price)s, %(description)s, %(ingredients)s, %(steps)s, %(user_id)s);
                """
        return connectToMySQL('wfd').query_db(query, data)

    @classmethod
    def edit_dinner(cls, data):
        query = """
                UPDATE dinners SET
                name=%(name)s, type=%(type)s, difficulty=%(difficulty)s, price=%(price)s, description=%(description)s, ingredients=%(ingredients)s, steps=%(steps)s, 
                updated_at= NOW() WHERE id = %(id)s;
                """
        return connectToMySQL('wfd').query_db(query, data)

    @classmethod
    def delete_dinner(cls, data):
        query = """
                DELETE FROM dinners WHERE id = %(id)s;
                """
        return connectToMySQL('wfd').query_db(query, data)

# ====================================================================

# VALIDATIONS FOR DINNER CREATION
    @staticmethod
    def validate_dinner(form_data):
        is_valid = True
        if len(form_data['name']) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False
        return is_valid
    
# figure out a way to make sure radio is selected for validations