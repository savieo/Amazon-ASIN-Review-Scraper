from dragline.item import Item, TextField, JSONField


class Product(Item):
    Brand = TextField()
    Part_No = TextField()
    ASIN = TextField()
    Rating_Numbers = TextField()
    OE_NO = TextField()
    Price = TextField()
    Customer_Name = TextField()
    Commented_Date = TextField()
    Comments = TextField()
    Url = TextField()
    Name = TextField()
    Searched_ASIN = TextField()
    # Input_Sku = TextField()
    Results_Url = TextField()
    Best_Seller_Rank = JSONField()
    
    Review_Url = TextField()
    Item_Description = TextField()
    Item_Package_Quantity = TextField()
    Inventory = TextField()
    Ship_Info = TextField()
    Item_Weight = TextField()
    Product_Dimensions = TextField()
    Number_of_Customer_Reviews = TextField()
    Date_First_Available = TextField()

class Missing(Item):
    Asin = TextField()
    Url = TextField()