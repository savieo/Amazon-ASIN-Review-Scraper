from qavalidation.customfields import Item
from qavalidation.customfields import (PriceField, IntField, DatetimeField,
                   BooleanField, LatitudeField, LongitudeField,
                   EmailField, HtmldumpField, TextField)


"""
Define the class here or import items.py
"""
# class Puritan(Item):
#     package_quantity = TextField(required=True)
#     date_time_checked = DatetimeField(required=True, gt="2017-06-17")
#     product_number_of_servings = TextField(required=False, empty=True)
#     brand = TextField(required=True)
#     delivery_amount = TextField(required=True, regex="^[\d]+\.[\d]{2}$|FREE")
#     product_url = TextField(required=True)
#     currency = TextField(required=True)
#     product_rating = TextField(required=False)
#     product_code = TextField(required=True, regex="^[\d]{6}$")
#     product_image_url = TextField(required=True, regex="https\:\/\/images.*\.jpg$")
#     condition = TextField(required=True)
#     product_title = TextField(required=True)
#     product_serving_size = TextField(required=True)
#     multipack_packs = TextField(required=True, regex="^[\d]{2}$")
#     multibuy_message = TextField(required=True)
#     region = TextField(required=True, regex="^US$")
#     single_quantity = TextField(required=False)
#     price = TextField(required=False, regex="^[\d]+\.[\d]$")
#     channel = TextField(required=True)
# schema = Puritan().generate_schema()
