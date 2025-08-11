from flask import Flask, render_template, redirect, url_for, flash, session, abort, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegistrationForm, PaymentForm, ContactForm
from models import db, User, Order, OrderItem ,ContactMessage
from flask_wtf.csrf import CSRFProtect
from datetime import timedelta, datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///badyproduct.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from data.pamper import get_pamper_products
from data.Soap import get_scop_products
from data.Stroller import get_stroller_products
from data.Bottle import get_bottle_products
from data.GirlsFashion import get_girls_fashion_products
from data.BoysFashion import get_boys_fashion_products
from data.product_utils import filter_products
from data.Offers import get_offer_products

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        flash('Login failed. Check your email and/or password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(name=form.name.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/home')
@login_required
def home():
    products = get_best_sellers()
    items_per_slide = 3
    slides = [products[i:i + items_per_slide] for i in range(0, len(products), items_per_slide)]
    total_slides = len(slides)

    try:
        current_index = int(request.args.get('slide', 0))
    except (ValueError, TypeError):
        current_index = 0
    current_index = max(0, min(current_index, total_slides - 1))

    return render_template('home.html',
                           slides=slides,
                           current_index=current_index,
                           total_slides=total_slides,
                           faqs=FAQS)


def get_best_sellers():
    return [
        {"id": 1, "title": "Wipes", "image": "Img-card-col.png", "rating": 5, "mrp": 1444, "price": 1299},
        {"id": 2, "title": "Mama Miel Baby", "image": "Frame 1171275003.png", "rating": 5, "mrp": 1444, "price": 1299},
        {"id": 3, "title": "Zibuyu", "image": "Frame 1171275013.png", "rating": 5, "mrp": 1444, "price": 1299},
        {"id": 4, "title": "Wipes", "image": "Img-card-col.png", "rating": 5, "mrp": 1444, "price": 1299},
        {"id": 5, "title": "Mama Miel Baby", "image": "Frame 1171275003.png", "rating": 5, "mrp": 1444, "price": 1299},
        {"id": 6, "title": "Zibuyu", "image": "Frame 1171275013.png", "rating": 5, "mrp": 1444, "price": 1299},
    ]

@app.route('/best-sellers')
def best_sellers():
    products = get_best_sellers() 
    items_per_slide = 3
    
    slides = [products[i:i + items_per_slide] for i in range(0, len(products), items_per_slide)]
    total_slides = len(slides)
    
    try:
        current_index = int(request.args.get('slide', 0))
    except ValueError:
        current_index = 0
    current_index = max(0, min(current_index, total_slides - 1))
    
    return render_template(
        'best_sellers.html',
        slides=slides,
        current_index=current_index,
        total_slides=total_slides
    )

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        try:
            message = ContactMessage(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                phone=form.phone.data,
                subject=form.subject.data,
                message=form.message.data
            )
            db.session.add(message)
            db.session.commit()
            flash('Message sent successfully!', 'success')
            return redirect(url_for('contact'))
        except Exception as e:
            db.session.rollback()
            flash('Error sending message. Please try again.', 'danger')
            app.logger.error(f"Error saving contact message: {str(e)}")
    
    return render_template('contact.html', form=form)

@app.route('/about')
def about():
    return render_template('about.html')


def collect_filter_states():
    """
    Gathers the current filter values from query parameters.
    Returns a dict like {'min_price': 100, 'max_price': 1000, ...}.
    """
    return {
        'min_price': request.args.get('min_price', type=int),
        'max_price': request.args.get('max_price', type=int),
        'free_shipping': is_free_shipping_selected(),
        'discounts': is_discounts_selected()
    }
def is_free_shipping_selected():
    return request.args.get('free_shipping') == 'true'

def is_discounts_selected():
    return request.args.get('discounts') == 'true'
