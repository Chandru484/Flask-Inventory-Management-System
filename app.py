from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime
import os

# Import models and db
from models import db, Product, Location, ProductMovement

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'inventory_management_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///inventory.db')
if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres://'):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the db with the app
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

# Route for Index (Welcome Page)
@app.route('/')
def index():
    return render_template('index.html')

# Routes for Dashboard
@app.route('/dashboard')
def dashboard():
    # Count statistics
    product_count = Product.query.count()
    location_count = Location.query.count()
    movement_count = ProductMovement.query.count()
    
    # Get low stock items (less than 10 items)
    low_stock_query = db.session.query(
        Product.product_id,
        func.sum(ProductMovement.qty).label('total_qty')
    ).join(ProductMovement).group_by(Product.product_id).having(func.sum(ProductMovement.qty) < 10)
    
    low_stock_count = low_stock_query.count()
    
    # Get recent movements
    recent_movements = ProductMovement.query.order_by(ProductMovement.movement_id.desc()).limit(5).all()
    
    # Prepare data for charts
    products = Product.query.all()
    product_names = [product.product_id for product in products]
    
    # Get stock levels for each product
    stock_levels = []
    for product in products:
        total_qty = db.session.query(func.sum(ProductMovement.qty)).filter(
            ProductMovement.product_id == product.product_id
        ).scalar() or 0
        stock_levels.append(total_qty)
    
    return render_template('dashboard.html', 
                          product_count=product_count,
                          location_count=location_count,
                          movement_count=movement_count,
                          low_stock_count=low_stock_count,
                          recent_movements=recent_movements,
                          product_labels=product_names,
                          stock_data=stock_levels,
                          stock_levels=stock_levels)



# Routes for Products
@app.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)

# Search route
@app.route('/search')
def search():
    query = request.args.get('query', '')
    if not query:
        return redirect(url_for('products'))
    
    # Search in products
    products = Product.query.filter(Product.product_id.like(f'%{query}%')).all()
    
    return render_template('products.html', products=products, search_query=query)

@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        product_id = request.form['product_id']
        
        # Check if product_id already exists
        existing_product = Product.query.filter_by(product_id=product_id).first()
        if existing_product:
            flash('Product ID already exists!', 'danger')
            return redirect(url_for('add_product'))
        
        # Create new product
        new_product = Product(product_id=product_id)
        db.session.add(new_product)
        db.session.commit()
        
        flash('Product added successfully!', 'success')
        return redirect(url_for('products'))
    
    return render_template('add_product.html')

