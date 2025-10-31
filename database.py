import sqlite3
from datetime import datetime
import json

DATABASE = 'herbal_garden.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS plants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            scientific_name TEXT,
            category TEXT,
            overview TEXT,
            medicinal_uses TEXT,
            cultivation TEXT,
            image_url TEXT,
            model_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            image_url TEXT,
            plant_id INTEGER,
            stock INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (plant_id) REFERENCES plants (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            customer_email TEXT NOT NULL,
            total_amount REAL NOT NULL,
            items TEXT,
            stripe_payment_id TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS community_submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plant_name TEXT NOT NULL,
            scientific_name TEXT,
            description TEXT,
            submitted_by TEXT,
            submitted_email TEXT,
            image_path TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            event_data TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def seed_data():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as count FROM plants")
    if cursor.fetchone()['count'] > 0:
        conn.close()
        return
    
    plants_data = [
        {
            'name': 'Ashwagandha',
            'scientific_name': 'Withania somnifera',
            'category': 'Adaptogen',
            'overview': 'Ashwagandha, also known as Indian ginseng, is a powerful adaptogenic herb used in Ayurvedic medicine for over 3,000 years. It is known for its rejuvenating and stress-relieving properties.',
            'medicinal_uses': 'Reduces stress and anxiety, improves brain function, lowers blood sugar and cortisol levels, helps fight symptoms of depression, boosts testosterone and fertility in men, increases muscle mass and strength, reduces inflammation, and improves heart health.',
            'cultivation': 'Grows well in dry regions with moderate temperatures (20-35°C). Requires well-drained sandy loam soil with pH 7.5-8.0. Plant spacing: 60x30 cm. Harvesting after 150-180 days when leaves turn yellow.',
            'image_url': '/static/images/ashwagandha.jpg',
            'model_url': '/static/models/ashwagandha.glb'
        },
        {
            'name': 'Tulsi',
            'scientific_name': 'Ocimum sanctum',
            'category': 'Immunity Booster',
            'overview': 'Tulsi, or Holy Basil, is considered the "Queen of Herbs" in Ayurveda. It has been revered for its medicinal properties and spiritual significance for thousands of years.',
            'medicinal_uses': 'Boosts immunity, fights respiratory infections, reduces fever, alleviates stress, supports digestive health, has anti-inflammatory properties, helps regulate blood sugar, and protects against infections.',
            'cultivation': 'Grows in tropical and subtropical regions. Prefers warm climate (25-35°C) and well-drained loamy soil. Requires full sunlight and regular watering. Can be grown from seeds or cuttings. Harvest leaves regularly for continuous growth.',
            'image_url': '/static/images/tulsi.jpg',
            'model_url': '/static/models/tulsi.glb'
        },
        {
            'name': 'Neem',
            'scientific_name': 'Azadirachta indica',
            'category': 'Purifier',
            'overview': 'Neem is known as the "Village Pharmacy" in India. Every part of the neem tree has been used in Ayurvedic and Unani medicine for centuries.',
            'medicinal_uses': 'Purifies blood, fights bacterial infections, treats skin diseases, boosts immunity, improves oral health, controls diabetes, promotes liver health, and has anti-cancer properties.',
            'cultivation': 'Hardy tree that grows in tropical and semi-tropical regions. Tolerates drought and poor soil. Prefers temperatures of 21-32°C. Grows best in deep, well-drained soil. Minimal maintenance required once established.',
            'image_url': '/static/images/neem.jpg',
            'model_url': '/static/models/neem.glb'
        },
        {
            'name': 'Brahmi',
            'scientific_name': 'Bacopa monnieri',
            'category': 'Brain Tonic',
            'overview': 'Brahmi is a renowned brain tonic in Ayurveda, traditionally used to enhance memory, learning, and concentration.',
            'medicinal_uses': 'Improves memory and cognitive function, reduces anxiety and stress, treats epilepsy, lowers blood pressure, has antioxidant effects, reduces inflammation, and supports healthy aging.',
            'cultivation': 'Aquatic or semi-aquatic plant that grows in wetlands. Requires moist, marshy soil and partial shade. Can be grown in pots with water. Propagates easily from cuttings. Harvest leaves after 3-4 months.',
            'image_url': '/static/images/brahmi.jpg',
            'model_url': '/static/models/brahmi.glb'
        },
        {
            'name': 'Turmeric',
            'scientific_name': 'Curcuma longa',
            'category': 'Anti-inflammatory',
            'overview': 'Turmeric, the golden spice of India, has been used in Ayurvedic medicine for over 4,000 years. Its active compound curcumin is extensively researched for medicinal properties.',
            'medicinal_uses': 'Powerful anti-inflammatory, strong antioxidant, improves brain function, lowers risk of heart disease, helps prevent cancer, useful in treating Alzheimer\'s, helps with arthritis, and fights depression.',
            'cultivation': 'Grows in tropical regions with high rainfall. Requires temperatures of 20-30°C. Prefers well-drained, fertile soil rich in organic matter. Plant rhizomes 5 cm deep. Harvest after 7-10 months when leaves turn yellow.',
            'image_url': '/static/images/turmeric.jpg',
            'model_url': '/static/models/turmeric.glb'
        },
        {
            'name': 'Amla',
            'scientific_name': 'Phyllanthus emblica',
            'category': 'Vitamin C Source',
            'overview': 'Amla, or Indian Gooseberry, is one of the most important herbs in Ayurveda. It is extremely rich in Vitamin C and antioxidants.',
            'medicinal_uses': 'Rich source of Vitamin C, boosts immunity, improves digestion, enhances hair growth, improves eyesight, regulates blood sugar, supports heart health, and has anti-aging properties.',
            'cultivation': 'Deciduous tree that grows in tropical and subtropical regions. Prefers dry climate with temperatures 10-46°C. Grows in various soil types but prefers sandy loam. Drought-resistant once established. Fruits after 4-5 years.',
            'image_url': '/static/images/amla.jpg',
            'model_url': '/static/models/amla.glb'
        }
    ]
    
    for plant in plants_data:
        cursor.execute('''
            INSERT INTO plants (name, scientific_name, category, overview, medicinal_uses, cultivation, image_url, model_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (plant['name'], plant['scientific_name'], plant['category'], plant['overview'], 
              plant['medicinal_uses'], plant['cultivation'], plant['image_url'], plant['model_url']))
    
    products_data = [
        {'name': 'Ashwagandha Capsules', 'description': 'Pure Ashwagandha extract capsules for stress relief', 'price': 24.99, 'plant_id': 1, 'stock': 50, 'image_url': '/static/images/ashwagandha-capsules.jpg'},
        {'name': 'Ashwagandha Powder', 'description': 'Organic Ashwagandha root powder - 100g', 'price': 18.99, 'plant_id': 1, 'stock': 75, 'image_url': '/static/images/ashwagandha-powder.jpg'},
        {'name': 'Tulsi Tea', 'description': 'Organic Holy Basil tea for immunity - 50 bags', 'price': 12.99, 'plant_id': 2, 'stock': 100, 'image_url': '/static/images/tulsi-tea.jpg'},
        {'name': 'Tulsi Drops', 'description': 'Concentrated Tulsi extract drops', 'price': 15.99, 'plant_id': 2, 'stock': 60, 'image_url': '/static/images/tulsi-drops.jpg'},
        {'name': 'Neem Face Wash', 'description': 'Natural Neem face wash for clear skin', 'price': 9.99, 'plant_id': 3, 'stock': 80, 'image_url': '/static/images/neem-facewash.jpg'},
        {'name': 'Neem Capsules', 'description': 'Pure Neem leaf capsules for blood purification', 'price': 19.99, 'plant_id': 3, 'stock': 45, 'image_url': '/static/images/neem-capsules.jpg'},
        {'name': 'Brahmi Memory Tonic', 'description': 'Brahmi syrup for enhanced memory and focus', 'price': 22.99, 'plant_id': 4, 'stock': 40, 'image_url': '/static/images/brahmi-tonic.jpg'},
        {'name': 'Turmeric Powder', 'description': 'Organic turmeric powder - 200g', 'price': 8.99, 'plant_id': 5, 'stock': 120, 'image_url': '/static/images/turmeric-powder.jpg'},
        {'name': 'Curcumin Capsules', 'description': 'High-potency curcumin extract capsules', 'price': 29.99, 'plant_id': 5, 'stock': 55, 'image_url': '/static/images/curcumin-capsules.jpg'},
        {'name': 'Amla Juice', 'description': 'Pure Amla juice for immunity - 500ml', 'price': 14.99, 'plant_id': 6, 'stock': 70, 'image_url': '/static/images/amla-juice.jpg'},
        {'name': 'Amla Candy', 'description': 'Sweet and tangy Amla candy - 250g', 'price': 6.99, 'plant_id': 6, 'stock': 90, 'image_url': '/static/images/amla-candy.jpg'}
    ]
    
    for product in products_data:
        cursor.execute('''
            INSERT INTO products (name, description, price, plant_id, stock, image_url)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (product['name'], product['description'], product['price'], 
              product['plant_id'], product['stock'], product['image_url']))
    
    conn.commit()
    conn.close()
