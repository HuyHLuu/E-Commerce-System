# Name: Hoang Minh Huy Luu
# Student id: 35097426
# Creation date: 30/3/2024
# Last modified: 21/4/2024
# High-level description: This is user operation class
import random
import string
import re
from model_admin import Admin
from model_customer import Customer

class UserOperation:
    @staticmethod
    def generate_unique_user_id():
        """
            Function to generate a unique user id
            Args:
                -None
            Returns:
                - The user id
                """
        # Generate a 10-digit unique user ID starting with 'u_'
        user_id = 'u_' + ''.join(random.choices(string.digits, k=10))
        return user_id

    @staticmethod
    def encrypt_password(user_password):
        """
            Function to encrypt the user password
                Args:
                    - user_password(string): The password of the customer
                Returns:
                    - The encrypted password
        """
        # Generate a random string for encryption
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=len(user_password) * 2))
        # Encrypt the password
        random_iter = iter(random_string)


        #make sure we sequentially select 2 character from the random string and 1 character from the user-entered password
        encrypted_password = ''
        for password_char in  user_password:
            random_char = next(random_iter)
            encrypted_password += random_char + next(random_iter) +  password_char
        encrypted_password = '^^' + encrypted_password + '$$'

        return encrypted_password

    @staticmethod
    def decrypt_password(encrypted_password):
        """
            Function to decrypt the encrypted password
            Args:
                - encrypted_password(string): The encrypted password

            Returns:
                - Return the original password
        """
        # Remove the prefix and suffix from the encrypted password
        encrypted_password = encrypted_password[2:-2]

        # Extract the original password from the encrypted password
        original_password = ''
        for i in range(2, len(encrypted_password), 3):
            original_password += encrypted_password[i]

        return original_password

    @staticmethod
    def check_username_exist(user_name):
        """
            Function to check if the username exist in the database
            Args:
                - user_name(string): The username that needs checking
            Returns:
                - True if username found, False if username not found
        """
        try:
            # Open the users.txt file in read mode
            with open("data/users.txt", "r") as file:
                # Iterate through the lines of the file to check if the username exists
                for line in file:
                    if user_name in line:
                        return True  # Username found

            return False  # Username not found
        except FileNotFoundError:
            return False
        except Exception as e:
            return False

    @staticmethod
    def validate_username(user_name):
        """
            Function to validate the username
            Args:
                - user_name: username that needs validation
            Returns:
                - True if validation passed, False if validation not passed
        """
        # Validate the username format
        if len(user_name) < 5:
            return False
        if not all(char.isalpha() or char == '_' for char in user_name):
            return False
        return True

    @staticmethod
    def validate_password(user_password):
        """
            Function to validate the user password
            Args:
                - user_password: user password that needs validation
            Returns:
                - True if validation passed, False if validation not passed
        """
        # Validate the password format
        if len(user_password) < 5:
            return False
        if not any(char.isalpha() for char in user_password) or not any(char.isdigit() for char in user_password):
            return False
        return True

    @staticmethod
    def login(user_name, user_password):
        """
            Function to log the user in by checking the username and the user_input
            Args:
                - user_name(str): username
                - user_password(str): user password
            Returns:
                - Admin object if the username and password is admin account
                - Customer object if customer account
                - None if no account match username and password

        """
        with open("data/users.txt", "r") as file:
            for line in file:
                match = re.match(
                    r"\{'user_id':'(.*?)', 'user_name':'(.*?)', 'user_password':'(.*?)', 'user_register_time':'(.*?)', 'user_role':'(.*?)'(?:, 'user_email':'(.*?)', 'user_mobile':'(.*?)')?\}",
                    line)
                if match:
                    user_id, extracted_user_name, extracted_user_password, user_register_time, user_role, user_email, user_mobile = match.groups()

                    if user_role == 'customer' and user_name == extracted_user_name and UserOperation.decrypt_password(
                            extracted_user_password) == user_password:
                        customer = Customer(user_id, extracted_user_name, UserOperation.encrypt_password(user_password),
                                            user_register_time, 'customer', user_email, user_mobile)
                        return customer
                    elif user_role == 'admin' and user_name == extracted_user_name and UserOperation.decrypt_password(
                            extracted_user_password) == user_password:
                        admin = Admin(user_id, extracted_user_name, UserOperation.encrypt_password(user_password),
                                      user_register_time, 'admin')
                        return admin
        return None


