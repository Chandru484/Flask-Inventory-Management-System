from app import app, db
from models import Product, Location, ProductMovement
from datetime import datetime, timedelta
import random

def seed_database():
    # Clear existing data
    db.session.query(ProductMovement).delete()
    db.session.query(Product).delete()
    db.session.query(Location).delete()
    db.session.commit()
    
    # Create products
    products = [
        Product(product_id='LAPTOP'),
        Product(product_id='SMARTPHONE'),
        Product(product_id='TABLET'),
        Product(product_id='MONITOR')
    ]
    
    db.session.add_all(products)
    db.session.commit()
    
    # Create locations
    locations = [
        Location(location_id='WAREHOUSE'),
        Location(location_id='STORE_NORTH'),
        Location(location_id='STORE_SOUTH'),
        Location(location_id='DISTRIBUTION')
    ]
    
    db.session.add_all(locations)
    db.session.commit()
    
    # Create product movements
    movements = []
    
    # Initial stock to warehouse (inward movements)
    for product in products:
        movements.append(
            ProductMovement(
                timestamp=datetime.now() - timedelta(days=30),
                from_location=None,
                to_location='WAREHOUSE',
                product_id=product.product_id,
                qty=random.randint(50, 100)
            )
        )
    
    # Move Product A to Location X
    movements.append(
        ProductMovement(
            timestamp=datetime.now() - timedelta(days=25),
            from_location=None,
            to_location='STORE_NORTH',
            product_id='LAPTOP',
            qty=20
        )
    )
    
    # Move Product B to Location X
    movements.append(
        ProductMovement(
            timestamp=datetime.now() - timedelta(days=24),
            from_location=None,
            to_location='STORE_NORTH',
            product_id='SMARTPHONE',
            qty=30
        )
    )
    
    # Move Product A from Location X to Location Y
    movements.append(
        ProductMovement(
            timestamp=datetime.now() - timedelta(days=20),
            from_location='STORE_NORTH',
            to_location='STORE_SOUTH',
            product_id='LAPTOP',
            qty=5
        )
    )
    
    # Distribute products from warehouse to stores
    for product in products:
        for location_id in ['STORE_NORTH', 'STORE_SOUTH', 'DISTRIBUTION']:
            movements.append(
                ProductMovement(
                    timestamp=datetime.now() - timedelta(days=random.randint(15, 20)),
                    from_location='WAREHOUSE',
                    to_location=location_id,
                    product_id=product.product_id,
                    qty=random.randint(5, 15)
                )
            )
    
    # Some returns to warehouse
    for product in products:
        movements.append(
            ProductMovement(
                timestamp=datetime.now() - timedelta(days=random.randint(5, 10)),
                from_location=random.choice(['STORE_NORTH', 'STORE_SOUTH']),
                to_location='WAREHOUSE',
                product_id=product.product_id,
                qty=random.randint(1, 3)
            )
        )
    
    # Some outgoing shipments (outward movements)
    for _ in range(4):
        product = random.choice(products)
        movements.append(
            ProductMovement(
                timestamp=datetime.now() - timedelta(days=random.randint(1, 5)),
                from_location=random.choice(['WAREHOUSE', 'DISTRIBUTION']),
                to_location=None,
                product_id=product.product_id,
                qty=random.randint(1, 10)
            )
        )
    
    db.session.add_all(movements)
    db.session.commit()
    
    print(f"Database seeded with {len(products)} products, {len(locations)} locations, and {len(movements)} movements.")

if __name__ == '__main__':
    with app.app_context():
        seed_database()