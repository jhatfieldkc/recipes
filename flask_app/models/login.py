from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Login():

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM users;'

        connection = connectToMySQL('exam')

        results = connection.query_db(query)

        exams = []

        for result in results:
            exams.append(cls(result))

        return exams

    @classmethod
    def create_user(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);'

        pw_hash = bcrypt.generate_password_hash(data['password'])

        data = {
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': data['email'],
            'password': pw_hash
        }

        connection = connectToMySQL('exam')
        results = connection.query_db(query, data)

        return results

    @classmethod
    def get_user_by_email(cls, data):

        query = "SELECT * FROM users WHERE email = %(email)s"
        connection = connectToMySQL('exam')
        results = connection.query_db(query, data)

        return results

    @staticmethod
    def validate_form(data):
        is_valid = True
        if len(data['first_name']) < 1:
            flash("First name must be at least 1 character.")
            is_valid = False

        if len(data['last_name']) < 1:
            flash("Last name must be at least 1 character.")
            is_valid = False

        # check for email validity with regular expression
        if len(Login.get_user_by_email(data)) != 0:
            flash("Email already registered.")
            is_valid = False

        if len(data['email']) < 1:
            flash("Email must be at least 1 character.")
            is_valid = False

        if len(data['password']) < 8:
            flash("Password must be at least 8 character.")
            is_valid = False

        if data['password'] != data['confirm_password']:
            flash("Password and confirm password must be the same.")
            is_valid = False

        return is_valid

    @staticmethod
    def validate_user(data):
        is_valid = True

        if not email_regex.match(data['email']): 
            flash("Invalid email address!")
            is_valid = False
        return is_valid

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("login").query_db(query,data)

        if len(result) < 1:
            return False

        return cls(result[0])