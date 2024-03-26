from models.productmodels import productmodel

def createitem(name, type, image, price, details):
    product_obj = productmodel(name, type, image, price, details)
    product_obj.insert()
