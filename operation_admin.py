# Name: Hoang Minh Huy Luu
# Student id: 35097426
# Creation date: 30/3/2024
# Last modified: 21/4/2024
# High-level description: This is admin operation class
from datetime import datetime
from model_admin import Admin
from operation_user import UserOperation


class AdminOperation:
    @staticmethod
    def register_admin():
        """
            Register an admin user.

            This function checks if the admin is already registered. If not, it generates a unique user ID,
            sets the admin username and password, and creates an Admin object. The admin information is then saved to a file.

            Returns:
                bool: True if the admin is successfully registered, False otherwise.
        """
        # Check if admin already registered
        if UserOperation.check_username_exist("admin"):

            return False

        # Generate unique user ID
        user_id = UserOperation.generate_unique_user_id()

        # Set admin username and password
        admin_username = "admin"
        admin_password = UserOperation.encrypt_password("admin@123")

        # Get current timestamp for registration time
        register_time = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")

        # Create Admin object
        admin = Admin(user_id, admin_username, admin_password, register_time)

        # Save admin information to file
        with open("data/users.txt", "a") as file:
            file.write(str(admin) + "\n")

        return True
