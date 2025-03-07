from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask import Flask, render_template, request, redirect, url_for, flash,session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mysqldb import MySQL



app = Flask(__name__)
app.config['SECRET_KEY'] = '283003'

from datetime import datetime
mysql = MySQL(app)

# MySQL connection string
connection_string = 'mysql://root:Qetuoadg%402@localhost/restaurant'
app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define the MenuItem model
class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<MenuItem {self.name}>'

# Define the Feedback model
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comments = db.Column(db.String(500), nullable=True)

# Customer model
class Customer(db.Model):
    cust_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cust_name = db.Column(db.String(100), nullable=False)
    cust_mail = db.Column(db.String(100), nullable=False)
    cust_phone = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Customer {self.cust_name}>'

class CustomerLog(db.Model):
    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cust_id = db.Column(db.Integer, nullable=False)
    cust_name = db.Column(db.String(100), nullable=False)
    cust_mail = db.Column(db.String(100), nullable=False)
    cust_phone = db.Column(db.String(20), nullable=False)
    log_type = db.Column(db.String(10), nullable=False, default='created')  # Default set to 'created'
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<CustomerLog {self.log_id} - {self.cust_name}>'


# Define the Table model (with reservations)
class Table(db.Model):
    __tablename__ = 'table'
    
    table_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    total_people = db.Column(db.Integer, nullable=False)
    is_reserved = db.Column(db.Boolean, default=False)
    reservation_time = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f'<Table {self.table_id}>'
    
    #reservation
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100))
    table_id = db.Column(db.Integer)
    reservation_time = db.Column(db.String(100))

# Define the Order model with Foreign Key relationships
class Order(db.Model):
    __tablename__ = 'order'
    order_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.cust_id'), nullable=False)  # Foreign key to Customer
    item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'), nullable=False)  # Foreign key to MenuItem
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50))  # Order status like "In Progress", "Completed"
    
    # Define relationships
    customer = db.relationship('Customer', backref='orders')
    menu_item = db.relationship('MenuItem', backref='orders')

    def __repr__(self):
        return f'<Order {self.order_id}>'
    
    #staff
class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)


class Item(db.Model):
    __tablename__ = 'items'  # This defines the table name in the database

    # Define the columns of the table
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Primary Key
    name = db.Column(db.String(255), nullable=False)  # Item name
    description = db.Column(db.String(255), nullable=True)  # Item description (optional)
    price = db.Column(db.Float, nullable=False)  # Item price

    def __repr__(self):
        return f'<Item {self.name}, {self.price}>'

    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price


# Create the database tables
with app.app_context():
    db.create_all()

#login
MANAGER_USERNAME = "manager"
MANAGER_PASSWORD = "password123"



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

@app.route('/items/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    if request.method == 'POST':
        # Update item with form data
        item.name = request.form['name']
        item.description = request.form['description']
        item.price = float(request.form['price'])
        
        db.session.commit()
        flash('Menu item updated successfully!', 'success')
        return redirect(url_for('manage_items'))
    
    return render_template('edit_item.html', item=item)


@app.route('/items/delete/<int:item_id>', methods=['GET', 'POST'])
def delete_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Menu item deleted successfully!', 'success')
    return redirect(url_for('manage_items'))



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
        
        # Create a new customer record
        new_customer = Customer(cust_name=cust_name, cust_mail=cust_mail, cust_phone=cust_phone)
        db.session.add(new_customer)
        db.session.commit()

        # Log the new customer entry with 'created' log_type
        customer_log_entry = CustomerLog(
            cust_id=new_customer.cust_id,
            cust_name=new_customer.cust_name,
            cust_mail=new_customer.cust_mail,
            cust_phone=new_customer.cust_phone,
            log_type='created',  # Mark the log type as 'created'
            timestamp=datetime.utcnow()  # Current timestamp for the log
        )
        db.session.add(customer_log_entry)
        db.session.commit()
        
        flash('New customer added and logged successfully!', 'success')
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
        flash('Customer details updated successfully!', 'success')
        return redirect(url_for('customer'))
    return render_template('edit_customer.html', customer=customer)

@app.route('/customer/delete/<int:cust_id>', methods=['POST'])
def delete_customer(cust_id):
    customer = Customer.query.get_or_404(cust_id)
    
    # Log the customer deletion
    customer_log_entry = CustomerLog(
        cust_id=customer.cust_id,
        cust_name=customer.cust_name,
        cust_mail=customer.cust_mail,
        cust_phone=customer.cust_phone,
        log_type="deleted"
    )
    db.session.add(customer_log_entry)
    
    # Now delete the customer
    db.session.delete(customer)
    db.session.commit()

    flash('Customer deleted and logged successfully!', 'success')
    return redirect(url_for('customer'))



#trigger customer log
from sqlalchemy.sql import text

@app.route('/customer_log')
def customer_logs():
    # Use text() to wrap the raw SQL query
    logs = db.session.execute(text("SELECT * FROM customer_log")).fetchall()
    return render_template('customer_log.html', logs=logs)
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

# functio  revenue
from sqlalchemy.sql import text

@app.route('/menu_item_revenue', methods=['GET', 'POST'])
def menu_item_revenue():
    revenue = None
    if request.method == 'POST':
        menu_item_id = request.form.get('menu_item_id')
        if menu_item_id:
            try:
                # Use text() to wrap the raw SQL query
                query = text("SELECT GetMenuItemRevenue(:menu_item_id) AS revenue")
                result = db.session.execute(query, {'menu_item_id': menu_item_id})
                revenue = result.scalar()  # Extract the result
            except Exception as e:
                flash(f"An error occurred: {str(e)}", "danger")
    return render_template('menu_item_revenue.html', revenue=revenue)


# Custom 404 Error Handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
#staff
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
