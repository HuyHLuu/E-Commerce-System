# Name: Hoang Minh Huy Luu
# Student id: 35097426
# Creation date: 30/3/2024
# Last modified: 21/4/2024
# High-level description: this is order model class
class Order:
    def __init__(self, order_id, user_id, pro_id, order_time="00-00-0000_00:00:00"):
        self.order_id = order_id
        self.pro_id = pro_id
        self.user_id = user_id
        self.order_time = order_time

    def __str__(self):
        return f"{{'order_id':'{self.order_id}', 'user_id':'{self.user_id}', 'pro_id':'{self.pro_id}','order_time':'{self.order_time}'}}"