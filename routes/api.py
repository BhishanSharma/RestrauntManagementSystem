from flask import Blueprint, request, jsonify
from models import db, Customer, Waiter, Chef, Tips, Order, Contains, Menu

api = Blueprint('api', __name__)

@api.route('/') # ✅✅✅
def index():
    return {"message": "Welcome to ServeSmart Backend API"}

# ------------------ Customers ------------------
@api.route('/api/customers', methods=['POST']) # ✅✅✅
def add_customer():
    data = request.get_json()
    if not data or 'fname' not in data or 'lname' not in data or 'cpass' not in data or 'contact' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    new_customer = Customer(
        cust_fname=data['fname'],
        cust_lname=data['lname'],
        cust_pass=data['cpass'],
        contact_no=data['contact']
    )
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({"message": "Customer added", "id": new_customer.cust_id}), 201

@api.route('/api/customers/login', methods=['POST'])
def login_customer():
    data = request.get_json()

    # Basic input validation
    if not data or 'contact' not in data or 'cpass' not in data:
        return jsonify({"error": "Missing contact or password"}), 400

    # Find the customer by contact
    customer = Customer.query.filter_by(contact_no=data['contact'], cust_pass=data['cpass']).first()

    if customer:
        return jsonify({
            "message": "Login successful",
            "id": customer.cust_id,
            "fname": customer.cust_fname,
            "lname": customer.cust_lname
        }), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@api.route('/api/customers', methods=['GET']) # ✅✅✅
def get_customers():
    customers = Customer.query.all()
    return jsonify([{
        "id": c.cust_id,
        "fname": c.cust_fname,
        "lname": c.cust_lname,
        "contact": c.contact_no
    } for c in customers])


# ------------------ Waiters ------------------
@api.route('/api/waiters', methods=['POST']) # ✅✅✅
def add_waiter():
    data = request.get_json()
    if not data or 'fname' not in data or 'lname' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    new_waiter = Waiter(
        waiter_fname=data['fname'],
        waiter_lname=data['lname'],
        waiter_contact=data['contact']
    )
    db.session.add(new_waiter)
    db.session.commit()
    return jsonify({"message": "Waiter added", "id": new_waiter.waiter_id}), 201

@api.route('/api/waiters', methods=['GET']) # ✅✅✅
def get_waiters():
    waiters = Waiter.query.all()
    return jsonify([{
        "id": w.waiter_id,
        "fname": w.waiter_fname,
        "lname": w.waiter_lname,
        "contact": w.waiter_contact
    } for w in waiters])


# ------------------ Chefs ------------------
@api.route('/api/chefs', methods=['POST']) # ✅✅✅
def add_chef():
    data = request.get_json()
    if not data or 'fname' not in data or 'lname' not in data or 'type' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    new_chef = Chef(
        chef_fname=data['fname'],
        chef_lname=data['lname'],
        chef_type=data['type']
    )
    db.session.add(new_chef)
    db.session.commit()
    return jsonify({"message": "Chef added", "id": new_chef.chef_id}), 201

@api.route('/api/chefs', methods=['GET']) # ✅✅✅
def get_chefs():
    chefs = Chef.query.all()
    return jsonify([{
        "id": c.chef_id,
        "fname": c.chef_fname,
        "lname": c.chef_lname,
        "type": c.chef_type
    } for c in chefs])


