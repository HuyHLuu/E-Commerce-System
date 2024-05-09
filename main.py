# Name: Hoang Mnh Huy Luu
# Student id: 35097426
# Creation date: 30/3/2024
# Last modified: 21/4/2024
# High-level description: this is the main control logic for the application

from io_interface import IOInterface
from operation_admin import AdminOperation
from operation_customer import CustomerOperation
from operation_order import OrderOperation
from operation_user import UserOperation
from opreation_product import ProductOperation


def main():
    # Register admin account
    AdminOperation.register_admin()

    # Extract the products from the csv files
    ProductOperation.extract_products_from_files()

    interface = IOInterface()
    while True:
        try:
            choice = interface.main_menu()
            login_control(choice)
            if choice == 3:
                IOInterface.print_message('Exiting the program')
                break
        except Exception as e:
            IOInterface.print_message(e)
            continue


def login_control(choice):
    if choice == 1:
        user_name = IOInterface.get_user_input('Enter your user name: ', 1)[0]
        password = IOInterface.get_user_input('Enter your password: ', 1)[0]
        customer = UserOperation.login(user_name, password)
        if (customer and customer.user_role == 'customer'):
            IOInterface.print_message('Password is correct, you are in as customer')

            while True:
                choice_customer = customer_control(customer)
                if choice_customer == 6:
                    break
        elif (customer and customer.user_role == 'admin'):
            IOInterface.print_message('Password is correct, you are in as admin')

            while True:
                choice_admin = admin_control()
                if choice_admin == 8:
                    break
        else:
            IOInterface.print_message('Username or password incorrect, please try again!')
    elif choice == 2:
        user_name = IOInterface.get_user_input('Enter your user name: ', 1)[0]
        password = IOInterface.get_user_input('Enter your password: ', 1)[0]
        user_email = IOInterface.get_user_input('Enter your email address: ', 1)[0]
        user_mobile = IOInterface.get_user_input('Enter your mobile number: ', 1)[0]

        if CustomerOperation.register_customer(user_name, password, user_email, user_mobile):
            IOInterface.print_message('User registered successfully!')
    elif choice == 3:
        IOInterface.print_message('User choose to exit')


def customer_control(customer):
    menu = IOInterface.customer_menu()
    choice = menu[0]
    keyword = menu[1]
    if (choice == 1):
        IOInterface.print_message('Your profile')
        IOInterface.print_message(f"User name: {customer.user_name}")
        IOInterface.print_message(f"User email address: {customer.user_email} ")
        IOInterface.print_message(f"User mobile number: {customer.user_mobile}")

    elif (choice == 2):
        IOInterface.print_message('Please choose which attribute do you want to update:')
        IOInterface.print_message('1: User name')
        IOInterface.print_message('2: User mobile')
        IOInterface.print_message('3: User email')
        IOInterface.print_message('4: User password')
        update_choice = IOInterface.get_user_input('Enter your choice: ', 1)[0]
        if update_choice == '1':
            name = IOInterface.get_user_input("Input user name:", 1)[0]
            if CustomerOperation.update_profile('user_name', name, customer):
                IOInterface.print_message('User name updated successfully')
        elif update_choice == '2':
            name = IOInterface.get_user_input("Input user mobile:", 1)[0]
            if CustomerOperation.update_profile('user_mobile', name, customer):
                IOInterface.print_message('User mobile updated successfully')
        elif update_choice == '3':
            name = IOInterface.get_user_input("Input user email:", 1)[0]
            if CustomerOperation.update_profile('user_email', name, customer):
                IOInterface.print_message('User email updated successfully')
        elif update_choice == '4':
            name = IOInterface.get_user_input("Input user password:", 1)[0]
            if CustomerOperation.update_profile('user_password', name, customer):
                IOInterface.print_message('User password updated successfully')
    elif (choice == 3):

        IOInterface.print_message('List of products: ')
        products = ProductOperation.get_product_list_by_keyword(keyword)
        for product in products:
            IOInterface.print_object(product)
    elif (choice == 4):

        orders = OrderOperation.get_order_list(customer.user_id, 1)
        if (orders[2] > 0):
            IOInterface.print_message(f'Total page: {orders[2]}')
            page_number = int(IOInterface.get_user_input('Enter page number: ', 1)[0])
            while page_number <= 0 or page_number > int(orders[2]):
                IOInterface.print_message('Invalid page number, please select again')
                page_number = int(IOInterface.get_user_input('Enter page number: ', 1)[0])
            orders = OrderOperation.get_order_list(customer.user_id, page_number)
            IOInterface.show_list('customer', 'Order', orders)
        else:
            IOInterface.print_message('No orders')
    elif (choice == 5):
        IOInterface.print_message('All consumption figure is:')
        OrderOperation.generate_single_customer_consumption_figure(customer.user_id)
    elif (choice == 6):
        IOInterface.print_message('Logging out')
    return choice


