from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

# Initialize the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = '283003'

# Configure the MySQL database connection
connection_string = 'mysql://root:Qetuoadg%402@localhost/restaurant'
app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and Flask-Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Database Models

# Customer Table
class Customer(db.Model):
    __tablename__ = 'customer'
    cust_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cust_name = db.Column(db.String(100), nullable=False)
    cust_mail = db.Column(db.String(100), nullable=False)
    cust_phone = db.Column(db.String(20), nullable=False)

# Customer Log Table (3NF-compliant)
class CustomerLog(db.Model):
    __tablename__ = 'customer_log'
    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cust_id = db.Column(db.Integer, db.ForeignKey('customer.cust_id'), nullable=False)
    log_type = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Table Information
class Table(db.Model):
    __tablename__ = 'table'
    table_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    total_people = db.Column(db.Integer, nullable=False)

# Reservation Table
class Reservation(db.Model):
    __tablename__ = 'reservation'
    reservation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    table_id = db.Column(db.Integer, db.ForeignKey('table.table_id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.cust_id'), nullable=False)
    reservation_time = db.Column(db.DateTime, nullable=False)

# Menu Item Table
class MenuItem(db.Model):
    __tablename__ = 'menu_item'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)

# Order Table
class Order(db.Model):
    __tablename__ = 'order'
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.cust_id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)

# Staff Table
class Staff(db.Model):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

# Feedback Table
class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comments = db.Column(db.String(500), nullable=True)

# Initialize the database
with app.app_context():
    db.create_all()

# Manager Credentials
MANAGER_USERNAME = "manager"
MANAGER_PASSWORD = "password123"

# Routes

# Login Route

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Verify manager credentials
        if username == MANAGER_USERNAME and password == MANAGER_PASSWORD:
            session['manager_logged_in'] = True
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            error = 'Invalid credentials. Please try again.'
    
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('manager_logged_in', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))
# Home Page
@app.route('/')
def index():
    if 'manager_logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

# Reservation Staff: Manage Tables
@app.route('/reservation', methods=['GET', 'POST'])
def manage_reservations():
    if request.method == 'POST':
        table_id = request.form['table_id']
        reservation_time = request.form['reservation_time']
        
        new_reservation = Reservation(table_id=table_id, reservation_time=reservation_time)
        db.session.add(new_reservation)
        db.session.commit()
        
        flash('Reservation added successfully!', 'success')
        return redirect(url_for('manage_reservations'))

    reservations = Reservation.query.all()
    return render_template('manage_reservations.html', reservations=reservations)

@app.route('/reservation/delete/<int:id>', methods=['GET', 'POST'])
def delete_reservation(id):
    reservation = Reservation.query.get_or_404(id)
    db.session.delete(reservation)
    db.session.commit()
    flash('Reservation deleted successfully!', 'success')
    return redirect(url_for('manage_reservations'))
# @app.route('/reservation', methods=['GET', 'POST'])
# def manage_reservations():
#     if request.method == 'POST':
#         # Handle form submission to add new reservation
#       # Defaults to 'Guest' if not provided
#         table_id = request.form['table_id']
#         reservation_time = request.form['reservation_time']
        
#         # Create a new reservation object with customer_name
#         new_reservation = Reservation( table_id=table_id, reservation_time=reservation_time)
        
#         # Add new reservation to the database
#         db.session.add(new_reservation)
#         db.session.commit()
        
#         flash('Reservation added successfully!', 'success')
#         return redirect(url_for('manage_reservations'))

#     # Handle GET request to display reservations
#     reservations = Reservation.query.all()
#     return render_template('reservation.html', reservations=reservations)

@app.route('/tables', methods=['GET', 'POST'])
def tables():
    if request.method == 'POST':
        total_people = request.form.get('total_people')
        reservation_time = request.form.get('reservation_time')  # Time the reservation is made
        new_table = Table(total_people=total_people, reservation_time=reservation_time, is_reserved=True)
        db.session.add(new_table)
        db.session.commit()
        return redirect(url_for('tables'))

    tables = Table.query.all()
    return render_template('tables.html', tables=tables)
# Reservation Staff: Delete Table
@app.route('/tables/delete/<int:table_id>', methods=['POST'])
def delete_table(table_id):
    table = Table.query.get_or_404(table_id)  # Ensure the table exists
    print(f"Deleting Table: {table_id}")  # Debugging print statement
    db.session.delete(table)
    db.session.commit()
    print(f"Table {table_id} deleted successfully.")  # Debugging print statement
    return redirect(url_for('tables'))


# Kitchen: Manage Orders
@app.route('/kitchen', methods=['GET', 'POST'])
def kitchen():
    orders = Order.query.all()
    return render_template('kitchen.html', orders=orders)

# Kitchen: Update Order Status
@app.route('/kitchen/update/<int:order_id>', methods=['POST'])
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    order.status = request.form.get('status')  # New status (e.g., "In Progress", "Completed")
    db.session.commit()
    return redirect(url_for('kitchen'))

    