# ------------------ Orders ------------------
@api.route('/api/orders', methods=['POST']) # ✅✅✅
def add_order():
    data = request.get_json()
    if not data or 'ord_date' not in data or 'cust_id' not in data or 'waiter_id' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    if not Customer.query.get(data['cust_id']) or not Waiter.query.get(data['waiter_id']):
        return jsonify({"error": "Invalid customer or waiter ID"}), 404

    new_order = Order(
        ord_date=data['ord_date'],
        cust_id=data['cust_id'],
        waiter_id=data['waiter_id']
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify({"message": "Order placed", "id": new_order.ord_no}), 201

@api.route('/api/orders/<int:order_id>/add_item', methods=['POST']) # ✅✅✅
def add_item_to_order(order_id):
    data = request.get_json()
    if not data or 'item_no' not in data or 'qty' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    if not Order.query.get(order_id):
        return jsonify({"error": "Invalid order ID"}), 404
    if not Menu.query.get(data['item_no']):
        return jsonify({"error": "Invalid food item ID"}), 404

    contains = Contains(
        ord_no=order_id,
        item_no=data['item_no'],
        qty=data['qty']
    )
    db.session.add(contains)
    db.session.commit()
    return jsonify({"message": "Item added to order"}), 201


# ------------------ Tips ------------------
@api.route('/api/tips', methods=['POST']) # ✅✅✅
def add_tip():
    data = request.get_json()
    if not data or 'cust_id' not in data or 'waiter_id' not in data or 'tip' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    if not Customer.query.get(data['cust_id']) or not Waiter.query.get(data['waiter_id']):
        return jsonify({"error": "Invalid customer or waiter ID"}), 404

    new_tip = Tips(
        cust_id=data['cust_id'],
        waiter_id=data['waiter_id'],
        tip=data['tip']
    )
    db.session.add(new_tip)
    db.session.commit()
    return jsonify({"message": "Tip recorded"}), 201


# ------------------ Billing ------------------
@api.route('/api/bill/<int:ord_no>', methods=['GET']) # ✅✅✅
def generate_bill(ord_no):
    # Fetch the order
    order = Order.query.get(ord_no)
    if not order:
        return jsonify({"message": "Order not found"}), 404

    # Get related customer and waiter info
    customer = order.customer
    waiter = order.waiter

    # Generate itemized bill
    bill_items = []
    total_amount = 0.0

    for c in order.contains:
        menu_item = Menu.query.get(c.item_no)
        if not menu_item:
            continue  # Skip missing items

        line_total = menu_item.item_price * c.qty
        total_amount += line_total

        bill_items.append({
            "item_id": menu_item.item_no,
            "item_name": menu_item.item_name,
            "item_type": menu_item.item_type,
            "price": menu_item.item_price,
            "quantity": c.qty,
            "total": line_total
        })

    # Create full response
    response = {
        "order_id": order.ord_no,
        "order_date": order.ord_date,
        "customer": {
            "id": customer.cust_id,
            "name": f"{customer.cust_fname} {customer.cust_lname}",
            "contact": customer.contact_no
        },
        "waiter": {
            "id": waiter.waiter_id,
            "name": f"{waiter.waiter_fname} {waiter.waiter_lname}",
            "contact": waiter.waiter_contact
        },
        "items": bill_items,
        "total_amount": round(total_amount, 2)
    }

    return jsonify(response), 200


# ------------------ Menu ------------------
@api.route('/api/menu', methods=['GET']) # ✅✅✅
def menu():
    # Fetch all food items from the database
    items = Menu.query.all()

    # Return a list of food items in the menu
    return jsonify([{
        "id": f.item_no,
        "name": f.item_name,
        "type": f.item_type,
        "price": f.item_price,
    } for f in items]), 200

# Updated By admin only
@api.route('/api/menu', methods=['POST']) # ✅✅✅
def add_menu_item():
    # Get the data from the request body
    data = request.get_json()

    # Check if the required fields are present
    if 'name' not in data or 'type' not in data or 'price' not in data or 'chef_id' not in data:
        return jsonify({"message": "Missing required fields"}), 400

    # Ensure the chef_id is valid
    chef_id = data['chef_id']
    # Assuming there's a Chef model and you can query it
    chef = Chef.query.get(chef_id)
    if not chef:
        return jsonify({"message": "Chef not found"}), 404

    # If 'stock' is not provided, set it to 0 by default
    item_stock = data.get('stock', 0)

    # Create a new Menu item
    new_item = Menu(
        item_name=data['name'],
        item_type=data['type'],
        item_price=data['price'],
        item_stock=item_stock,
        chef_id=chef_id
    )

    # Add the new item to the database
    try:
        db.session.add(new_item)
        db.session.commit()
        return jsonify({
            "id": new_item.item_no,
            "name": new_item.item_name,
            "type": new_item.item_type,
            "price": new_item.item_price,
            "stock": new_item.item_stock,
            "chef_id": new_item.chef_id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to add the item", "error": str(e)}), 500