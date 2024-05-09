import csv
import os
import re

import matplotlib.pyplot as plt
from collections import Counter, defaultdict

from model_customer import Customer
from model_product import Product


class ProductOperation:

    @staticmethod
    def extract_products_from_files():
        """
            Function extract the product from the csv files
                Args:
                    None
                Returns:
                    None
        """
        # Specify the CSV file path

        current_directory = os.getcwd()
        product_directory = os.path.join(current_directory, "data\product")
        # Define a set to store unique product strings
        unique_products = set()

        # Loop through each file in the directory
        for filename in os.listdir(product_directory):
            if filename.endswith(".csv"):  # Check if the file is a CSV file
                csv_file_path = os.path.join(product_directory, filename)

                # Read data from the CSV file and extract necessary attributes
                with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        # Extract required attributes from each row
                        pro_id = row['id']
                        pro_model = row['model']
                        pro_category = row['category']
                        pro_name = row['name']
                        pro_current_price = row['current_price']
                        pro_raw_price = row['raw_price']
                        pro_discount = row['discount']
                        pro_likes_count = row['likes_count']

                        # Create a string representation of the product
                        product = Product(pro_id, pro_model, pro_category, pro_name, pro_current_price, pro_raw_price,
                                          pro_discount, pro_likes_count)
                        product_str = str(product)
                        # Add the product string to the set of unique products
                        unique_products.add(product_str)
                        # Write the product information to the products.txt file
                # Open the products.txt file in append mode
                with open("data/products.txt", "w", encoding="utf-8") as file:
                    # Write the unique product information to the products.txt file
                    for product_str in unique_products:
                        file.write(product_str + "\n")

    @staticmethod
    def delete_product(product_id):
        """
            Function to validate the username
            Args:
                - product_id(str): id of the product that user want to delete
            Returns:
                - True if product is deleted, False if not deleted
        """
        try:
            # Open the products.txt file in read mode
            with open("data/products.txt", "r") as file:
                lines = file.readlines()

            # Open the products.txt file in write mode to update it
            with open("data/products.txt", "w") as file:
                deleted = False
                for line in lines:
                    # Split the line to extract the product ID
                    parts = line.strip().split(',')
                    pro_id = parts[0].split(':')[1].strip("'")

                    # If the product ID matches the provided ID, skip writing this line
                    if pro_id == product_id:
                        deleted = True
                    else:
                        file.write(line)

            if deleted:
                return True  # Product deleted successfully
            else:
                return False  # Product with the provided ID not found
        except FileNotFoundError:
            return False
        except Exception as e:
            return False

    @staticmethod
    def get_product_list(page_number):
        """
            Function to get the product list base on the page number
            Args:
                - page_number: product page number
            Returns:
                - list of products
        """
        try:
            products_per_page = 10
            products = []

            # Open the products.txt file in read mode
            with open("data/products.txt", "r", encoding="utf-8") as file:
                lines = file.readlines()

            # Calculate the start and end index of products for the requested page
            start_index = (page_number - 1) * products_per_page
            end_index = min(start_index + products_per_page, len(lines))

            # Extract products for the requested page
            for line in lines[start_index:end_index]:
                pattern = r"'(.*?)':'(.*?)'"
                matches = re.findall(pattern, line)

                # Create a dictionary from the matches
                product_data = dict(matches)
                pro_id = product_data.get('pro_id', '')
                pro_model = product_data.get('pro_model', '')
                pro_category = product_data.get('pro_category', '')
                pro_name = product_data.get('pro_name', '')
                pro_current_price = product_data.get('pro_current_price', '')
                pro_raw_price = product_data.get('pro_raw_price', '')
                pro_discount = product_data.get('pro_discount', '')
                pro_likes_count = product_data.get('pro_likes_count', '')

                # Append the Product object to the products list
                product = Product(pro_id, pro_model, pro_category, pro_name, pro_current_price, pro_raw_price,
                                  pro_discount, pro_likes_count)  # Assuming Product class accepts *args
                products.append(product)

            # Calculate total number of pages
            total_pages = (len(lines) + products_per_page - 1) // products_per_page
            return (products, page_number, total_pages)

        except FileNotFoundError:
            print("Error: products.txt file not found.")
            return ([], 0, 0)
        except Exception as e:
            print(f"An error occurred: {e}")
            return ([], 0, 0)

    @staticmethod
    def get_product_list_by_keyword(keyword):
        """
            Function to get the product list by keyword
            Args:
                - keyword: keyword used to filter the products in the product list
            Returns:
                - list of matching products
        """
        matching_products = []

        try:
            with open("data/products.txt", "r", encoding="utf-8") as file:
                for line in file:

                    pattern = r"'(.*?)':'(.*?)'"
                    matches = re.findall(pattern, line)

                    # Create a dictionary from the matches
                    product_data = dict(matches)

                    pro_name = product_data.get('pro_name', '')
                    # Check if pro_name is not None and then convert it to lowercase
                    if pro_name is not None:
                        pro_name = pro_name.lower()

                    # Check if the keyword is present in any of the product attributes
                    if keyword.lower() in pro_name:
                        pro_id = product_data.get('pro_id', '')
                        pro_model = product_data.get('pro_model', '')
                        pro_category = product_data.get('pro_category', '')
                        pro_name = product_data.get('pro_name', '')
                        pro_current_price = product_data.get('pro_current_price', '')
                        pro_raw_price = product_data.get('pro_raw_price', '')
                        pro_discount = product_data.get('pro_discount', '')
                        pro_likes_count = product_data.get('pro_likes_count', '')
                        product = Product(pro_id, pro_model, pro_category, pro_name, pro_current_price, pro_raw_price,
                                          pro_discount, pro_likes_count)
                        # Add the product to the list of matching products
                        matching_products.append(product)

        except FileNotFoundError:
            print("Error: products.txt file not found.")

        return matching_products

    @staticmethod
    def get_product_by_id(product_id):
        """
            Function to find the product base on product id
                Args:
                    - product_id: id of the product to look up
                Returns:
                    - The product with the matching id
        """
        try:
            with open("data/products.txt", "r", encoding="utf-8") as file:
                for line in file:
                    # Split the line by ',' to get product attributes
                    product_info = line.strip().split(',')

                    # look for the id
                    pro_id = next(
                        (item.split(":")[1].strip().strip("'") for item in product_info if "'pro_id'" in item), None)

                    if str(product_id) == str(pro_id):
                        pattern = r"'(.*?)':'(.*?)'"
                        matches = re.findall(pattern, line)

                        # Create a dictionary from the matches
                        product_data = dict(matches)
                        pro_id = product_data.get('pro_id', '')
                        pro_model = product_data.get('pro_model', '')
                        pro_category = product_data.get('pro_category', '')
                        pro_name = product_data.get('pro_name', '')
                        pro_current_price = product_data.get('pro_current_price', '')
                        pro_raw_price = product_data.get('pro_raw_price', '')
                        pro_discount = product_data.get('pro_discount', '')
                        pro_likes_count = product_data.get('pro_likes_count', '')
                        product = Product(pro_id, pro_model, pro_category, pro_name, pro_current_price, pro_raw_price,
                                          pro_discount, pro_likes_count)

                        return product

        except FileNotFoundError:
            print("Error: products.txt file not found.")

        return None

    @staticmethod
    def generate_category_figure():
        """
            Function to generate the category figure
                Args:
                    - None
                Returns:
                    - None
        """
        # Read the product information from the file
        with open('data/products.txt', 'r') as file:
            lines = file.readlines()

        # Extract the category information for each product
        categories = []
        for line in lines:
            # Split the line by comma and extract the category from the third element
            elements = line.strip().split(',')
            category = elements[2].split(':')[1].strip("'")
            categories.append(category)

        # Count the number of products in each category
        category_counts = Counter(categories)

        # Sort the categories and counts in descending order of counts
        sorted_categories = sorted(category_counts.keys(), key=lambda x: category_counts[x], reverse=True)
        sorted_counts = [category_counts[category] for category in sorted_categories]

        # Plot the category figure
        plt.figure(figsize=(10, 6))
        plt.bar(sorted_categories, sorted_counts, color='skyblue')
        plt.xlabel('Category')
        plt.ylabel('Number of Products')
        plt.title('Category Figure')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig('data/figure/category_figure.png')
        plt.show()

    @staticmethod
    def extract_discounts_from_file():
        """
            Function to extract discount from products.txt file
                Args:
                    - None
                Returns:
                    - Discount list
        """
        # Initialize a list to store discount values
        discounts = []

        # Read product information from the products.txt file
        with open("data/products.txt", "r", encoding="utf-8") as file:
            # Loop through each line in the file
            for line in file:
                # Extract discount value using regular expression
                discount_match = re.search(r"'pro_discount'\s*:\s*'(\d+)'", line)
                if discount_match:
                    discount = float(discount_match.group(1))
                    discounts.append(discount)

        return discounts

    @staticmethod
    def generate_discount_figure():
            """
                Function to generate the discount figure
                Args:
                    - None
                Returns:
                    - None
            """
            discounts = ProductOperation.extract_discounts_from_file()

            # Categorize discounts
            less_than_30 = sum(1 for discount in discounts if discount < 30)
            between_30_and_60 = sum(1 for discount in discounts if 30 <= discount <= 60)
            greater_than_60 = sum(1 for discount in discounts if discount > 60)

            # Create labels and sizes for the pie chart
            labels = ['< 30%', '30% - 60%', '> 60%']
            sizes = [less_than_30, between_30_and_60, greater_than_60]

            # Plotting the pie chart
            plt.figure(figsize=(8, 6))
            plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
            plt.title('Proportion of Products with Discount Values')
            plt.savefig('data/figure/discount_figure.png')
            plt.show()

    @staticmethod
    def extract_discount_likes_count_from_file():
        """
            Function to extract the discount and likes count relation from file
            Args:
                - None
            Returns:
                - Discount and Likes Count lists
        """
        # Initialize lists to store discount values and likes counts
        discounts = []
        likes_counts = []

        # Read product information from the products.txt file
        with open("data/products.txt", "r", encoding="utf-8") as file:
            # Loop through each line in the file
            for line in file:
                # Extract discount value using regular expression
                discount_match = re.search(r"'pro_discount'\s*:\s*'(\d+)'", line)
                if discount_match:
                    discount = float(discount_match.group(1))
                    discounts.append(discount)

                # Extract likes count using regular expression
                likes_count_match = re.search(r"'pro_likes_count'\s*:\s*'(\d+)'", line)
                if likes_count_match:
                    likes_count = int(likes_count_match.group(1))
                    likes_counts.append(likes_count)

        return discounts, likes_counts

    @staticmethod
    def generate_discount_likes_count_figure():
        """
            Function to generate the discount and likes count relation figure
            Args:
                None
            Returns:
                None
        """
        # Extract discounts and likes counts from the file
        discounts, likes_counts = ProductOperation.extract_discount_likes_count_from_file()

        # Plotting the discounts vs likes counts
        plt.figure(figsize=(10, 6))
        plt.scatter(discounts, likes_counts, color='skyblue', alpha=0.5)
        plt.xlabel('Discount Percentage')
        plt.ylabel('Likes Count')
        plt.title('Relationship between Discount and Likes Count')
        plt.grid(True)
        plt.savefig('data/figure/discount_like_count_figure.png')
        plt.show()

    @staticmethod
    def extract_likes_count_from_file():
        """
        Function to extract the likes count from file grouped by category
        Args:
            None
        Returns:
            - A dictionary with product categories as keys and total likes count as values
        """
        # Initialize a dictionary to store total likes counts grouped by category
        likes_counts_by_category = {}

        # Read product information from the products.txt file
        with open("data/products.txt", "r", encoding="utf-8") as file:
            # Loop through each line in the file
            for line in file:
                # Extract category and likes count using regular expression
                category_match = re.search(r"'pro_category'\s*:\s*'([^']+)'", line)
                likes_count_match = re.search(r"'pro_likes_count'\s*:\s*'(\d+)'", line)
                if category_match and likes_count_match:
                    category = category_match.group(1)
                    likes_count = int(likes_count_match.group(1))
                    # Update total likes count for the category
                    if category in likes_counts_by_category:
                        likes_counts_by_category[category] += likes_count
                    else:
                        likes_counts_by_category[category] = likes_count

        return likes_counts_by_category

    @staticmethod
    def generate_likes_count_figure():
        """
        Function to generate the likes count figure grouped by category
        Args:
            None
        Returns:
            None
        """
        # Extract likes counts grouped by category
        likes_counts_by_category = ProductOperation.extract_likes_count_from_file()

        # Sort the categories by total likes count in ascending order
        sorted_categories = sorted(likes_counts_by_category.keys(), key=lambda x: likes_counts_by_category[x])

        # Create a bar chart
        plt.figure(figsize=(10, 6))
        plt.barh(sorted_categories, [likes_counts_by_category[category] for category in sorted_categories],
                 color='skyblue')
        plt.xlabel('Likes Count')
        plt.ylabel('Category')
        plt.title('Total Likes Count by Category')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('data/figure/likes_count_by_category.png')
        plt.show()

    @staticmethod
    def delete_all_products():
        """
            Function to delete all products
            Args:
                - None
            Returns:
                - None
        """
        from io_interface import IOInterface
        file_path = "data/products.txt"

        # Check if the file exists
        if os.path.exists(file_path):
            # Open the file in write mode to clear its contents
            with open(file_path, "w") as file:
                file.truncate(0)  # Clear the file contents
            IOInterface.print_message("All products have been deleted.")
        else:
            IOInterface.print_error_message('ProductOperation.delete_all_product', "Products file does not exist.")

