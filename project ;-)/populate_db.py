import os
import django
from django.core.management.base import BaseCommand
from decimal import Decimal
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'partlink.settings')
django.setup()

from django.contrib.auth.models import User
from products.models import Category, Product
from accounts.models import UserProfile

def create_mock_data():
    print("Starting database population...")
    
    # Categories
    categories_data = [
        ("Fasteners", "Screws, bolts, nuts, and washers."),
        ("Bearings", "Ball bearings, roller bearings, plain bearings."),
        ("Gaskets & Seals", "Rubber gaskets, O-rings, and mechanical seals."),
        ("Machined Parts", "Custom CNC machined parts from various metals."),
        ("Springs", "Compression, extension, and torsion springs."),
        ("Gears", "Spur gears, helical gears, and worm gears."),
        ("Valves", "Flow control valves, check valves."),
        ("Electrical Components", "Connectors, terminals, and switches.")
    ]
    
    categories = {}
    for name, desc in categories_data:
        cat, created = Category.objects.get_or_create(name=name, defaults={'description': desc})
        categories[name] = cat
        if created:
            print(f"Created category: {name}")

    # Users
    # Check for existing suppliers or create them
    supplier_names = ['SupplierTech', 'PrimeManufacturing', 'GlobalParts']
    suppliers = []
    
    for s_name in supplier_names:
        username = s_name.lower()
        user, created = User.objects.get_or_create(username=username, email=f"{username}@example.com")
        if created:
            user.set_password('password123')
            user.save()
            print(f"Created user: {username}")
        
        prof, p_created = UserProfile.objects.get_or_create(user=user, defaults={
            'role': 'supplier',
            'company_name': f"{s_name} Co.",
            'is_approved': True
        })
        if not p_created and not prof.is_approved:
            prof.is_approved = True
            prof.save()
            
        suppliers.append(user)

    # Products
    products_data = [
        # Fasteners
        ("M8 Stainless Steel Hex Bolt", "Fasteners", "High tensile hex bolt for heavy machinery.", "Stainless Steel 304", "Thread: M8, Length: 50mm", 15.50, 100, 5000),
        ("M4 Brass Machine Screw", "Fasteners", "Small machine screws for electronics.", "Brass", "Thread: M4, Length: 20mm", 5.00, 500, 20000),
        ("Nylon Insert Lock Nut, M10", "Fasteners", "Prevents loosening under vibration.", "Steel alloy, Nylon", "Thread: M10", 22.00, 50, 3000),
        
        # Bearings
        ("Deep Groove Ball Bearing 6205", "Bearings", "Standard ball bearing for general applications.", "Chrome Steel", "ID: 25mm, OD: 52mm, W: 15mm", 150.00, 10, 500),
        ("Tapered Roller Bearing 30204", "Bearings", "Designed taking combined loads.", "Chrome Steel", "ID: 20mm, OD: 47mm, W: 15.25mm", 320.00, 5, 200),
        ("Miniature Ball Bearing MR105ZZ", "Bearings", "Shielded miniature bearing.", "Stainless Steel", "ID: 5mm, OD: 10mm, W: 4mm", 45.00, 50, 1500),

        # Gaskets & Seals
        ("Silicone O-Ring Set", "Gaskets & Seals", "High temperature resistant O-rings.", "Silicone", "Various sizes (10mm - 50mm OD)", 75.00, 20, 1000),
        ("PTFE Flange Gasket 2 Inch", "Gaskets & Seals", "Chemical resistant gasket for piping.", "PTFE", "2 Inch nominal size", 250.00, 10, 400),
        ("Nitrile Rubber Oil Seal", "Gaskets & Seals", "Prevents oil leakage in rotary shafts.", "Nitrile Rubber", "ID: 30mm, OD: 50mm", 180.00, 15, 800),

        # Machined Parts
        ("Custom Aluminum Extrusion Profile", "Machined Parts", "Anodized aluminum profile.", "Aluminum 6061", "Length: 1000mm", 1200.00, 5, 100),
        ("Stainless Steel Mounting Bracket", "Machined Parts", "L-shaped heavy duty bracket.", "Stainless Steel 316", "100x100x5mm", 450.00, 25, 600),
        ("Brass Spacer Standoff", "Machined Parts", "Hex standoff for PCB mounting.", "Brass", "M3, Length 15mm", 12.00, 100, 5000),

        # Springs
        ("Heavy Duty Compression Spring", "Springs", "High load capacity spring.", "Spring Steel", "OD: 25mm, L: 100mm, Wire: 3mm", 85.00, 50, 1000),
        ("Stainless Steel Tension Spring", "Springs", "Corrosion resistant extension spring.", "Stainless Steel", "OD: 15mm, L: 80mm", 60.00, 50, 1200),

        # Gears
        ("Module 1 Spur Gear", "Gears", "Standard spur gear for power transmission.", "Carbon Steel", "Teeth: 40, Mod: 1, Bore: 12mm", 350.00, 5, 150),
        ("Nylon Helical Gear", "Gears", "Quiet operating gear.", "Nylon", "Teeth: 30, Mod: 1.5", 220.00, 10, 300),

        # Valves
        ("Brass Ball Valve 1/2 Inch", "Valves", "Shut-off valve for liquid/gas.", "Brass", "1/2 Inch NPT", 450.00, 10, 250),
        ("Stainless Steel Check Valve", "Valves", "One-way flow control.", "Stainless Steel 316", "1 Inch NPT", 1800.00, 2, 50)
    ]
    
    category_images = {
        "Fasteners": "products/fastener.png",
        "Bearings": "products/bearing.png",
        "Gaskets & Seals": "products/gasket.png",
        "Machined Parts": "products/machined.png",
        "Springs": "products/spring.png",
        "Gears": "products/gear.png",
        "Valves": "products/valve.png",
        "Electrical Components": "products/electrical.png"
    }

    for name, cat_name, desc, material, specs, price, min_qty, stock in products_data:
        supplier = random.choice(suppliers)
        category = categories[cat_name]
        
        prod, created = Product.objects.update_or_create(
            name=name,
            defaults={
                'supplier': supplier,
                'category': category,
                'description': desc,
                'material': material,
                'specifications': specs,
                'price_per_unit': Decimal(str(price)),
                'minimum_order_qty': min_qty,
                'stock_quantity': stock,
                'is_active': True,
                'image': category_images.get(cat_name)
            }
        )
        if created:
            print(f"Created product: {name} (Supplier: {supplier.username})")
        else:
            print(f"Updated product: {name} (Supplier: {supplier.username})")

    print("Database population complete!")

if __name__ == '__main__':
    create_mock_data()
