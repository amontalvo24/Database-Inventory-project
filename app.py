# Imports
from flask import Flask, request, jsonify, url_for, redirect, render_template, session, flash, get_flashed_messages
from flask_cors import CORS, cross_origin
import psycopg2 as ps
import json
from datetime import datetime

from handler import (PartHandler, UserHandler, TransactionsHandler, SuppliersHandler, SuppliesHandler, RacksHandler,
                     WarehouseHandler, IncomingHandler, OutgoingHandler, ExchangeHandler, StatisticHandler, NotebookHandler)

# Creating a Flask object
app = Flask(__name__)
# Apply CORS
CORS(app)

# Session secret key and DB credentials for connector
app.secret_key = b'a87f5efe3fe0001710d3920260314992e082602601f0037d7a9346b4de973e37'
valid_entities = ['user', 'warehouse', 'part', 'supplier', 'supplies', 'rack', 'transaction', 'incoming', 'outgoing', 'exchange']

# Creating Routes
# Home Route
@app.route("/")
def index():
    return redirect(url_for('home'))

# Home Route
@app.route("/equipazo/", methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        name = None
        if 'username' in session:
            name = session['username']
            return render_template('home.html', name=name)
        else:
            return render_template('home.html')
    elif request.method == 'POST':
        if 'username' in session:
            session.pop('username', None)
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))
    
