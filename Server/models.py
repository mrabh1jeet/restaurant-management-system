from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))



from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)

# # MySQL connection string
# connection_string = 'mysql://root:Qetuoadg%402@localhost/restaurant'
# app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# # Define the MenuItem model
# class MenuItem(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.String(200), nullable=False)
#     price = db.Column(db.Float, nullable=False)

#     def __repr__(self):
#         return f'<MenuItem {self.name}>'

# # Define the Feedback model
# class Feedback(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(100), nullable=False)
#     rating = db.Column(db.Integer, nullable=False)
#     comments = db.Column(db.String(500), nullable=True)

# # Define the Customer model
# class Customer(db.Model):
#     cust_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     cust_name = db.Column(db.String(100), nullable=False)
#     cust_mail = db.Column(db.String(100), nullable=False)
#     cust_phone = db.Column(db.String(20), nullable=False)

# # Define the Table model (with reservations)
# class Table(db.Model):
#     table_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     total_people = db.Column(db.Integer, nullable=False)
#     is_reserved = db.Column(db.Boolean, default=False)  # Indicates if the table is reserved
#     reservation_time = db.Column(db.String(50), nullable=True)  # Reserved time (could also be a DateTime)
    
#     def __repr__(self):
#         return f'<Table {self.table_id}>'

# # Define the Order model
# class Order(db.Model):
#     __tablename__ = 'order'
#     order_id = db.Column(db.Integer, primary_key=True)
#     customer_id = db.Column(db.Integer)
#     item_id = db.Column(db.Integer)
#     quantity = db.Column(db.Integer)
#     status = db.Column(db.String(50))  # Make sure this is defined in the model


#     # Define relationship with MenuItem
#     menu_item = db.relationship('MenuItem', backref='orders')

#     def __repr__(self):
#         return f'<Order {self.order_id}>'

# # Create the database tables
# with app.app_context():
#     db.create_all()

# # Home Page
# @app.route('/')
# def index():
#     return render_template('index.html')

# # Reservation Staff: Manage Tables and Reservations
# @app.route('/tables', methods=['GET', 'POST'])
# def tables():
#     if request.method == 'POST':
#         total_people = request.form.get('total_people')
#         reservation_time = request.form.get('reservation_time')  # Time the reservation is made
#         new_table = Table(total_people=total_people, reservation_time=reservation_time, is_reserved=True)
#         db.session.add(new_table)
#         db.session.commit()
#         return redirect(url_for('tables'))

#     tables = Table.query.all()
#     return render_template('tables.html', tables=tables)

# # Reservation Staff: Edit Table Reservation
# @app.route('/tables/edit/<int:table_id>', methods=['GET', 'POST'])
# def edit_table(table_id):
#     table = Table.query.get_or_404(table_id)
#     if request.method == 'POST':
#         table.total_people = request.form.get('total_people')
#         table.reservation_time = request.form.get('reservation_time')
#         db.session.commit()
#         return redirect(url_for('tables'))
#     return render_template('edit_table.html', table=table)

# # Reservation Staff: Delete Reservation (Cancel Reservation)
# @app.route('/tables/delete/<int:table_id>', methods=['POST'])
# def delete_table(table_id):
#     table = Table.query.get_or_404(table_id)
#     db.session.delete(table)
#     db.session.commit()
#     return redirect(url_for('tables'))

# # Kitchen: Manage Orders
# @app.route('/kitchen', methods=['GET', 'POST'])
# def kitchen():
#     orders = Order.query.all()
#     return render_template('kitchen.html', orders=orders)

# # Kitchen: Update Order Status
# @app.route('/kitchen/update/<int:order_id>', methods=['POST'])
# def update_order_status(order_id):
#     order = Order.query.get_or_404(order_id)
#     order.status = request.form.get('status')  # New status (e.g., "In Progress", "Completed")
#     db.session.commit()
#     return redirect(url_for('kitchen'))