CATEGORY_DATA = {
    'pampers': {
        'name': "Pampers",
        'get_products': get_pamper_products,
        'template': 'products/pampers.html'
    },
    'boys_fashion': {
        'name': "Boy's Fashion",
        'get_products': get_boys_fashion_products,
        'template': 'products/boys_fashion.html'
    },
    'girls_fashion': {
        'name': "Girl's Fashion",
        'get_products': get_girls_fashion_products,
        'template': 'products/girls_fashion.html'
    },
    'scop': {
        'name': "Scop",
        'get_products': get_scop_products,
        'template': 'products/scop.html'
    },
    'stroller': {
        'name': "Stroller",
        'get_products': get_stroller_products,
        'template': 'products/stroller.html'
    },
    'bottle': {
        'name': "Bottle",
        'get_products': get_bottle_products,
        'template': 'products/bottle.html'
    }

}

@app.route('/offers')
def offers():
    filters = collect_filter_states()
    
    products = filter_products(
        get_offer_products(),
        price_filter=(filters['min_price'], filters['max_price']) 
            if filters['min_price'] is not None and filters['max_price'] is not None 
            else None,
        free_shipping=filters['free_shipping'],
        discounts=filters['discounts']
    )

    breadcrumbs = [
        {'name': 'Home', 'url': url_for('home')},
        {'name': 'Offers', 'url': None}
    ]

    return render_template(
        'offers.html',
        category_name="Special Offers",
        products=products,
        breadcrumbs=breadcrumbs,
        current_filters=filters,
        filters=[
            "Price(100-1000)",
            "Price(1000-1500)",
            "Price(1500-10000)",
            "Free Shipping",
            "Discounts"
        ],
        selected_filter=request.args.get('filter')
    )

@app.route('/products')
def products():
    return redirect(url_for('products_category', category='pampers'))

@app.route('/products/<category>')
def products_category(category):
    info = CATEGORY_DATA.get(category)
    if not info:
        abort(404)

    filters = collect_filter_states()
    
    products = filter_products(
        info['get_products'](),
        price_filter=(filters['min_price'], filters['max_price']) 
            if filters['min_price'] is not None and filters['max_price'] is not None 
            else None,
        free_shipping=filters['free_shipping'],
        discounts=filters['discounts']
    )

    breadcrumbs = [
        {'name': 'Home', 'url': url_for('home')},
        {'name': 'Products', 'url': url_for('products')},
        {'name': info['name'], 'url': None}
    ]

    return render_template(
        info['template'],
        category_name=info['name'],
        products=products,
        breadcrumbs=breadcrumbs,
        current_filters=filters,
        filters=[
            "Price(100-1000)",
            "Price(1000-1500)",
            "Price(1500-10000)",
            "Free Shipping",
            "Discounts"
        ],
        selected_filter=request.args.get('filter')
    )

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


FAQS = [
        {'question': 'Are your products safe for newborns?', 'answer': 'Yes, all our products are dermatologically tested and made with gentle, non-toxic ingredients that are safe for newborns and sensitive skin.'},
        {'question': 'How long does delivery take?', 'answer': 'Delivery typically takes 3-5 business days depending on your location. You\'ll receive tracking details once your order is shipped.'},
        {'question': 'Can I return or exchange a product?', 'answer': 'Yes, we offer a 7-day return or exchange policy on unused and unopened items. Please contact our support team to initiate a return.'},
        {'question': 'What payment methods do you accept?', 'answer': 'We accept all major credit/debit cards, UPI, net banking, and wallet payments like Paytm and Google Pay.'},
        {'question': 'Are your skincare products organic or natural?', 'answer': 'Yes, our skincare range is made using organic and naturally derived ingredients, free from harmful chemicals and artificial fragrances.'}
    ]

@app.route('/faq')
def faq():
   return render_template('faq.html', faqs=FAQS)

@app.template_filter('format_currency')
def format_currency(value):
    return "₹{:,.2f}".format(value)