@app.route('/products/edit/<product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        new_product_id = request.form['product_id']
        
        # Check if the new product_id already exists (if changed)
        if new_product_id != product_id:
            existing_product = Product.query.filter_by(product_id=new_product_id).first()
            if existing_product:
                flash('Product ID already exists!', 'danger')
                return redirect(url_for('edit_product', product_id=product_id))
        
        # Update product
        product.product_id = new_product_id
        db.session.commit()
        
        flash('Product updated successfully!', 'success')
        return redirect(url_for('products'))
    
    return render_template('edit_product.html', product=product)

@app.route('/products/delete/<product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Check if product is used in any movements
    movements = ProductMovement.query.filter_by(product_id=product_id).first()
    if movements:
        flash('Cannot delete product as it is used in product movements!', 'danger')
        return redirect(url_for('products'))
    
    db.session.delete(product)
    db.session.commit()
    
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('products'))

# Routes for Locations
@app.route('/locations')
def locations():
    locations = Location.query.all()
    return render_template('locations.html', locations=locations)

@app.route('/locations/add', methods=['GET', 'POST'])
def add_location():
    if request.method == 'POST':
        location_id = request.form['location_id']
        
        # Check if location_id already exists
        existing_location = Location.query.filter_by(location_id=location_id).first()
        if existing_location:
            flash('Location ID already exists!', 'danger')
            return redirect(url_for('add_location'))
        
        # Create new location
        new_location = Location(location_id=location_id)
        db.session.add(new_location)
        db.session.commit()
        
        flash('Location added successfully!', 'success')
        return redirect(url_for('locations'))
    
    return render_template('add_location.html')

@app.route('/locations/edit/<location_id>', methods=['GET', 'POST'])
def edit_location(location_id):
    location = Location.query.get_or_404(location_id)
    
    if request.method == 'POST':
        new_location_id = request.form['location_id']
        
        # Check if the new location_id already exists (if changed)
        if new_location_id != location_id:
            existing_location = Location.query.filter_by(location_id=new_location_id).first()
            if existing_location:
                flash('Location ID already exists!', 'danger')
                return redirect(url_for('edit_location', location_id=location_id))
        
        # Update location
        location.location_id = new_location_id
        db.session.commit()
        
        flash('Location updated successfully!', 'success')
        return redirect(url_for('locations'))
    
    return render_template('edit_location.html', location=location)

@app.route('/locations/delete/<location_id>', methods=['POST'])
def delete_location(location_id):
    location = Location.query.get_or_404(location_id)
    
    # Check if location is used in any movements
    from_movements = ProductMovement.query.filter_by(from_location=location_id).first()
    to_movements = ProductMovement.query.filter_by(to_location=location_id).first()
    
    if from_movements or to_movements:
        flash('Cannot delete location as it is used in product movements!', 'danger')
        return redirect(url_for('locations'))
    
    db.session.delete(location)
    db.session.commit()
    
    flash('Location deleted successfully!', 'success')
    return redirect(url_for('locations'))

# Routes for Product Movements
@app.route('/movements')
def movements():
    movements = ProductMovement.query.order_by(ProductMovement.timestamp.desc()).all()
    return render_template('movements.html', movements=movements)

@app.route('/movements/add', methods=['GET', 'POST'])
def add_movement():
    products = Product.query.all()
    locations = Location.query.all()
    
    if request.method == 'POST':
        product_id = request.form['product_id']
        from_location = request.form.get('from_location') or None
        to_location = request.form.get('to_location') or None
        qty = int(request.form['qty'])
        
        # Validate that at least one location is specified
        if not from_location and not to_location:
            flash('Either source or destination location must be specified!', 'danger')
            return render_template('add_movement.html', products=products, locations=locations)
        
        # Create new movement
        new_movement = ProductMovement(
            product_id=product_id,
            from_location=from_location,
            to_location=to_location,
            qty=qty,
            timestamp=datetime.now()
        )
        
        db.session.add(new_movement)
        db.session.commit()
        
        flash('Product movement recorded successfully!', 'success')
        return redirect(url_for('movements'))
    
    return render_template('add_movement.html', products=products, locations=locations)

@app.route('/movements/edit/<int:movement_id>', methods=['GET', 'POST'])
def edit_movement(movement_id):
    movement = ProductMovement.query.get_or_404(movement_id)
    products = Product.query.all()
    locations = Location.query.all()
    
    if request.method == 'POST':
        movement.product_id = request.form['product_id']
        movement.from_location = request.form.get('from_location') or None
        movement.to_location = request.form.get('to_location') or None
        movement.qty = int(request.form['qty'])
        
        # Validate that at least one location is specified
        if not movement.from_location and not movement.to_location:
            flash('Either source or destination location must be specified!', 'danger')
            return render_template('edit_movement.html', movement=movement, products=products, locations=locations)
        
        db.session.commit()
        flash('Product movement updated successfully!', 'success')
        return redirect(url_for('movements'))
    
    return render_template('edit_movement.html', movement=movement, products=products, locations=locations)

@app.route('/movements/delete/<int:movement_id>', methods=['POST'])
def delete_movement(movement_id):
    movement = ProductMovement.query.get_or_404(movement_id)
    db.session.delete(movement)
    db.session.commit()
    
    flash('Product movement deleted successfully!', 'success')
    return redirect(url_for('movements'))

# Route for Balance Report
@app.route('/report')
def report():
    # Get all products and locations
    products = Product.query.all()
    locations = Location.query.all()
    
    # Initialize the balance report data structure
    balance_report = []
    
    # Calculate balance for each product at each location
    for product in products:
        for location in locations:
            # Calculate incoming quantity (to_location = current location)
            incoming = db.session.query(db.func.sum(ProductMovement.qty)).filter(
                ProductMovement.product_id == product.product_id,
                ProductMovement.to_location == location.location_id
            ).scalar() or 0
            
            # Calculate outgoing quantity (from_location = current location)
            outgoing = db.session.query(db.func.sum(ProductMovement.qty)).filter(
                ProductMovement.product_id == product.product_id,
                ProductMovement.from_location == location.location_id
            ).scalar() or 0
            
            # Calculate balance
            balance = incoming - outgoing
            
            # Only add to report if there's a non-zero balance
            if balance != 0:
                balance_report.append({
                    'product': product,
                    'location': location,
                    'quantity': balance
                })
    
    return render_template('report.html', balance_report=balance_report)

# Dashboard functionality moved to the top of the file
    recent_movements = ProductMovement.query.order_by(ProductMovement.timestamp.desc()).limit(5).all()
    
    # Data for location distribution chart
    locations = Location.query.all()
    location_labels = [loc.location_id for loc in locations]
    location_data = []
    
    # Data for stock levels chart
    products = Product.query.all()
    product_labels = [prod.product_id for prod in products]
    product_stock = []
    
    # Calculate stock for each product at each location
    for product in products:
        total_stock = 0
        for location in locations:
            # Calculate stock at this location
            stock_in = db.session.query(func.sum(ProductMovement.qty)).filter(
                ProductMovement.product_id == product.product_id,
                ProductMovement.to_location_id == location.id
            ).scalar() or 0
            
            stock_out = db.session.query(func.sum(ProductMovement.qty)).filter(
                ProductMovement.product_id == product.product_id,
                ProductMovement.from_location_id == location.id
            ).scalar() or 0
            
            location_stock = stock_in - stock_out
            total_stock += max(0, location_stock)
            
        product_stock.append(total_stock)
        if total_stock < 10:  # Example threshold for low stock
            low_stock_count += 1
    
    # Calculate items per location for the pie chart
    for location in locations:
        location_total = 0
        for product in products:
            stock_in = db.session.query(func.sum(ProductMovement.qty)).filter(
                ProductMovement.product_id == product.product_id,
                ProductMovement.to_location_id == location.id
            ).scalar() or 0
            
            stock_out = db.session.query(func.sum(ProductMovement.qty)).filter(
                ProductMovement.product_id == product.product_id,
                ProductMovement.from_location_id == location.id
            ).scalar() or 0
            
            product_at_location = stock_in - stock_out
            if product_at_location > 0:
                location_total += product_at_location
        
        location_data.append(location_total)
    
    return render_template('dashboard.html', 
                          product_count=product_count,
                          location_count=location_count,
                          movement_count=movement_count,
                          low_stock_count=low_stock_count,
                          recent_movements=recent_movements,
                          location_labels=location_labels,
                          location_data=location_data,
                          product_labels=product_labels,
                          product_stock=product_stock)

if __name__ == '__main__':
    # Create directories if they don't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    if not os.path.exists('static'):
        os.makedirs('static')
        
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)