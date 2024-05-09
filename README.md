# E-Commerce-System user instruction

When booting up the system, users are greeted with 3 options. Users can press 1 to log in ,2 to register account or 3 to close the program. The admin account is registered as the same time the program starts with the following:
-	Admin username: admin
-	Admin password: admin@123

If user choose 1 to log in, the program requires user to input username and password. If the username and password match an admin account, then the user is logged in as admin, else if the username matches a customer account, then the user is logged in as a customer, else if no account matches, the user is taken back to the starting screen.

If user chooses 2 to register an account, the program will prompt the user to enter the Username, user password, email address and mobile number. If the user input passes all validation, the user account will be created and stored in data/users.txt file. 

If the user is logged in as admin, the admin menu will display 6 options:

1)	Show products.
The total number of pages of products (10 products per page) will be shown to the user first. After that, the program will prompt the user to input the page number they want to view. If it is not a valid input (a number between 1 and the largest page number), the program will prompt the user to input again. If the input is valid, then the products in the selected page number will be shown.

2)	Register another customer.
The program will ask the user to enter a new customer name, password, email address and mobile number. If all the validation passes, the new customer info will be saved in data/users.txt file.
3)	Get Customer list.
The total number of pages of customers (10 customers per page) will be shown to the user first. After that, the program will prompt the user to input the page number they want to view. If it is not a valid input (a number between 1 and the largest page number), the program will prompt the user to input again. If the input is valid, then the customers in the selected page number will be shown.
4)	Show orders.
This will display all the orders to the user.
5)	Generate test data:
 	This method will publish test data by reading the product information from the csv files, create 10 customers and create orders.
6)	Generate all statistical figures: 
The programs will prompt the user to choose which type of figure the user can choose to generate: 
+ 1: Discount figure
+ 2: Likes count figure
+ 3: Category figure
+ 4: Discount likes count figure
+ 5: All top 10 best sellers figure
+ 6: All customers consumption figure
The user can input from 1 to 6 to generate 1 figure at a time, if the input is invalid, the program will ask the user to input again.
7)	Delete all data.
This option will delete all the data stored in users.txt, products.txt and orders.txt file.
8)	Logout
This option will log the user out and return the user to the starting screen.


If the user is logged in as a customer, the menu will display 6 options to choose from
1)	Show profile.
The program will display the user profile, include the username user email and mobile phone.
2)	Update profile.
The program will prompt users to choose which attribute they want to update from username, user email and user mobile phone and user password. After choosing which attribute, the user will enter the new value.
3)	Show products by keyword.
This function will allow users to search for products by keyword. Enter the keyword after 3 and a white space.
4)	Show history orders: 
The total number of pages of history orders (10 orders per page) will be shown to the user first. After that, the program will prompt the user to input the page number they want to view. If it is not a valid input (a number between 1 and the largest page number), the program will prompt the user to input again. If the input is valid, then the orders in the selected page number will be shown.

5)	Generate all consumption figure:
The program will create a figure of all the consumption of the current user. 
6)	Log out
The program will log the user out and return to the starting screen.

All the commands used to reach the task listed in section 2.11.2, section 2.11.3 and section 2.11.4: 
2.11.2: main_menu()
In main_menu function, we have 3 options
(1)User Login: call UserOperation.login(user_name, password)
(2)User Register : call CustomerOperation.register_customer(user_name, password, user_email, user_mobile)
(3)Quit: break the loop

2.11.3.admin_menu():
23 (1).Show products: call ProductOperation.get_products_list(page_number)
23 (2).Add customers : call CustomerOperation.register_customer(user_name, password, user_email, user_mobile)
(3).Show customers: call CustomerOperation.get_customer_list(1)
(4).Show orders : call OrderOperation.get_all_orders()
(5).Generate test data: 
+ Call ProductOperation.extract_product_from_files() to extract list of products
+ Call OrderOperation.generate_test_order_data() to create test orders
(6).Generate all statistical figures :
+ Call ProductOperation.generate_discount_figure()
+ Call ProductOperation.generate_likes_count_figure()
+ Call ProductOperation.generate_category_figure()
+ Call ProductOperation.generate_discount_likes_count_figure()
+ Call OrderOperation.generate_all_top_10_best_sellers_figure()
+Call OrderOperation.generate_all_customers_consumption_figure()
(7).Delete all data 
+ Call OrderOperation.delete_all_orders()
+ Call ProductOperation.delete_all_products()
+ Call CustomerOperation.delete_all_customers()
(8).Logout
Break the loop
 2.11.4.customer_menu()
(1).Show profile : Print out the customer object
(2).Update profile :
+ Call CustomerOperation.update_profile() to update username, user mobile or user email of user
(3).Show products( user input could be “3keyword” or “3”) 
+ ProductOperation.get_product_list_by_keyword(keyword)
(4) Show history orders 
OrderOperation.get_order_list(user_id, page_number)
(5).Generate all consumption figures 
OrderOperation.generate_single_customer_consumption_figure(user_id)
(6).Logout Positional Arguments 
There are some unused functions: 
ProductOperation.delet_product(product_id)
CustomerOperation.delete_customer()