@app.route('/checkout/<int:product_id>', methods=['GET', 'POST'])
@login_required
def checkout(product_id):
    try:
        all_products = []
        all_products.extend(get_pamper_products()) 
        all_products.extend(get_boys_fashion_products()) 
        all_products.extend(get_girls_fashion_products())
        all_products.extend(get_scop_products())
        all_products.extend(get_stroller_products())
        all_products.extend(get_bottle_products())
        all_products.extend(get_offer_products())

        print(f"\nTotal products loaded: {len(all_products)}")
        print("Sample products:")
        for p in all_products[:3]:
            print(f"ID: {p['id']}, Title: {p['title']}, Price: {p['price']}")

        product = next((p for p in all_products if p['id'] == product_id), None)
        
        if not product:
            available_ids = [p['id'] for p in all_products]
            print(f"\nERROR: Product {product_id} not found. Available IDs: {available_ids}")
            flash(f'Product ID {product_id} not available', 'danger')
            return redirect(url_for('products'))

        if request.method == 'POST':
            quantity = int(request.form.get('quantity', 1))
            address = request.form.get('address', '').strip()
            payment_method = request.form.get('payment_method', '').strip()

            if not address or not payment_method:
                flash('Please fill all required fields', 'danger')
            else:
                order_total = product['price'] * quantity
                flash(f'Order successful! Total: ₹{order_total}', 'success')
                return redirect(url_for('order_confirmation', product_id=product_id))
        breadcrumbs = [
            {'name': 'Home', 'url': url_for('home')},
            {'name': 'Products', 'url': url_for('products')},
            {'name': 'Checkout', 'url': None}
        ]

        return render_template('checkout.html', 
                            product=product, 
                            breadcrumbs=breadcrumbs)

    except Exception as e:
        print(f"\nCRITICAL ERROR IN CHECKOUT: {str(e)}")
        flash('An unexpected error occurred. Please try again.', 'danger')
        return redirect(url_for('home'))
    

@app.route('/update-quantity/<int:product_id>', methods=['POST'])
def update_quantity(product_id):
    try:
        new_quantity = int(request.form['quantity'])
        if new_quantity < 1:
            flash('Quantity must be at least 1', 'warning')
            return redirect(url_for('cart'))
            
        for item in session['cart']:
            if item['id'] == product_id:
                item['quantity'] = new_quantity
                break
                
        session.modified = True
        flash('Quantity updated', 'success')
    except ValueError:
        flash('Invalid quantity', 'danger')
    
    return redirect(url_for('cart'))

@app.route('/order-complete')
def order_complete():
    import random
    order_id = f"OCD{random.randint(1000, 9999)}"
    
    return render_template('order_complete.html', 
                         order_id=order_id)

@app.route('/reset-db')
def reset_db():
    db.drop_all()
    db.create_all()
    return "Database tables recreated"


@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if 'cart' not in session or not session['cart']:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('cart'))
    
    cart_items = session.get('cart', [])
    subtotal = sum(item['price'] * item['quantity'] for item in cart_items)
    discount = subtotal * session.get('coupon', {}).get('discount', 0)
    total = subtotal - discount
    
    form = PaymentForm(request.form)
    
    if request.method == 'POST' and form.validate():
        order = Order(
            first_name=form.first_name.data,
            email=form.email.data,
            phone=form.phone.data,
            company_name=form.company_name.data,
            street_address=form.street_address.data,
            apartment=form.apartment.data,
            city=form.city.data,
            subtotal=subtotal,
            discount=discount,
            total=total,
            payment_method=form.payment_method.data,
            status='pending'
        )
        
        db.session.add(order)
        db.session.commit()  

        for item in cart_items:
            order.items.append(OrderItem(
                order_id=order.id, 
                product_id=item['id'],
                quantity=item['quantity'],
                price=item['price']
            ))
            db.session.add(order)
        
        db.session.commit() 

        session.pop('cart', None)
        session.pop('coupon', None)
        
        flash('Order placed successfully!', 'success')
        return redirect(url_for('order_complete', order_id=order.id))
    
    return render_template('payment.html',
                        form=form,
                        cart_items=cart_items,
                        subtotal=subtotal,
                        discount=discount,
                        total=total)

