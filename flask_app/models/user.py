from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_app.models import dinner

class User: 
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.dinners = []

    @classmethod
    def create_user(cls, data):
        print('A')
        query = "INSERT INTO users (username, email, password) VALUES (%(username)s, %(email)s, %(password)s);"
        print('B')
        return connectToMySQL('wfd').query_db(query, data)

    @classmethod
    def get_user(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('wfd').query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('wfd').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def validate_user(data):
        is_valid = True
        if len(data['username']) < 2:
            flash("Username must be at least 2 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!")
            is_valid = False
        if len(data['register_password']) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False
        if (data['register_password']) != (data['confirm_password']):
            flash("Passwords must match!")
            is_valid = False
        return is_valid