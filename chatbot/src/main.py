import dotenv
from chains.product_chain import product_chain

query = """Give me 3 bottles that zus is offering along with their price ranges"""

res = product_chain.invoke(query)

s = res.get("result")
print(s)