COUPONS = {
    'WELCOME10': 0.10, 
    'FREESHIP': 0.05 
}

@app.before_request
def initialize_cart():
    if 'cart' not in session:
        session['cart'] = []

@app.context_processor
def inject_cart_count():
    cart_count = 0
    if 'cart' in session and isinstance(session['cart'], list):
        cart_count = sum(item.get('quantity', 0) for item in session['cart'])
    return dict(cart_count=cart_count)

@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    if 'cart' not in session:
        session['cart'] = []
    
    try:
        product_id = int(request.form['product_id'])
        product = find_product_by_id(product_id)
        
        if not product:
            flash('Product not found', 'danger')
            return redirect(url_for('products'))
        
        quantity = int(request.form.get('quantity', 1))
        
        cart = session['cart']
        existing_item = next((item for item in cart if item['id'] == product_id), None)
        
        if existing_item:
            existing_item['quantity'] += quantity
        else:
            cart.append({
                'id': product_id,
                'title': product['title'],
                'price': float(product['price']),
                'image': product['images'][0],
                'quantity': quantity
            })
        
        session.modified = True
        flash(f'{product["title"]} added to cart!', 'success')
        return redirect(url_for('cart'))
        
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('home'))
    
@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if 'cart' not in session:
        session['cart'] = []
  
    if request.method == 'POST' and 'coupon_code' in request.form:
        coupon_code = request.form['coupon_code'].strip().upper()
        if coupon_code in COUPONS:
            session['coupon'] = {
                'code': coupon_code,
                'discount': COUPONS[coupon_code],
                'applied_at': datetime.utcnow()
            }
            flash('Coupon applied successfully!', 'success')
        else:
            flash('Invalid coupon code', 'danger')
        return redirect(url_for('cart'))

    cart_items = session.get('cart', [])
    subtotal = sum(item['price'] * item['quantity'] for item in cart_items)
    discount = calculate_discount(subtotal)
    total = max(0, subtotal - discount) 
    
    return render_template('cart.html',
                         cart_items=cart_items,
                         subtotal=subtotal,
                         discount=discount,
                         total=total,
                         coupon=session.get('coupon'))

@app.route('/remove-from-cart/<int:product_id>')
def remove_from_cart(product_id):
    if 'cart' in session:
        session['cart'] = [item for item in session['cart'] if item['id'] != product_id]
        session.modified = True
        flash('Item removed from cart', 'info')
    return redirect(url_for('cart'))

def calculate_discount(subtotal):
    if 'coupon' not in session:
        return 0
    
    coupon = session['coupon']
    if 'applied_at' in coupon:
        expiry_time = coupon['applied_at'] + timedelta(hours=24)
        if datetime.utcnow() > expiry_time:
            session.pop('coupon', None)
            return 0
    
    return round(subtotal * float(coupon.get('discount', 0)), 2)

def find_product_by_id(product_id):
    """Search for product across all categories"""
    product_id = int(product_id)  

    product_fetchers = [
        get_pamper_products,
        get_scop_products,
        get_stroller_products,
        get_bottle_products,
        get_girls_fashion_products,
        get_boys_fashion_products,
        get_offer_products
    ]

    for fetcher in product_fetchers:
        for product in fetcher():
            if product.get('id') == product_id:
                product.setdefault('images', ['default-product.png'])
                product.setdefault('title', 'Unknown Product')
                return product
                
    return None  

@app.route('/search')
def search():
    query = request.args.get('q', '').strip().lower()
    
    if not query:
        return redirect(url_for('home'))

    all_products = (
        get_pamper_products() +
        get_scop_products() +
        get_stroller_products() +
        get_bottle_products() +
        get_girls_fashion_products() +
        get_boys_fashion_products() +
        get_offer_products()
    )
     
    results = []
    for product in all_products:
        if query in product['title'].lower():
            results.append(product)
    
    return render_template(
        'search_results.html',
        query=query,
        results=results,
        results_count=len(results)
    )

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
