# Name: Hoang Minh Huy Luu
# Student id: 35097426
# Creation date: 30/3/2024
# Last modified: 21/4/2024
# High-level description: this is product model class
class Product:
    def __init__(self, pro_id, pro_model, pro_category, pro_name, pro_current_price, pro_raw_price, pro_discount, pro_likes_count):
        self.pro_id = pro_id
        self.pro_model = pro_model
        self.pro_category = pro_category
        self.pro_name = pro_name
        self.pro_current_price = pro_current_price
        self.pro_discount = pro_discount
        self.pro_raw_price = pro_raw_price
        self.pro_likes_count = pro_likes_count


    def __str__(self):
        return f"{{'pro_id':'{self.pro_id}', 'pro_model':'{self.pro_model}', 'pro_category':'{self.pro_category}','pro_name':'{self.pro_name}', 'pro_current_price':'{self.pro_current_price}','pro_raw_price':'{self.pro_raw_price}', 'pro_discount':'{self.pro_discount}','pro_likes_count':'{self.pro_likes_count}'}}"