# Manage Menu Items
@app.route('/items', methods=['GET', 'POST'])
def manage_items():
    if request.method == 'POST':
        data = request.form
        new_item = MenuItem(name=data['name'], description=data['description'], price=data['price'])
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('manage_items'))
    
    items = MenuItem.query.all()
    return render_template('items.html', items=items)

# @app.route('/items/edit/<int:item_id>', methods=['GET', 'POST'])
# def edit_item(item_id):
#     item = Item.query.get(item_id)  # Assuming 'Item' is the model name for menu items

#     if request.method == 'POST':
#         item.name = request.form['name']
#         item.description = request.form['description']
#         item.price = request.form['price']
#         db.session.commit()
#         flash('Item updated successfully!', 'success')
#         return redirect(url_for('items'))

#     return render_template('edit_item.html', item=item)

# @app.route('/items/delete/<int:item_id>', methods=['POST'])
# def delete_item(item_id):
#     item = Item.query.get(item_id)
    
#     if item:
#         db.session.delete(item)
#         db.session.commit()
#         flash('Item deleted successfully!', 'success')
#     else:
#         flash('Item not found!', 'error')

#     return redirect(url_for('items'))



# Customer Feedback
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        data = request.form
        new_feedback = Feedback(name=data['name'], email=data['email'], rating=data['rating'], comments=data['comments'])
        db.session.add(new_feedback)
        db.session.commit()
        return redirect(url_for('feedback'))

    feedbacks = Feedback.query.all()
    return render_template('feedback.html', feedbacks=feedbacks)

# Manage Customers
@app.route('/customer', methods=['GET', 'POST'])
def customer():
    if request.method == 'POST':
        cust_name = request.form.get('cust_name')
        cust_mail = request.form.get('cust_mail')
        cust_phone = request.form.get('cust_phone')
        
        new_customer = Customer(cust_name=cust_name, cust_mail=cust_mail, cust_phone=cust_phone)
        db.session.add(new_customer)
        db.session.commit()
        
        return redirect(url_for('customer'))

    customers = Customer.query.all()
    return render_template('customer.html', customers=customers)

# Edit Customer
@app.route('/customer/edit/<int:cust_id>', methods=['GET', 'POST'])
def edit_customer(cust_id):
    customer = Customer.query.get_or_404(cust_id)
    if request.method == 'POST':
        customer.cust_name = request.form.get('cust_name')
        customer.cust_mail = request.form.get('cust_mail')
        customer.cust_phone = request.form.get('cust_phone')
        db.session.commit()
        return redirect(url_for('customer'))
    return render_template('edit_customer.html', customer=customer)

# Delete Customer
@app.route('/customer/delete/<int:cust_id>', methods=['POST'])
def delete_customer(cust_id):
    customer = Customer.query.get_or_404(cust_id)
    db.session.delete(customer)
    db.session.commit()
    return redirect(url_for('customer'))

# Orders
@app.route('/orders', methods=['GET', 'POST'])
def orders():
    if request.method == 'POST':
        customer_id = request.form.get('customer_id')
        item_id = request.form.get('item_id')
        quantity = request.form.get('quantity')
        
        new_order = Order(customer_id=customer_id, item_id=item_id, quantity=quantity)
        db.session.add(new_order)
        db.session.commit()
        
        return redirect(url_for('orders'))

    orders = Order.query.all()
    menu_items = MenuItem.query.all()  # Fetch all menu items for the form
    return render_template('orders.html', orders=orders, menu_items=menu_items)

# Edit Order
@app.route('/orders/edit/<int:order_id>', methods=['GET', 'POST'])
def edit_order(order_id):
    order = Order.query.get_or_404(order_id)
    if request.method == 'POST':
        order.customer_id = request.form.get('customer_id')
        order.item_id = request.form.get('item_id')
        order.quantity = request.form.get('quantity')
        db.session.commit()
        return redirect(url_for('orders'))
    menu_items = MenuItem.query.all()
    return render_template('edit_order.html', order=order, menu_items=menu_items)

# Delete Order
@app.route('/orders/delete/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return redirect(url_for('orders'))

# Custom 404 Error Handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/staff', methods=['GET', 'POST'])
def manage_staff():
    if request.method == 'POST':
        # Handle adding new staff
        staff_name = request.form['staff_name']
        staff_phone = request.form['staff_phone']
        staff_position = request.form['staff_type']  # Changed variable name to match form field
        
        # Create a new staff member
        new_staff = Staff(
            name=staff_name,
            phone=staff_phone,
            position=staff_position  # Use position instead of type
        )
        db.session.add(new_staff)
        db.session.commit()
        flash('New staff member added!', 'success')
        return redirect(url_for('manage_staff'))

    # For GET requests, retrieve all staff members
    staff_members = Staff.query.all()
    return render_template('staff.html', staff_members=staff_members)

@app.route('/staff/delete/<int:staff_id>', methods=['POST'])
def delete_staff(staff_id):
    staff_member = Staff.query.get(staff_id)
    if staff_member:
        db.session.delete(staff_member)
        db.session.commit()
        flash('Staff member deleted!', 'success')
    return redirect(url_for('manage_staff'))


@app.route('/contact')
def contact():
    return render_template('contact.html')



if __name__ == '__main__':
    app.run(debug=True, port=5001)
