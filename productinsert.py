from models.productmodels import productmodel, products
from models.prodstockmodels import prodstock, productstockmodel

stock_obj = productstockmodel("Wholewheat Bread", 10, 2)
stock_obj.insert()