def admin_control():
    choice = IOInterface.admin_menu()
    # Need to use the get product list
    if (choice == 1):
        products = ProductOperation.get_product_list(1)
        if (products[2] > 0):
            IOInterface.print_message(f'Total product page(max 10 products per page): {products[2]}')
            page_number = int(IOInterface.get_user_input('Enter page number: ', 1)[0])
            while page_number <= 0 or page_number > int(products[2]):
                IOInterface.print_message('Invalid page number, please select again')
                page_number = int(IOInterface.get_user_input('Enter page number: ', 1)[0])
            products = ProductOperation.get_product_list(page_number)
            IOInterface.show_list('admin', 'Product', products)
        else:
            IOInterface.print_message('No products found')
    elif (choice == 2):
        IOInterface.print_message('Register another customer')
        user_name = IOInterface.get_user_input("Enter new customer user name: ", 1)[0]
        password = IOInterface.get_user_input("Enter new customer password: ", 1)[0]
        user_email = IOInterface.get_user_input('Enter new customer email address: ', 1)[0]
        user_mobile = IOInterface.get_user_input('Enter new customer mobile number: ', 1)[0]

        if CustomerOperation.register_customer(user_name, password, user_email, user_mobile):
            IOInterface.print_message('User registered successfully!')
    elif (choice == 3):

        customers = CustomerOperation.get_customer_list(1)

        if customers[2] > 0:
            IOInterface.print_message(f'Total page: {customers[2]}')
            page_number = int(IOInterface.get_user_input('Enter page number: ', 1)[0])

            while page_number <= 0 or page_number > int(customers[2]):
                IOInterface.print_message('Invalid page number, please select again')
                page_number = int(IOInterface.get_user_input('Enter page number: ', 1)[0])
            customers = CustomerOperation.get_customer_list(page_number)
            IOInterface.show_list('admin', 'Customer', customers)
        else:
            IOInterface.print_message('No customer')


    elif (choice == 4):
        orders = OrderOperation.get_all_orders()
        for order in orders:
            IOInterface.print_object(order)


    elif (choice == 5):
        IOInterface.print_message('Generating test data...')
        ProductOperation.extract_products_from_files()
        OrderOperation.generate_test_order_data()
        IOInterface.print_message('Test data generated')

    elif (choice == 6):
        IOInterface.print_message('Select which figure you want to generate: ')
        IOInterface.print_message('1: Generate discount figure')
        IOInterface.print_message('2: Generate likes count figure')
        IOInterface.print_message('3: Generate category figure')
        IOInterface.print_message('4: Discount likes count figure')
        IOInterface.print_message('5: Top 10 best sellers figure')
        IOInterface.print_message('6: All customer consumption figure')
        figure_choice = IOInterface.get_user_input("Enter the graph you want to generate (from 1-6): ", 1)[0]
        while not (figure_choice.isdigit() and 0 < int(figure_choice) <= 6):
            IOInterface.print_message('Invalid input, please input again')
            figure_choice = IOInterface.get_user_input("Enter the graph you want to generate (from 1-6): ", 1)[0]

        switch = {
            1: lambda: (ProductOperation.generate_discount_figure(), 'Discount Figure generated'),
            2: lambda: (ProductOperation.generate_likes_count_figure(), 'Likes count figure generated'),
            3: lambda: (ProductOperation.generate_category_figure(), 'Category figure generated'),
            4: lambda: (
                ProductOperation.generate_discount_likes_count_figure(), 'Discount likes count figure generated'),
            5: lambda: (
                OrderOperation.generate_all_top_10_best_sellers_figure(), 'Top 10 best sellers figure generated'),
            6: lambda: (
                OrderOperation.generate_all_customers_consumption_figure(), 'All customer consumption figure generated')
        }

        func = switch.get(int(figure_choice))
        if func:
            result, message = func()
            IOInterface.print_message(message)
        else:
            print("Invalid figure choice")

    elif (choice == 7):
        IOInterface.print_message('Deleting all data...')
        OrderOperation.delete_all_orders()
        ProductOperation.delete_all_products()
        CustomerOperation.delete_all_customers()
    elif (choice == 8):
        IOInterface.print_message('Logging out')

    return choice


if __name__ == "__main__":
    main()
