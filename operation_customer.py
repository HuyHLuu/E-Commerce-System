# Name: Hoang Minh Huy Luu
# Student id: 35097426
# Creation date: 30/3/2024
# Last modified: 21/4/2024
# High-level description: This is customer operation class
import re
import time
from model_customer import Customer
from operation_user import UserOperation


class CustomerOperation:
    @staticmethod
    def validate_email(user_email):
        """
        Validate the provided email address format.
        An email address consists of four parts:
        - Username: The part of the email address before the "@" symbol.
        - @ symbol: Separates the username and domain name.
        - Domain name: Refers to the mail server that stores or routes the email.
        - Dot (.): Separates a portion of the address from the domain name.
        """

        # Splitting the email address into username and domain parts
        parts = user_email.split('@')
        if len(parts) != 2:
            return False
        username, domain = parts
        if '.' not in domain or domain.index('.') == 0 or domain.index('.') == len(domain) - 1:
            return False
        return True

    @staticmethod
    def validate_mobile(user_mobile):
        """
        Validate the provided mobile number format.
        The mobile number should be exactly 10 digits long, consisting only of numbers, and
        starting with either '04' or '03'.
        """
        return user_mobile.isdigit() and (user_mobile.startswith('04') or user_mobile.startswith('03'))

    @staticmethod
    def register_customer(user_name, user_password, user_email, user_mobile):
        """
            Register a new customer into the data/users.txt file

                Args:
                    - user_name (str): username of the customer.
                    - user_password (str): user password for the customer.
                    - user_email (str): email address of the customer
                    - user_mobile (str): user mobile number
                Returns:
                    - True if success, False if fail
        """
        from io_interface import IOInterface


        if not UserOperation.validate_username(user_name):
            # Need to replace this with the print error message
            IOInterface.print_error_message('CustomerOperation.register_customer', 'Invalid user name')

            return False
        if UserOperation.check_username_exist(user_name):
            IOInterface.print_error_message('CustomerOperation.register_customer', 'User name already exist')
            return False
        # Validate the user email and mobile number
        if not CustomerOperation.validate_email(user_email):
            IOInterface.print_error_message('CustomerOperation.register_customer', 'Invalid email address')
            return False

        if not CustomerOperation.validate_mobile(
                user_mobile):
            IOInterface.print_error_message('CustomerOperation.register_customer', 'Invalid mobile number')
            IOInterface.print_message("The mobile number should be exactly 10 digits long, consisting only of numbers, "
                                      "and starting with either'04'or'03'.")
            return False
        if not UserOperation.validate_password(user_password):
            IOInterface.print_error_message('CustomerOperation.register_customer', 'Invalid password')
            IOInterface.print_message(
                "The password should contain at least one letter this letter can be either upper case or lower case) and one number.The length of the password must be greater than or equal to 5 characters.")
            return False
        # Generate a unique user ID
        user_id = UserOperation.generate_unique_user_id()

        # Get the current time
        user_register_time = time.strftime("%d-%m-%Y_%H:%M:%S")

        # Construct the customer object
        customer = Customer(user_id, user_name, UserOperation.encrypt_password(user_password), user_register_time,
                            'customer', user_email, user_mobile)

        # Write the customer information into the data/users.txt file
        with open("data/users.txt", "a") as file:
            file.write(str(customer) + "\n")

        return True

    @staticmethod
    def update_profile(attribute_name, value, customer_object):
        """
            Update an attribute in the customer profile

                Args:
                    - attribute_name (str): name of the attribute to update.
                    - value (str): the new value.
                    - customer_object(Customer): the customer object
                    Returns:
                        - True if success, False if fail
        """
        if attribute_name == 'user_email':
            # Perform validation for email format
            if not CustomerOperation.validate_email(value):
                return False
        elif attribute_name == 'user_mobile':
            # Perform validation for mobile number format
            if not CustomerOperation.validate_mobile(value):
                return False
        elif attribute_name == 'user_password':
            # Perform validation for mobile number format
            if not UserOperation.validate_password(value):
                return False
        elif attribute_name == 'user_name':
            # Perform validation for mobile number format
            if not UserOperation.validate_username(value):
                return False
        # Add more validations for other attributes if needed

        # Update the attribute value of the customer object
        setattr(customer_object, attribute_name, value)

        # Write the changes to the data/users.txt file
        with open("data/users.txt", "r") as file:
            lines = file.readlines()
        with open("data/users.txt", "w") as file:
            for line in lines:
                if customer_object.user_id in line:
                    line = str(customer_object) + "\n"
                file.write(line)

        return True

    @staticmethod
    def delete_customer(customer_id):
        """
            Delete the customer data stored in data/users.txt based in the provided customer_id
                Args:
                - customer_id (str): The id of the user

                Returns:
                - None
        """
        with open("data/users.txt", "r") as file:
            lines = file.readlines()

        # Filter out the line corresponding to the customer to be deleted
        filtered_lines = [line for line in lines if f"'user_id':'{customer_id}'" not in line]

        # Check if any line was removed
        if len(lines) == len(filtered_lines):
            # Customer not found, return False
            return False

        # Write the updated data back to the file
        with open("data/users.txt", "w") as file:
            for line in filtered_lines:
                file.write(line)

        # Return True to indicate successful deletion
        return True

    @staticmethod
    def get_customer_list(page_number):
        """
            Get the list of customer, 10 customers per page

                Args:
                - user_role (str): The role of the user ('admin' or 'customer').
                - list_type (str): The type of list ('Customer', 'Product', or 'Order').
                - object_list (list): The list of objects to be displayed.

                Returns:
                - None
                """
        # Define the number of customers per page
        customers_per_page = 10

        # Read data from the file
        with open("data/users.txt", "r") as file:
            lines = file.readlines()

        # Calculate the total number of pages
        total_pages = ((len(lines) - 1) + customers_per_page - 1) // customers_per_page

        # Determine the start and end indices of the customers for the specified page
        start_index = (page_number - 1) * customers_per_page
        end_index = min(start_index + customers_per_page, len(lines))

        # Extract the customers for the specified page
        customer_data = lines[start_index:end_index]

        # Parse the customer data and create customer objects
        customers = []
        for line in customer_data:

            match = re.match(
                r"\{'user_id':'(.*?)', 'user_name':'(.*?)', 'user_password':'(.*?)', 'user_register_time':'(.*?)', 'user_role':'(.*?)'(?:, 'user_email':'(.*?)', 'user_mobile':'(.*?)')?\}",
                line)
            if match:
                user_id, user_name, user_password, user_register_time, user_role, user_email, user_mobile = match.groups()
                if user_role == 'admin':
                    continue
                # Create a customer object
                customer = Customer(user_id, user_name, user_password, user_register_time, user_role, user_email,
                                    user_mobile)
                customers.append(customer)

        # Return the list of customers for the specified page along with total pages
        return customers, page_number, total_pages

    @staticmethod
    def delete_all_customers():

        """
            Delete all the customers data stored in data/users.txt file

            Args:
            - None

            Returns:
            - None
        """
        from io_interface import IOInterface
        try:

            # Open the file where orders are stored in write mode
            with open('data/users.txt', 'w') as users_file:
                # Clear the content of the file
                users_file.truncate(0)
                IOInterface.print_message('All customers have been deleted')

        except Exception as e:
            IOInterface.print_error_message('CustomerOperation.delete_all_customers', 'Error '
                                                                                      'occurs at')
