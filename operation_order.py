# Name: Hoang Minh Huy Luu
# Student id: 35097426
# Creation date: 30/3/2024
# Last modified: 21/4/2024
# High-level description: This is order operation class
import re
import string
from collections import defaultdict
from datetime import datetime, timedelta
import random
from matplotlib import pyplot as plt
from model_customer import Customer
from model_order import Order
from operation_customer import CustomerOperation
from operation_user import UserOperation
from opreation_product import ProductOperation


class OrderOperation:
    @staticmethod
    def generate_unique_order_id():
        """
           Generate a unique order id
                Args:
                - None

                Returns:
                - None
        """
        prefix = "o_"
        order_id = prefix + ''.join(random.choices('0123456789', k=5))
        # Check if the generated order_id already exists, if yes, generate a new one
        while OrderOperation.check_order_id_exist(order_id):
            order_id = prefix + ''.join(random.choices('0123456789', k=5))
        return order_id

    @staticmethod
    def check_order_id_exist(order_id):
        """
            Function to check if an order_is is existed in the database
                Args:
                - order_id(string): The id of the order

                Returns:
                - True if order exists, False otherwise
        """
        try:
            with open("data/orders.txt", "r") as file:
                for line in file:
                    if order_id in line:
                        return True
            return False
        except FileNotFoundError:
            return False

    @staticmethod
    def create_an_order(customer_id, product_id, create_time=None):
        """
            Function to create an order and add it to the data/orders.txt
            Args:
                - customer_id(string): The id of the customer
                - product_id(string): THe id of the product
                - create_time(string): the time when the order was created
            Returns:
                - True if order created, False otherwise
        """
        if not create_time:
            create_time = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
        order_id = OrderOperation.generate_unique_order_id()
        order_data = Order(order_id, customer_id, product_id, create_time)
        try:
            with open("data/orders.txt", "a") as file:
                file.write(str(order_data) + "\n")
            return True
        except Exception as e:
            return False

    @staticmethod
    def delete_order(order_id):
        """
            Function to remove an order from the data/orders.txt file
            Args:
                - customer_id(string): The id of the customer
            Returns:
                - True if order created, False otherwise
        """

        try:
            with open("data/orders.txt", "r") as file:
                lines = file.readlines()

            with open("data/orders.txt", "w") as file:
                for line in lines:
                    order_data = line.strip().split(',')
                    if order_data[0] != order_id:
                        file.write(line)

            return True
        except Exception as e:
            return False

    @staticmethod
    def get_order_list(customer_id, page_number):
        """
            Function to remove an order from the data/orders.txt file
            Args:
                - customer_id(string): The id of the customer
                - page_number(integer): The selected page number
            Returns:
                - True if order created, False otherwise
        """
        try:
            with open("data/orders.txt", "r") as file:
                lines = file.readlines()

            orders = []
            for line in lines:
                match = re.match(r"{'order_id':'(.*?)', 'user_id':'(.*?)', 'pro_id':'(.*?)','order_time':'(.*?)'}",
                                 line)
                if match:
                    order_id, user_id, pro_id, order_time = match.groups()
                    if user_id == customer_id:
                        orders.append(Order(order_id, user_id, pro_id, order_time))
            total_orders = len(orders)
            orders_per_page = 10
            total_pages = (total_orders + orders_per_page - 1) // orders_per_page
            start_index = (page_number - 1) * orders_per_page
            end_index = min(start_index + orders_per_page, total_orders)

            return orders[start_index:end_index], page_number, total_pages
        except Exception as e:

            return [], page_number, 0

    @staticmethod
    def generate_test_order_data():

        """
            Function to generate test users and orders data
            Args:
                - None
            Returns:
                - None
        """
        # Assume you have a list of customers and products
        products = ProductOperation.get_product_list_by_keyword('')

        customers = []  # List of customer objects
        # Generate 10 customers
        for i in range(10):
            # Generate unique user ID
            user_id = UserOperation.generate_unique_user_id()
            letters = string.ascii_lowercase
            user_name = ''.join(random.choice(letters) for _ in range(8))
            # Sample values for user_name, user_password, user_email, and user_mobile
            user_password = "password123"
            user_email = f"customer_{i}@example.com"
            user_mobile = f"0412345678"

            while not CustomerOperation.register_customer(user_name, user_password, user_email, user_mobile):
                user_name = ''.join(random.choice(letters) for _ in range(14))
            # Create Customer object
            customer = Customer(user_id, user_name, user_password, user_email=user_email, user_mobile=user_mobile)
            # Append customer to list
            customers.append(customer)

        # Iterate over each customer
        for customer in customers:
            # Generate random number of orders (between 50 and 200)
            num_orders = random.randint(50, 200)
            for _ in range(num_orders):
                # Randomly select a product
                product = random.choice(products)

                # Generate a random order time scattered over 12 months
                days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]  # Number of days in each month
                month = random.randint(1, 12)
                day = random.randint(1, days_in_month[month - 1])  # Subtract 1 from month to index correctly
                order_time = datetime.now() - timedelta(days=random.randint(0, 365))
                order_time = order_time.replace(month=month, day=day)
                OrderOperation.create_an_order(customer.user_id, product.pro_id,
                                               order_time.strftime('%d-%m-%Y_%H:%M:%S'))

    def generate_single_customer_consumption_figure(customer_id):
        """
            Function to generate a figure of consumption of a single customer base on customer_id
            Args:
                - customer_id(string): The id of the customer
            Returns:
                - None
        """
        # Step 1: Retrieve all orders for the given customer
        orders = OrderOperation.get_orders_by_customer_id(customer_id)

        # Step 2: Group orders by month and calculate total consumption for each  month
        monthly_consumption = {}
        for order in orders:
            month = datetime.strptime(order.order_time, "%d-%m-%Y_%H:%M:%S").strftime("%m")
            if month not in monthly_consumption:
                monthly_consumption[month] = 0

            product = ProductOperation.get_product_by_id(order.pro_id)

            if product.pro_current_price:
                order_price = float(product.pro_current_price)
            else:
                order_price = 0.0
            monthly_consumption[month] += order_price

        # Step 3: Generate a graph to visualize the consumption for each month
        months = sorted(list(monthly_consumption.keys()))
        consumption = list(monthly_consumption.values())

        plt.bar(months, consumption)
        plt.xlabel('Month-Year')
        plt.ylabel('Total Consumption')
        plt.title('Monthly Consumption for customer {}'.format(customer_id))
        plt.xticks(rotation=45)
        plt.savefig('data/figure/monthly_consumption.png')
        plt.tight_layout()
        plt.show()

    @staticmethod
    def get_orders_by_customer_id(customer_id):
        """
            Function to get all orders belong to a customer based on customer_id
            Args:
                - customer_id(string): The id of the customer
            Returns:
                - List of orders belonging to the customer
        """
        orders = []
        with open("data/orders.txt", "r") as file:
            for line in file:
                match = re.match(r"{'order_id':'(.*?)', 'user_id':'(.*?)', 'pro_id':'(.*?)','order_time':'(.*?)'}",
                                 line)
                if match:
                    order_id, user_id, pro_id, order_time = match.groups()

                    if str(user_id) == str(customer_id):
                        order = Order(order_id, user_id, pro_id, order_time)
                        orders.append(order)
        return orders

    @staticmethod
    def delete_all_orders():
        """
            Function to remove all orders from the data/orders.txt file
            Args:
                - None
            Returns:
                - None
        """
        from io_interface import IOInterface
        try:
            # Open the file where orders are stored in write mode
            with open('data/orders.txt', 'w') as orders_file:
                # Clear the content of the file
                orders_file.truncate(0)
                IOInterface.print_message('All orders have been deleted')

        except Exception as e:

            IOInterface.print_error_message('OrderOperation.delete_all_orders', 'Cannot delete'
                                                                                ' orders at')

    @staticmethod
    def generate_all_customers_consumption_figure():
        """
            Function to generate the consumption figure for all customers
            Args:
               - None
            Returns:
                - None
        """
        # Step 1: Retrieve all orders for all customers
        all_orders = OrderOperation.get_all_orders()
        # Step 2: Group orders by month and calculate total consumption for each month
        monthly_consumption = defaultdict(float)
        current_pro_id = None
        current_product = None
        for order in all_orders:

            month = datetime.strptime(order.order_time, "%d-%m-%Y_%H:%M:%S").strftime("%m")
            if current_pro_id != order.pro_id:
                current_product = ProductOperation.get_product_by_id(order.pro_id)
                current_pro_id = order.pro_id
            if current_product.pro_current_price:
                order_price = float(current_product.pro_current_price)
            else:
                order_price = 0.0
            monthly_consumption[month] += order_price

        # Step 3: Generate a single graph to visualize the total consumption across all months
        months = sorted(list(monthly_consumption.keys()))
        consumption = list(monthly_consumption.values())

        plt.bar(months, consumption)
        plt.xlabel('Month')
        plt.ylabel('Total Consumption')
        plt.title('Total Monthly Consumption for All Customers')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('data/figure/all_customer_consumption.png')
        plt.show()

    @staticmethod
    def generate_all_top_10_best_sellers_figure():
        """
            Function to generate top 10 sellers base on sales quantity
            Args:
                - None
            Returns:
                - None
        """
        # Step 1: Retrieve all orders
        all_orders = OrderOperation.get_all_orders()

        # Step 2: Count the quantity of each product sold
        product_sales = defaultdict(int)
        for order in all_orders:
            product_sales[order.pro_id] += 1

        # Step 3: Sort the products based on their sales quantity
        sorted_products = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)

        # Step 4: Select the top 10 best-selling products
        top_10_products = sorted_products[:10]

        # Step 5: Create a bar graph to visualize the top 10 best sellers
        product_names = []
        sales_quantity = []
        for product_id, quantity in top_10_products:
            product = ProductOperation.get_product_by_id(product_id)
            product_names.append(product.pro_name)
            sales_quantity.append(quantity)

        plt.figure(figsize=(15, 6))  # Adjust width and height as needed
        plt.barh(product_names, sales_quantity, color='skyblue')
        plt.xlabel('Product')
        plt.ylabel('Sales Quantity')
        plt.title('Top 10 Best Sellers')

        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('data/figure/top_10_best_seller.png')
        plt.show()

    @staticmethod
    def get_all_orders():
        """
            Function to get all orders in the data/orders.txt file
            Args:
                - None
            Returns:
                - List of order
        """
        orders = []
        with open('data/orders.txt', 'r') as file:
            for line in file:
                match = re.match(r"{'order_id':'(.*?)', 'user_id':'(.*?)', 'pro_id':'(.*?)','order_time':'(.*?)'}",
                                 line)
                if match:
                    order_id, user_id, pro_id, order_time = match.groups()

                    order = Order(order_id, user_id, pro_id, order_time)
                    orders.append(order)
        return orders