# # Manage Menu Items
# @app.route('/items', methods=['GET', 'POST'])
# def manage_items():
#     if request.method == 'POST':
#         data = request.form
#         new_item = MenuItem(name=data['name'], description=data['description'], price=data['price'])
#         db.session.add(new_item)
#         db.session.commit()
#         return redirect(url_for('manage_items'))
    
#     items = MenuItem.query.all()
#     return render_template('items.html', items=items)

# # Customer Feedback
# @app.route('/feedback', methods=['GET', 'POST'])
# def feedback():
#     if request.method == 'POST':
#         data = request.form
#         new_feedback = Feedback(name=data['name'], email=data['email'], rating=data['rating'], comments=data['comments'])
#         db.session.add(new_feedback)
#         db.session.commit()
#         return redirect(url_for('feedback'))

#     feedbacks = Feedback.query.all()
#     return render_template('feedback.html', feedbacks=feedbacks)

# # Manage Customers
# @app.route('/customer', methods=['GET', 'POST'])
# def customer():
#     if request.method == 'POST':
#         cust_name = request.form.get('cust_name')
#         cust_mail = request.form.get('cust_mail')
#         cust_phone = request.form.get('cust_phone')
        
#         new_customer = Customer(cust_name=cust_name, cust_mail=cust_mail, cust_phone=cust_phone)
#         db.session.add(new_customer)
#         db.session.commit()
        
#         return redirect(url_for('customer'))

#     customers = Customer.query.all()
#     return render_template('customer.html', customers=customers)

# # Edit Customer
# @app.route('/customer/edit/<int:cust_id>', methods=['GET', 'POST'])
# def edit_customer(cust_id):
#     customer = Customer.query.get_or_404(cust_id)
#     if request.method == 'POST':
#         customer.cust_name = request.form.get('cust_name')
#         customer.cust_mail = request.form.get('cust_mail')
#         customer.cust_phone = request.form.get('cust_phone')
#         db.session.commit()
#         return redirect(url_for('customer'))
#     return render_template('edit_customer.html', customer=customer)

# # Delete Customer
# @app.route('/customer/delete/<int:cust_id>', methods=['POST'])
# def delete_customer(cust_id):
#     customer = Customer.query.get_or_404(cust_id)
#     db.session.delete(customer)
#     db.session.commit()
#     return redirect(url_for('customer'))

# # Orders
# @app.route('/orders', methods=['GET', 'POST'])
# def orders():
#     if request.method == 'POST':
#         customer_id = request.form.get('customer_id')
#         item_id = request.form.get('item_id')
#         quantity = request.form.get('quantity')
        
#         new_order = Order(customer_id=customer_id, item_id=item_id, quantity=quantity)
#         db.session.add(new_order)
#         db.session.commit()
        
#         return redirect(url_for('orders'))

#     orders = Order.query.all()
#     menu_items = MenuItem.query.all()  # Fetch all menu items for the form
#     return render_template('orders.html', orders=orders, menu_items=menu_items)

# # Edit Order
# @app.route('/orders/edit/<int:order_id>', methods=['GET', 'POST'])
# def edit_order(order_id):
#     order = Order.query.get_or_404(order_id)
#     if request.method == 'POST':
#         order.customer_id = request.form.get('customer_id')
#         order.item_id = request.form.get('item_id')
#         order.quantity = request.form.get('quantity')
#         db.session.commit()
#         return redirect(url_for('orders'))
#     menu_items = MenuItem.query.all()
#     return render_template('edit_order.html', order=order, menu_items=menu_items)

# # Delete Order
# @app.route('/orders/delete/<int:order_id>', methods=['POST'])
# def delete_order(order_id):
#     order = Order.query.get_or_404(order_id)
#     db.session.delete(order)
#     db.session.commit()
#     return redirect(url_for('orders'))

# # Custom 404 Error Handler
# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404

# if __name__ == '__main__':
#     app.run(debug=True, port=5001)
