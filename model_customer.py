# Name: Hoang Minh Huy Luu
# Student id: 35097426
# Creation date: 30/3/2024
# Last modified: 21/4/2024
# High-level description: this is customer model class
from model_user import User


class Customer(User):
    def __init__(self, user_id, user_name, user_password, user_register_time="00-00-0000_00:00:00", user_role="customer", user_email=None, user_mobile=None):
        super().__init__(user_id, user_name, user_password, user_register_time, user_role)
        self.user_email = user_email
        self.user_mobile = user_mobile

    def __str__(self):
        customer_info = super().__str__().rstrip("}")
        customer_info += f", 'user_email':'{self.user_email}', 'user_mobile':'{self.user_mobile}'}}"
        return customer_info
