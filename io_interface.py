# Name: Hoang Minh Huy Luu
# Student id: 35097426
# Creation date: 30/3/2024
# Last modified: 21/4/2024
# High-level description: this class handles all the I/O operation


class IOInterface:
    @staticmethod
    def get_user_input(message, num_of_args):
        """
        Accept user input.

        Args:
        - message (str): The message to display as a prompt.
        - num_of_args (int): The number of arguments expected from the user input.

        Returns:
        - list: A list containing user input arguments. If the number of user's input arguments
                is less than `num_of_args`, the rest are returned as empty strings.
        """
        user_input = input(message).split()[:num_of_args]
        user_args = user_input + [''] * (num_of_args - len(user_input))
        return user_args

    @staticmethod
    def main_menu():
        """
        Display the main menu options.

        Returns:
        - int: The selected option.
        """
        IOInterface.print_message("Main Menu:")
        IOInterface.print_message("1. Login")
        IOInterface.print_message("2. Register")
        IOInterface.print_message("3. Quit")

        while True:
            choice = IOInterface.get_user_input("Please enter your choice: ",1)

            if choice[0].isdigit() and 1 <= int(choice[0]) <= 3:
                return int(choice[0])
            else:
                IOInterface.print_error_message('Menu choice', "Invalid choice. Please enter a number between 1 and 3.")

        return 0

    @staticmethod
    def admin_menu():
        """
        Display the admin menu options.

        Returns:
        - int: The selected option.
        """
        IOInterface.print_message("Admin Menu:")
        IOInterface.print_message("1. Show Products")
        IOInterface.print_message("2. Add Customers")
        IOInterface.print_message("3. Show Customers")
        IOInterface.print_message("4. Show Orders")
        IOInterface.print_message("5. Generate Test Data")
        IOInterface.print_message("6. Generate All Statistical Figures")
        IOInterface.print_message("7. Delete All Data")
        IOInterface.print_message("8. Logout")

        while True:
            choice = IOInterface.get_user_input("Please enter your choice: ",1)

            if choice[0].isdigit() and 1 <= int(choice[0]) <= 8:
                return int(choice[0])
            else:
                IOInterface.print_error_message("Admin menu", "Invalid choice. Please enter a number between 1 and 8.")

        return 0  # This line should never be reached

    @staticmethod
    def customer_menu():
        """
        Display the customer menu options.

        Returns:
        - tuple: (selected option, keyword)
        """
        IOInterface.print_message("Customer Menu:")
        IOInterface.print_message("1. Show Profile")
        IOInterface.print_message("2. Update Profile")
        IOInterface.print_message("3. Show Products (Enter '3' followed by keyword for search)")
        IOInterface.print_message("4. Show History Orders")
        IOInterface.print_message("5. Generate All Consumption Figures")
        IOInterface.print_message("6. Logout")

        while True:
            choice = IOInterface.get_user_input("Please enter your choice: ", 2)
            if choice[0].isdigit() and 1 <= int(choice[0]) <= 6:
                if int(choice[0]) == 3:
                    option_choice = int(choice[0])
                    keyword = choice[1]
                    return int(option_choice), keyword
                else:

                    return int(choice[0]), None
            else:
                IOInterface.print_error_message("Customer menu", "Invalid choice. Please enter a number between 1 and 8.")


        return 0, None

    @staticmethod
    def show_list(user_role, list_type, object_list):
        """
        Print out the list of objects.

        Args:
        - user_role (str): The role of the user ('admin' or 'customer').
        - list_type (str): The type of list ('Customer', 'Product', or 'Order').
        - object_list (list): The list of objects to be displayed.

        Returns:
        - None
        """
        if user_role == 'customer' and list_type == 'Customer':
            IOInterface.print_message("Access denied. You do not have permission to view customer lists.")
            return
        if list_type == 'Customer':
            IOInterface.print_message('Customers are:')
        elif list_type == 'Product':
            IOInterface.print_message('Products are:')
        elif list_type == 'Order':
            IOInterface.print_message('Orders are: ')

        for index, item in enumerate(object_list[0], start=((object_list[1]-1)*10)+1):
            IOInterface.print_message(f"Row {index}: {item}")

        IOInterface.print_message(f"Page number: {object_list[1]}")
        IOInterface.print_message(f"Total pages: {object_list[2]}")

    @staticmethod
    def print_error_message(error_source, error_message):
        """
        Prints an error message along with the source of the error.

        Args:
        - error_source (str): The source or context where the error occurred.
        - error_message (str): The error message to be displayed.

        Returns:
        - None
        """
        print(f"Error occurred in {error_source}: {error_message}")

    @staticmethod
    def print_object(target_object):
        """
        Prints the string representation of the given object.

        Args:
        - target_object: The object to be printed.

        Returns:
        - None
        """
        print(str(target_object))

    @staticmethod
    def print_message(message):
        print(message)