# Login page
@app.route("/equipazo/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if auth_user(request.form.get('username'), request.form.get('password')) != 'Logged In':
            error = 'Invalid Credentials'
        else:
            flash('You were successfully logged in')
            session['username'] = request.form['username']
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

# Verifying user existence in database and authenticating password for login
#def auth_user(username, password):
#    conn = ps.connect(db)
#    cur1 = conn.cursor()
#    query = f'''select USER_PASS, count(*) from users where user_email='{username}' group by 1'''
#    cur1.execute(query)
#    user_count = cur1.fetchall()
#    # Check user exists
#    if len(user_count) == 0:
#        conn.commit()
#        conn.close()
#        return 'Invalid Credentials'
#    # Check if password matches
#    elif user_count[0][0] == password:
#        conn.commit()
#        conn.close()
#        return 'Logged In'
#    else:
#        conn.commit()
#        conn.close()
#        return 'Invalid Credentials'
#

# CRUD Operations 
# Create (Post)
# Create an entity
@app.post("/equipazo/<string:entity>/")
def create_entity(entity):
    # Valid strings: user, warehouse, rack, part, supplier, supplies, incoming, outgoing, exchange
    # Check for spelling or unsupported entity in url
    if entity not in valid_entities:
        return f'Cannot create new {entity}, check spelling or use a supported entity.'
    else:
        # Save request data
        if request.is_json:
            data = request.get_json()
        else:
            return 'Invalid data in request body.'
        # Validate user permissions
        # validate_auth(usr, data)
        if entity == 'user':
            return UserHandler().insertUser(data)
        elif entity == 'warehouse':
            return WarehouseHandler().insertWarehouse(data)
        elif entity == 'rack':
            return RacksHandler().insertRack(data)
        elif entity == 'part':
            return PartHandler().insertPart(data)
        elif entity == 'supplier':
            return SuppliersHandler().insertSupplier(data)
        elif entity == 'supplies':
            return SuppliesHandler().insertSupplies(data)
        elif entity == 'incoming':
            return IncomingHandler().insertIncoming(data)
        elif entity == 'outgoing':
            return OutgoingHandler().insertOutgoing(data)
        elif entity == 'exchange':
            return ExchangeHandler().insertExchange(data)

# Read (Get)
# Get all Entities
# Add code to view all entries of an entity
@app.get("/equipazo/<string:entity>")
def get_entity_all(entity):
    if entity not in valid_entities:
        return jsonify(message=f'Entity {entity} not found', code=404)
    elif entity == 'part':
        return PartHandler().getAllParts()
    elif entity == 'supplier':
        return SuppliersHandler().getAllSuppliers()
    elif entity == 'user':
        return UserHandler().getAllUsers()
    elif entity == 'warehouse':
        return WarehouseHandler().getAllWarehouses()
    elif entity == 'rack':
        return RacksHandler().getAllRacks()
    elif entity == 'supplies':
        return SuppliesHandler().getAllSupplies()
    elif entity == 'incoming':
        return IncomingHandler().getAllIncoming()
    elif entity == 'outgoing':
        return OutgoingHandler().getAllOutgoing()
    elif entity == 'exchange':
        return ExchangeHandler().getAllExchange()
    elif entity == 'transaction':
        return TransactionsHandler().getAllTransactions()

#    conn = ps.connect(db)
#    cur1 = conn.cursor()
#    query= f'''SELECT * FROM {entity};'''
#    cur1.execute(query)
#    result = cur1.fetchall()
#    data = []
#    col_n= []
#    for desc in cur1.description:
#        col_n.append(desc[0])
#    for row in result:
#        data.append(dict(zip(col_n, row)))
#    conn.commit()
#    conn.close()
#    return json.dumps(data, default=str, indent=4)

# Get specific entity by id
@app.get("/equipazo/<string:entity>/<int:ent_id>")
def get_entity_by_id(entity, ent_id):
    # Must validate access permission from logged in user to view an entity's data
    if entity not in valid_entities:
        return jsonify(f'Cannot find {entity}, check spelling or use a supported entity.'), 404
    else:
        if entity == 'user':
            return UserHandler().searchById(ent_id)
        elif entity == 'warehouse':
            return WarehouseHandler().searchById(ent_id)
        elif entity == 'rack':
            return RacksHandler().searchById(ent_id)
        elif entity == 'part':
            return PartHandler().searchById(ent_id)
        elif entity == 'supplier':
            return SuppliersHandler().searchById(ent_id)
#        elif entity == 'transaction':
#            return jsonify('Operation not supported'), 405
#            return TransactionsHandler().searchById(ent_id)
        elif entity == 'supplies':
            return SuppliesHandler().searchById(ent_id)
        elif entity == 'incoming':
            return IncomingHandler().searchById(ent_id)
        elif entity == 'outgoing':
            return OutgoingHandler().searchById(ent_id)
        elif entity == 'exchange':
            return ExchangeHandler().searchById(ent_id)

# Update (Put)
# Update a specific entity by id
@app.put("/equipazo/<string:entity>/<int:ent_id>")
def update_entity_by_id(entity, ent_id):
    if entity not in valid_entities:
        return jsonify(message=f'Entity {entity} not found', code=404)
    
    if request.is_json:
        data = request.get_json()
        if entity == 'user':
            return UserHandler().updateUser(ent_id,data)
        elif entity == 'warehouse':
            return WarehouseHandler().updateWarehouse(ent_id, data)
        elif entity == 'rack':
            return RacksHandler().updateRack(ent_id, data)
        elif entity == 'part':
            return PartHandler().updatePart(ent_id, data)
        elif entity == 'supplier':
            return SuppliersHandler().updateSupplier(ent_id, data)
        elif entity == 'supplies':
            return SuppliesHandler().updateSupplies(ent_id, data)
        elif entity == 'incoming':
            return IncomingHandler().updateIncoming(ent_id, data)
        elif entity == 'outgoing':
            return OutgoingHandler().updateOutgoing(ent_id, data)
        elif entity == 'exchange':
            return ExchangeHandler().updateExchange(ent_id, data)
        
# Delete (Delete)
# Delete a specific entity by id
@app.delete("/equipazo/<string:entity>/<int:ent_id>")
def delete_entity_by_id(entity, ent_id):
    if entity not in valid_entities:
        return f'Cannot find {entity}, check spelling or use a supported entity.'
    else:
        if entity == 'user':
            return UserHandler().deleteUser(ent_id)
        elif entity == 'warehouse':
            return WarehouseHandler().deleteWarehouse(ent_id)
        elif entity == 'rack':
            return RacksHandler().deleteRack(ent_id)
        elif entity == 'part':
            return PartHandler().deletePart(ent_id)
        elif entity == 'supplier':
            return SuppliersHandler().deleteSupplier(ent_id)
        elif entity == 'supplies':
            return SuppliesHandler().deleteSupplies(ent_id)


# Local Statistics Aggregates
# All require validation of access permission and input validity
# Warehouse's profit for the year
@app.post("/equipazo/warehouse/<int:id>/profit")
def get_warehouse_profit(id):
    return StatisticHandler().calculate_profit_by_year(id)

# Low stock racks - Top 5 racks with quantity under the 25% capacity threshold
@app.post("/equipazo/warehouse/<int:id>/rack/lowstock")
def get_lowstock_racks(id):
    return StatisticHandler().get_top_5_racks_under_threshold(id)

# Part material/type - Bottom 3 part types/materials in the warehouse
@app.post("/equipazo/warehouse/<int:id>/rack/material")
def get_bottom_material(id):
    return StatisticHandler().get_bottom_3_parts_type(id)

# Top 5 most expensive racks in the warehouse
@app.post("/equipazo/warehouse/<int:id>/rack/expensive")
def expensive_racks(id):
    return StatisticHandler().top_5_expensive_racks(id)


# Top 3 suppliers that supplied the given warehouse
@app.post("/equipazo/warehouse/<int:id>/transaction/suppliers")
def top_suppliers(id):
    return StatisticHandler().get_top_3_supplier_trans(id)

# Top 3 days with smallest incoming transaction costs
@app.post("/equipazo/warehouse/<int:id>/transaction/leastcost")
def lowest_cost_days(id):
    return StatisticHandler().get_bottom_3_days_smallest_incoming_price(id)

# Top 3 users that receive the most exchanges
@app.post("/equipazo/warehouse/<int:id>/users/receivesmost")
def most_exchanges_user(id):
    return StatisticHandler().get_top_3_users_most_exchanges(id)


# Global Statistics Aggregates
# All require validation of access permission 
# Top 10 Warehouses with the most racks
@app.get("/equipazo/most/rack")
def most_racks():
    return StatisticHandler().get_top_10_warehouses_most_racks()

# Top 5 Warehouses with most incoming transactions
@app.get("/equipazo/most/incoming")
def most_incoming():
    return StatisticHandler().get_top_5_warehouses_most_incoming_trans()

# Top 5 Warehouses that delivered the most exchanges
@app.get("/equipazo/most/deliver")
def most_exchange_delivered():
    return StatisticHandler().get_top_5_warehouses_most_deliveries_exchanges()

# Top 3 Users that made the most transactions
@app.get("/equipazo/most/transactions")
def most_transactions():
    return StatisticHandler().get_top_3_users_most_trans()

# Top 3 Warehouses with the least outgoing transactions
@app.get("/equipazo/least/outgoing")
def least_outgoing():
    return StatisticHandler().get_top_3_warehouses_least_outgoing_trans()

# Top 3 Warehouse's Cities with the most transactions
@app.get("/equipazo/most/city")
def most_trans_per_city():
    return StatisticHandler().get_top_3_warehouses_cities_most_trans()


@app.get("/equipazo/supplier/<int:id>/parts/supplied")
def parts_supplied_by_supplier(id):
    return StatisticHandler().parts_supplied_by_supplier(id)

@app.get("/equipazo/user/<int:id>/transactions")
def transactions_by_warehouse(id):
    return StatisticHandler().transactions_by_warehouse(id)

@app.get("/equipazo/warehouse/<int:id>/parts")
def parts_in_ware(id):
    return StatisticHandler().parts_in_ware(id)

# Voila Dashboard Routes
# Launch Dashboard Notebook
@app.route("/equipazo/dashboard/")
def render_dashboard():
    return NotebookHandler().render_notebook('equipazo.ipynb')

# Adding method to run app
if __name__ == "__main__":
         app.run(debug=True)