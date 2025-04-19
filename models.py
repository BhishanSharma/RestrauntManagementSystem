from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Customer(db.Model):
    cust_id = db.Column(db.Integer, primary_key=True)
    cust_fname = db.Column(db.String(100))
    cust_lname = db.Column(db.String(100))
    cust_pass = db.Column(db.String(100))
    contact_no = db.Column(db.String(15))
    orders = db.relationship('Order', backref='customer', lazy=True)
    tips = db.relationship('Tips', backref='customer', lazy=True)

    def __repr__(self):
        return f"<Customer {self.cust_fname} {self.cust_lname}>"


class Waiter(db.Model):
    waiter_id = db.Column(db.Integer, primary_key=True)
    waiter_fname = db.Column(db.String(100))
    waiter_lname = db.Column(db.String(100))
    waiter_contact = db.Column(db.String(100))
    orders = db.relationship('Order', backref='waiter', lazy=True)
    tips = db.relationship('Tips', backref='waiter', lazy=True)

    def __repr__(self):
        return f"<Waiter {self.waiter_fname} {self.waiter_lname} {self.waiter_contact}>"


class Tips(db.Model):
    cust_id = db.Column(db.Integer, db.ForeignKey('customer.cust_id'), primary_key=True)
    waiter_id = db.Column(db.Integer, db.ForeignKey('waiter.waiter_id'), primary_key=True)
    tip = db.Column(db.Float)

    def __repr__(self):
        return f"<Tip Cust:{self.cust_id} Waiter:{self.waiter_id} Tip:{self.tip}>"


class Chef(db.Model):
    chef_id = db.Column(db.Integer, primary_key=True)
    chef_fname = db.Column(db.String(100))
    chef_lname = db.Column(db.String(100))
    chef_type = db.Column(db.String(50))

    def __repr__(self):
        return f"<Chef {self.chef_fname} {self.chef_lname} - {self.chef_type}>"


class Order(db.Model):
    ord_no = db.Column(db.Integer, primary_key=True)
    ord_date = db.Column(db.String(20))
    cust_id = db.Column(db.Integer, db.ForeignKey('customer.cust_id'))
    waiter_id = db.Column(db.Integer, db.ForeignKey('waiter.waiter_id'))
    contains = db.relationship('Contains', backref='order', lazy=True)

    def __repr__(self):
        return f"<Order #{self.ord_no} Date:{self.ord_date}>"


# connecting order with the item
class Contains(db.Model):
    ord_no = db.Column(db.Integer, db.ForeignKey('order.ord_no'), primary_key=True)
    item_no = db.Column(db.Integer, db.ForeignKey('menu.item_no'), primary_key=True)
    qty = db.Column(db.Integer)

    def __repr__(self):
        return f"<Contains Order:{self.ord_no} Item:{self.item_no} Qty:{self.qty}>"


class Menu(db.Model):
    item_no = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Unique ID for the menu item
    item_name = db.Column(db.String(100), nullable=False)  # Name of the menu item
    item_type = db.Column(db.String(50), nullable=False)  # Type/category of the menu item
    item_price = db.Column(db.Float, nullable=False)  # Price of the menu item
    item_stock = db.Column(db.Integer, nullable=False, default=0)  # Stock quantity for the item
    chef_id = db.Column(db.Integer, db.ForeignKey('chef.chef_id'), nullable=False)  # Foreign key to Chef model

    # Relationship with Chef (Assuming you have a Chef model)
    chef = db.relationship('Chef', backref=db.backref('menu_items', lazy=True))

    def __repr__(self):
        return f'<Menu {self.item_name} ({self.item_type}) - {self.item_price}>'
