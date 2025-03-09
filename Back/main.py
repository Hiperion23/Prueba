from fastapi import FastAPI
import xmlrpc.client
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

url = "https://tralsa-new-test2.odoo.com"
db = "tralsa-new-test2"
username = "api-pruebatecnica@trigono.com"
password = "12345"

def get_orders():
    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

    fields = [
        "id", "name", "create_date", "date_order", "state", "partner_id",
        "pricelist_id", "payment_term_id", "user_id", "fiscal_position_id",
        "amount_tax", "amount_untaxed", "amount_undiscounted", "amount_total"
    ]

    orders = models.execute_kw(
        db, uid, password, "sale.order", "search_read", [], {"fields": fields, "limit": 1000}
    )
    
    return orders

@app.get("/orders")
def read_orders():
    return get_orders()
