# Name: Hoang Minh Huy Luu
# Student id: 35097426
# Creation date: 30/3/2024
# Last modified: 21/4/2024
# High-level description: this is admin model class
from model_user import User


class Admin(User):
    def __init__(self, user_id, user_name, user_password, user_register_time="00-00-0000_00:00:00", user_role="admin"):
        super().__init__(user_id, user_name, user_password, user_register_time, user_role)

    def __str__(self):
        admin_info = super().__str__()

        return admin_info
