from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from openai import OpenAI
import stripe
import json
from datetime import datetime
from database import init_db, get_db, seed_data

app = Flask(__name__)
app.secret_key = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')
CORS(app)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

openai_api_key = os.environ.get('OPENAI_API_KEY', '')
openai_client = OpenAI(api_key=openai_api_key) if openai_api_key else None
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY', '')

init_db()
seed_data()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/garden')
def garden():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM plants ORDER BY name')
    plants = cursor.fetchall()
    conn.close()
    return render_template('garden.html', plants=plants)

@app.route('/plant/<int:plant_id>')
def plant_detail(plant_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM plants WHERE id = ?', (plant_id,))
    plant = cursor.fetchone()
    conn.close()
    
    if plant:
        log_analytics('plant_view', {'plant_id': plant_id, 'plant_name': plant['name']})
        return render_template('plant_detail.html', plant=plant)
    return "Plant not found", 404

@app.route('/shop')
def shop():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT products.*, plants.name as plant_name 
        FROM products 
        LEFT JOIN plants ON products.plant_id = plants.id 
        ORDER BY products.name
    ''')
    products = cursor.fetchall()
    conn.close()
    return render_template('shop.html', products=products)

@app.route('/api/cart', methods=['POST'])
def update_cart():
    data = request.json or {}
    if 'cart' not in session:
        session['cart'] = []
    
    product_id = data.get('product_id')
    action = data.get('action', 'add')
    
    if action == 'add':
        session['cart'].append(product_id)
        session.modified = True
        return jsonify({'success': True, 'cart_count': len(session['cart'])})
    elif action == 'remove':
        if product_id in session['cart']:
            session['cart'].remove(product_id)
            session.modified = True
        return jsonify({'success': True, 'cart_count': len(session['cart'])})
    elif action == 'get':
        return jsonify({'cart': session.get('cart', []), 'cart_count': len(session.get('cart', []))})
    
    return jsonify({'success': False})

@app.route('/checkout')
def checkout():
    cart_items = session.get('cart', [])
    if not cart_items:
        return redirect(url_for('shop'))
    
    conn = get_db()
    cursor = conn.cursor()
    
    products = []
    total = 0
    for item_id in cart_items:
        cursor.execute('SELECT * FROM products WHERE id = ?', (item_id,))
        product = cursor.fetchone()
        if product:
            products.append(dict(product))
            total += product['price']
    
    conn.close()
    return render_template('checkout.html', products=products, total=total)

@app.route('/api/create-payment-intent', methods=['POST'])
def create_payment_intent():
    try:
        data = request.json or {}
        amount = int(float(data.get('amount', 0)) * 100)
        
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='usd',
            metadata={'customer_email': data.get('email', '')}
        )
        
        return jsonify({'clientSecret': intent.client_secret})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/complete-order', methods=['POST'])
def complete_order():
    try:
        data = request.json or {}
        cart_items = session.get('cart', [])
        
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO orders (customer_name, customer_email, total_amount, items, stripe_payment_id, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data.get('name', ''), data.get('email', ''), data.get('amount', 0), json.dumps(cart_items), 
              data.get('payment_id', ''), 'completed'))
        
        conn.commit()
        conn.close()
        
        session['cart'] = []
        session.modified = True
        
        log_analytics('order_completed', {'amount': data.get('amount', 0), 'items_count': len(cart_items)})
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json or {}
        user_message = data.get('message', '')
        
        if not openai_client:
            return jsonify({'response': 'AI chatbot is not configured. Please set the OPENAI_API_KEY environment variable.'})
        
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert in Ayurveda and AYUSH medicinal plants. Provide helpful, accurate information about medicinal plants, their uses, benefits, and traditional Ayurvedic practices. Be friendly and educational."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        bot_response = response.choices[0].message.content
        log_analytics('chatbot_query', {'query': user_message[:100]})
        
        return jsonify({'response': bot_response})
    except Exception as e:
        return jsonify({'response': f'Sorry, I encountered an error: {str(e)}'})

@app.route('/recognize')
def recognize():
    return render_template('recognize.html')

@app.route('/api/recognize-plant', methods=['POST'])
def recognize_plant():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        if not file.filename or file.filename == '':
            return jsonify({'error': 'No image selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        
        if not openai_client:
            return jsonify({'error': 'AI recognition is not configured. Please set the OPENAI_API_KEY environment variable.'}), 400
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        import base64
        with open(filepath, 'rb') as img_file:
            image_data = base64.b64encode(img_file.read()).decode('utf-8')
        
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Identify this medicinal plant. If it's a medicinal plant used in Ayurveda or traditional medicine, provide its common name, scientific name, and key medicinal uses. If you're not certain, make your best guess from common medicinal plants."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300
        )
        
        result = response.choices[0].message.content
        log_analytics('plant_recognition', {'filename': filename})
        
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': f'Recognition failed: {str(e)}'}), 400

@app.route('/community')
def community():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM community_submissions ORDER BY created_at DESC LIMIT 50')
    submissions = cursor.fetchall()
    conn.close()
    return render_template('community.html', submissions=submissions)

@app.route('/api/submit-plant', methods=['POST'])
def submit_plant():
    try:
        data = request.form
        image = request.files.get('image')
        
        image_path = None
        if image and image.filename and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO community_submissions 
            (plant_name, scientific_name, description, submitted_by, submitted_email, image_path, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (data.get('plant_name'), data.get('scientific_name'), data.get('description'),
              data.get('submitted_by'), data.get('submitted_email'), image_path, 'pending'))
        
        conn.commit()
        conn.close()
        
        log_analytics('community_submission', {'plant_name': data.get('plant_name')})
        
        return jsonify({'success': True, 'message': 'Your submission has been received and is pending approval.'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/admin')
def admin():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) as count FROM plants')
    plant_count = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM products')
    product_count = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM orders WHERE status = "completed"')
    order_count = cursor.fetchone()['count']
    
    cursor.execute('SELECT SUM(total_amount) as total FROM orders WHERE status = "completed"')
    revenue = cursor.fetchone()['total'] or 0
    
    cursor.execute('SELECT * FROM community_submissions WHERE status = "pending" ORDER BY created_at DESC')
    pending_submissions = cursor.fetchall()
    
    cursor.execute('SELECT * FROM orders ORDER BY created_at DESC LIMIT 10')
    recent_orders = cursor.fetchall()
    
    conn.close()
    
    return render_template('admin.html', 
                         plant_count=plant_count,
                         product_count=product_count,
                         order_count=order_count,
                         revenue=revenue,
                         pending_submissions=pending_submissions,
                         recent_orders=recent_orders)

@app.route('/api/admin/approve-submission/<int:submission_id>', methods=['POST'])
def approve_submission(submission_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('UPDATE community_submissions SET status = ? WHERE id = ?', ('approved', submission_id))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/admin/reject-submission/<int:submission_id>', methods=['POST'])
def reject_submission(submission_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('UPDATE community_submissions SET status = ? WHERE id = ?', ('rejected', submission_id))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/analytics')
def get_analytics():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT event_type, COUNT(*) as count 
        FROM analytics 
        GROUP BY event_type
    ''')
    event_stats = cursor.fetchall()
    
    cursor.execute('''
        SELECT DATE(created_at) as date, COUNT(*) as count 
        FROM analytics 
        GROUP BY DATE(created_at) 
        ORDER BY date DESC 
        LIMIT 30
    ''')
    daily_activity = cursor.fetchall()
    
    conn.close()
    
    return jsonify({
        'event_stats': [dict(row) for row in event_stats],
        'daily_activity': [dict(row) for row in daily_activity]
    })

def log_analytics(event_type, event_data):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO analytics (event_type, event_data) VALUES (?, ?)',
                      (event_type, json.dumps(event_data)))
        conn.commit()
        conn.close()
    except:
        pass

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
