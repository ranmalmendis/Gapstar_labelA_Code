from django.core.management.base import BaseCommand
from products.models import Product  
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.management.base import BaseCommand

toyota_spare_parts = [
        {"name": "Toyota Air Filter", "description": "High-quality air filter for Toyota cars.", "price": 25.99, "stock_quantity": 50},
        {"name": "Toyota Oil Filter", "description": "Ensures clean oil circulates through the engine.", "price": 15.75, "stock_quantity": 75},
        {"name": "Toyota Brake Pad Set", "description": "Durable brake pads for enhanced safety.", "price": 45.00, "stock_quantity": 100},
        {"name": "Toyota Alternator", "description": "Reliable alternator for Toyota vehicles.", "price": 120.99, "stock_quantity": 30},
        {"name": "Toyota Spark Plugs", "description": "High-performance spark plugs.", "price": 22.50, "stock_quantity": 150},
        {"name": "Toyota Timing Belt", "description": "Precision-engineered timing belt.", "price": 65.00, "stock_quantity": 40},
        {"name": "Toyota Water Pump", "description": "Efficient water pump for engine cooling.", "price": 89.99, "stock_quantity": 25},
        {"name": "Toyota Clutch Kit", "description": "Complete clutch kit for smooth gear shifts.", "price": 250.00, "stock_quantity": 20},
        {"name": "Toyota Fuel Pump", "description": "Fuel pump for optimal engine performance.", "price": 145.00, "stock_quantity": 30},
        {"name": "Toyota Radiator", "description": "High-capacity radiator for engine cooling.", "price": 130.00, "stock_quantity": 25},
        {"name": "Toyota Suspension Bushing", "description": "Reduces vibration and noise.", "price": 35.00, "stock_quantity": 80},
        {"name": "Toyota Wheel Bearing", "description": "Wheel bearings for smooth driving.", "price": 40.00, "stock_quantity": 60},
        {"name": "Toyota Exhaust System", "description": "Complete exhaust system for Toyota.", "price": 320.00, "stock_quantity": 15},
        {"name": "Toyota Headlights", "description": "Bright and durable headlights.", "price": 90.00, "stock_quantity": 40},
        {"name": "Toyota Tail Lights", "description": "High-visibility tail lights.", "price": 85.00, "stock_quantity": 40},
    ]

class Command(BaseCommand):
    help = 'Inserts sample data into the Product table'
    # Sample data for Toyota spare parts
    
    
    def handle(self, *args, **options):

        # Insert data into the database
        for part in toyota_spare_parts:
            try:
                Product.objects.create(**part)
                print(f"Successfully added {part['name']}.")
            except Exception as e:
                print(f"Failed to add {part['name']}: {e}")
        # Create a sample user
        try:
            sample_user = User.objects.create_user('admin', 'ranmalmendis8@gmail.com', 'admin@1A')
            print("Test user created successfully.")
        except IntegrityError:
            print("Sample user already exists.")
        except Exception as e:
            print(f"Failed to create sample user: {e}")




        

        self.stdout.write(self.style.SUCCESS('Successfully inserted sample data into the tables.'))


