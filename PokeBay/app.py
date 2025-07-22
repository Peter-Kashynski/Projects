from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_socketio import SocketIO, send, join_room, leave_room
import random 
from string import ascii_uppercase 
from datetime import datetime, timedelta
from forms import RegistrationForm, LoginForm, DeleteForm, LogoutForm
from flask_sqlalchemy import SQLAlchemy  
from sqlalchemy import or_, desc, func
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required 
from werkzeug.security import generate_password_hash, check_password_hash  
from flask_wtf.csrf import CSRFProtect 
from wtforms.validators import DataRequired, Email, ValidationError 
from collections import defaultdict 
from werkzeug.utils import secure_filename 
import os
from functions import format_timestamp 
from pytz import timezone 
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__) 
app.config["SECRET_KEY"] = 'glitter8831'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myDB.db' 
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Folder where images will be saved
app.config['ALLOWED_EXTENSIONS'] = {
    'png',    
    'jpg',   
    'jpeg',  
    'webp',   
    'bmp',  
    'tiff',  
    'tif',   
    'svg',    
    'ico',   
    'heic',   
    'heif',    
    'html',
}  

socketio = SocketIO(app)   

db = SQLAlchemy(app)  

login_manager = LoginManager()
login_manager.init_app(app) 
login_manager.login_view = 'login' # type: ignore
login_manager.login_message = "Please log in to access this page."  
csrf = CSRFProtect(app)

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(11), index=True, unique=True) 
  email = db.Column(db.String(120), index=True, unique=True) 
  password_hash = db.Column(db.String(128), index=True, unique=True)  
  joined_at = db.Column(db.DateTime(), index=True, default=datetime.utcnow)  
  shipping_address =  db.Column(db.String(128), index=True)
  timezone = db.Column(db.String(50), default='UTC')   

  def __repr__(self):
    return '<User {}>'.format(self.username)

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)   

class Expansions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expansion = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Expansion {self.expansion}>"

# using the market_item table 
class MarketItem(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False) 
    description = db.Column(db.String(1050), nullable=False)
    card_name = db.Column(db.String(100), nullable=False)
    card_number = db.Column(db.String(20), nullable=False)
    card_set = db.Column(db.String(100), nullable=False)
    image_filenames = db.Column(db.String(500), nullable=False)  
    username = db.Column(db.String(64), db.ForeignKey('user.username'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sold = db.Column(db.Boolean, default=False) 
    sold_at = db.Column(db.DateTime)  
    shipped = db.Column(db.Boolean, default=False)
    buyer_username = db.Column(db.String(64))
    
    user = db.relationship('User', backref='market_items')
    
    def __repr__(self):
        return f'<MarketItem {self.card_name} - {self.card_set}>' 
    
with app.app_context():
    db.create_all()   

#user loader 
@login_manager.user_loader
def load_user(user_id):  
    return User.query.get(int(user_id))  

# custom message for unloggedin users   
@login_manager.unauthorized_handler 
def unauthorized(): 
    return render_template('loginfail.html')

@app.route('/') 
def root(): 
    return redirect(url_for('login'))  

# login route
@app.route('/login', methods=['GET','POST'])
def login():    
  logout_user() 
  form = LoginForm() 
  user = None
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first() 
    if user and user.check_password(form.password.data):
        login_user(user, remember=form.remember.data)   
        return redirect(url_for('marketplace', current_user=user)) 
    else: 
        flash("Invalid username or password. Please try again.", "error")
  return render_template('login.html', form=form, current_user=user)  

@app.route('/logout', methods=['GET','POST'])
def logout():
    logout_user()
    return redirect(url_for('login')) 

@app.route('/register', methods=['GET','POST']) 
def register():   
    logout_user()
    form = RegistrationForm() 
    if form.validate_on_submit(): 
        existing_email = User.query.filter_by(email=form.email.data).first()  
        existing_username = User.query.filter_by(username=form.username.data).first()
        if existing_username: 
            flash(" Username taken, please choose a different one. ") 
            return render_template('register.html', form=form) 
        if existing_email:  
            flash(" Email already in use, please choose a different one. ") 
            return render_template('register.html', form=form)
        user = User(username=form.username.data, email=form.email.data) # type: ignore
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()  
        flash("Registration successful! You can now log in.", "register-success")
        return redirect(url_for('login'))  
    return render_template('register.html', form=form) 

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/your-listings/<username>') 
@login_required
def your_listings(username):  
    # blocking attempts to access other profiles 
    if current_user.username != username:
        flash("You can only view your own profile. Please use the marketplace to view other users' listings.", "profile_error")
        return redirect(url_for('marketplace')) 
        
    page = request.args.get('page', 1, type=int)
    per_page = 20 # can change amount of items shown on page 
    
    # Get total count of unsold items
    total_items = MarketItem.query.filter_by(username=username, sold=False).count()
    total_pages = (total_items + per_page - 1) // per_page  # Ceiling division
    
    # Get unsold items for current page
    pagination = MarketItem.query.filter_by(username=username, sold=False)\
        .order_by(MarketItem.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    your_items = pagination.items
    
    return render_template('your_listings.html',
                         username=username,
                         your_items=your_items,
                         page=page,
                         total_pages=total_pages)

@app.route('/sold-items/<username>') 
@login_required
def sold_items(username): 
    if current_user.username != username:
        flash("You can only view your own profile. Please use the marketplace to view other users' listings.", "profile_error")
        return redirect(url_for('marketplace')) 

    page = request.args.get('page', 1, type=int)
    per_page = 20  # can change amount of items shown on page
    
    # Get total count of sold items
    total_items = MarketItem.query.filter_by(username=username, sold=True).count()
    total_pages = (total_items + per_page - 1) // per_page  # Ceiling division
    
    # Get paginated sold items for the user
    pagination = MarketItem.query.filter_by(username=username, sold=True)\
        .order_by(MarketItem.shipped.asc(), MarketItem.sold_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    sold_items = pagination.items

    return render_template("sold_items.html", 
                         sold_items=sold_items,
                         page=page,
                         total_pages=total_pages,
                         username=username)

@app.route('/display-profile/<username>') 
@login_required
def display_profile(username):  
    page = request.args.get('page', 1, type=int)
    per_page = 20 # can change amount of items shown on page 
    
    # Get total count of items
    total_items = MarketItem.query.filter_by(username=username).count()
    total_pages = (total_items + per_page - 1) // per_page  # Ceiling division
    
    # Get items for current page
    pagination = MarketItem.query.filter_by(username=username)\
        .order_by(MarketItem.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    user_items = pagination.items
    
    return render_template('display_profile.html',
                         username=username,
                         user_items=user_items,
                         page=page,
                         total_pages=total_pages)

@app.route('/create-listing', methods=["GET", "POST"])
@login_required
def create_listing():
    if request.method == "POST":
        item = str(request.form.get("itemtitle"))
        price = request.form.get("itemprice")   
        description = request.form.get("itemdescription")
        card_name = str(request.form.get("cardname"))
        card_number = str(request.form.get("cardnumber"))
        card_set = str(request.form.get("selected_expansion"))
        username = current_user.username
        image_filenames = []

        if 'itempictures' in request.files:
            files = request.files.getlist('itempictures')
            for file in files:
                if file:
                    if not allowed_file(file.filename):
                        flash(f"File type not allowed. Please upload only: {', '.join(app.config['ALLOWED_EXTENSIONS'])}", "listing_error")
                        return render_template("create_listing/create_listing.html")
                    
                    if not os.path.exists(app.config['UPLOAD_FOLDER']):
                        os.makedirs(app.config['UPLOAD_FOLDER'])

                    # Generate a unique filename to avoid conflicts
                    filename = str(file.filename)
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                    unique_filename = timestamp + filename
                    
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                    file.save(file_path)
                    image_filenames.append(unique_filename)
    
        if not item or not price or not image_filenames or not card_name or not card_number or not card_set:
            flash("All fields are required", "listing_error")
            return render_template("create_listing/create_listing.html")

        try: 
            utc_time = datetime.utcnow()
            formatted_time = utc_time.strftime('%Y-%m-%d %H:%M')  # Format directly to match item_page format
            utc_time_object = datetime.strptime(formatted_time, '%Y-%m-%d %H:%M') 

            # Create new market item
            new_item = MarketItem(**{
                'item': item,
                'price': price, 
                'description': description,
                'card_name': card_name,
                'card_number': card_number,
                'card_set': card_set,
                'image_filenames': ','.join(image_filenames),
                'username': username, 
                'created_at': utc_time_object,
            })
                        

            # Add and commit to database
            db.session.add(new_item)
            db.session.commit()
            flash("Item listed successfully!", "listing_success")
        except Exception as e:
            db.session.rollback()
            flash("Error creating listing. Please try again.", "listing_error")
            print(f"Error: {e}")

        return redirect(url_for('marketplace', current_item=new_item))

    return render_template("create_listing/create_listing.html")

@app.route('/search-expansions') 
def search_expansions():  
    q = request.args.get("q")
    print(q)

    if q: 
        results = Expansions.query.filter(Expansions.expansion.icontains(q)).limit(10).all() # or startswith
    else: 
        results = []

    return render_template("create_listing/expansion_search_results.html", results=results) 

import stripe 
app.config["STRIPE-PK"] = os.environ.get('STRIPE_PK')
app.config["STRIPE-SK"] = os.environ.get('STRIPE_SK')
stripe.api_key = app.config["STRIPE-SK"] # this is used and implicitly called 
# when we make a session like below  
@app.route('/marketplace/item/<int:item_id>', methods=['GET'])
@login_required
def item_page(item_id): 
    # Get the item from database using ID
    item = MarketItem.query.get_or_404(item_id)
    
    # Get the seller's user object to compare IDs
    seller = User.query.filter_by(username=item.username).first()
    is_seller = current_user.is_authenticated and seller and current_user.id == seller.id

    # Convert UTC time to EST
    if item.created_at:
        local_time = item.created_at.replace(tzinfo=timezone('UTC')).astimezone(timezone('America/New_York'))
        formatted_time = local_time.strftime('%Y-%m-%d %I:%M %p')
    else:
        formatted_time = None

    # Format sold_at time if item is sold
    sold_at_formatted = None
    ship_by_formatted = None
    if item.sold_at:
        sold_at_local = item.sold_at.replace(tzinfo=timezone('UTC')).astimezone(timezone('America/New_York'))
        sold_at_formatted = sold_at_local.strftime('%Y-%m-%d %I:%M %p')
        
        # Calculate ship by date (3 days after sold date)
        ship_by_date = sold_at_local + timedelta(days=3)
        ship_by_formatted = ship_by_date.strftime('%Y-%m-%d %I:%M %p')

    # Get buyer information if item is sold
    buyer_shipping_address = None
    if item.sold:
        buyer = User.query.filter_by(username=item.buyer_username).first()
        if buyer:
            buyer_shipping_address = buyer.shipping_address

    item_data = { 
        "item_id": item.id,
        "item": item.item,
        "price": item.price, 
        "description": item.description,
        "image_filenames": item.image_filenames.split(','),
        "card_name": item.card_name,
        "card_number": item.card_number,
        "card_set": item.card_set,
        "username": item.username,
        "created_at": formatted_time,
        "is_seller": is_seller,
        "sold": item.sold,
        "shipped": item.shipped,
        "buyer_shipping_address": buyer_shipping_address,
        "sold_at": sold_at_formatted,
        "ship_by": ship_by_formatted
    }  

    try:
        # First get similar items
        similar_items = (MarketItem.query
                        .filter(or_(
                            MarketItem.card_name.ilike(f'%{item.card_name}%'),  # Similar name
                            MarketItem.card_set == item.card_set  # Same set
                        ))
                        .filter(MarketItem.id != item.id)  # Exclude current item
                        .order_by(
                            desc(MarketItem.card_name == item.card_name),  # Exact matches first
                            desc(MarketItem.card_set == item.card_set)     # Same set second
                        )
                        .limit(8)
                        .all())

        # If we have less than 8 items, add random items
        if len(similar_items) < 8:
            items_needed = 8 - len(similar_items)
            random_items = (MarketItem.query
                           .filter(MarketItem.id != item.id)
                           .filter(~MarketItem.id.in_([item.id for item in similar_items]))
                           .order_by(func.random())
                           .limit(items_needed)
                           .all())
            similar_items.extend(random_items)

        # Random items you might like
        items_you_might_like = (MarketItem.query
                           .filter(MarketItem.id != item.id)
                           .filter(~MarketItem.id.in_([item.id for item in similar_items]))
                           .order_by(func.random())
                           .limit(8)
                           .all())

        return render_template('item_page.html', 
                             similar_items=similar_items, 
                             item_data=item_data, 
                             items_you_might_like=items_you_might_like)

    except Exception as e:
        print(f"Error in item_page: {str(e)}")
        similar_items = []
        return render_template('item_page.html', 
                             similar_items=similar_items, 
                             item_data=item_data)

@app.route('/purchase-item', methods=['POST'])
@login_required
def purchase_item():
    try:
        # Check if user has a shipping address
        if not (current_user.shipping_address and current_user.shipping_address.strip()):
            flash("Please add a valid shipping address before making a purchase.", "error")
            return redirect(url_for('shipping_address'))

        # Get form data
        item_name = request.form.get('item_name')
        item_price = float(request.form.get('item_price', 0)) * 100  # Convert to cents
        card_name = request.form.get('card_name')
        card_set = request.form.get('card_set')
        seller = request.form.get('seller')
        item_id = request.form.get('item_id')  # Get the item_id from the form

        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': f"{item_name} - {card_set}",
                        'description': f"Seller: {seller}",
                    },
                    'unit_amount': int(item_price),  # Must be an integer
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=url_for('purchase_success', item_id=item_id, _external=True),
            cancel_url=url_for('item_page', item_id=item_id, _external=True),
        )
        if session.url:
            return redirect(session.url, code=303)
        return "Error: No checkout URL generated", 500
    except Exception as e:
        return str(e), 500

@app.route('/purchase-success/<int:item_id>')
@login_required
def purchase_success(item_id):
    try:
        # Get the item
        item = MarketItem.query.get_or_404(item_id)
        
        # Update the item as sold and set buyer username
        item.sold = True
        item.sold_at = datetime.utcnow()
        item.buyer_username = current_user.username
        
        # Commit the changes
        db.session.commit()
        
        flash("Thank you for your purchase! The Seller has been contacted.", "success")
        return redirect(url_for('marketplace'))
    except Exception as e:
        flash("There was an error processing your purchase. Please contact support.", "error")
        return redirect(url_for('marketplace'))

@app.route('/marketplace/item/<int:item_id>/edit-listing', methods=['POST'])
@login_required 
def edit_listing(item_id): 
    item = MarketItem.query.get_or_404(item_id)  

    if item.created_at:
        local_time = item.created_at.replace(tzinfo=timezone('UTC')).astimezone(timezone('America/New_York'))
        formatted_time = local_time.strftime('%Y-%m-%d %I:%M %p')
    else:
        formatted_time = None 

    item_data = { 
        "item_id": item.id,
        "item": item.item,
        "price": item.price, 
        "description": item.description,
        "image_filenames": item.image_filenames.split(','),
        "card_name": item.card_name,
        "card_number": item.card_number,
        "card_set": item.card_set,
        "username": item.username,
        "created_at": formatted_time,
    }
    return render_template('edit_listing.html', item_data=item_data) 

@app.route('/marketplace/item/<int:item_id>/update', methods=['POST'])
@login_required
def update_listing(item_id):
    item = MarketItem.query.get_or_404(item_id)
    
    # Check if the current user is the owner of the listing
    if current_user.username != item.username:
        flash("You can only edit your own listings.", "error")
        return redirect(url_for('marketplace'))

    try:
        # Get form data
        item.item = request.form.get("itemtitle", "")
        price_str = request.form.get("itemprice")
        if price_str is not None:
            item.price = float(price_str)
        item.description = request.form.get("itemdescription", "")
        item.card_name = request.form.get("cardname", "")
        item.card_number = request.form.get("cardnumber", "")
        item.card_set = request.form.get("selected_expansion", "")

        # Handle new images if uploaded
        if 'itempictures' in request.files:
            files = request.files.getlist('itempictures')
            if files and files[0].filename:  # Check if any files were uploaded
                # Get existing image filenames
                existing_filenames = item.image_filenames.split(',') if item.image_filenames else []
                new_image_filenames = []
                
                for file in files:
                    if file and file.filename and allowed_file(file.filename):
                        # Generate a unique filename
                        filename = secure_filename(file.filename)
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                        unique_filename = timestamp + filename
                        
                        # Save the file
                        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                        file.save(file_path)
                        new_image_filenames.append(unique_filename)
                
                if new_image_filenames:  # Only update if new images were uploaded
                    # Combine existing and new filenames
                    all_filenames = existing_filenames + new_image_filenames
                    item.image_filenames = ','.join(all_filenames)

        # Update the database
        db.session.commit()
        flash("Listing updated successfully!", "listing_success")
        return redirect(url_for('item_page', item_id=item.id))

    except Exception as e:
        db.session.rollback()
        flash("Error updating listing. Please try again.", "listing_error")
        print(f"Error: {e}")
        return redirect(url_for('edit_listing', item_id=item.id))

@app.route('/marketplace/item/<int:item_id>/delete', methods=['POST'])
@login_required
def delete_item(item_id):
    item = MarketItem.query.get_or_404(item_id)
    
    # Check if the current user is the owner of the listing
    if current_user.username != item.username:
        flash("You can only delete your own listings.", "listing_error")
        return redirect(url_for('marketplace'))

    try:
        # Delete the item from the database
        db.session.delete(item)
        db.session.commit()
        flash("Item deleted successfully!", "listing_success")
    except Exception as e:
        db.session.rollback()
        flash("Error deleting item. Please try again.", "listing_error")
        print(f"Error: {e}")
    
    return redirect(url_for('marketplace'))

@app.route('/marketplace/item/<int:item_id>/mark-shipped', methods=['POST'])
@login_required
def mark_as_shipped(item_id):
    item = MarketItem.query.get_or_404(item_id)
    
    # Check if the current user is the owner of the listing
    if current_user.username != item.username:
        flash("You can only mark your own items as shipped.", "error")
        return redirect(url_for('marketplace'))

    try:
        item.shipped = True
        db.session.commit()
        flash("Item marked as shipped successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash("Error marking item as shipped. Please try again.", "error")
        print(f"Error: {e}")
    
    return redirect(url_for('item_page', item_id=item.id))

market_items = []
@app.route('/marketplace', methods=["GET"]) 
@login_required
def marketplace():
    username = current_user.username if current_user.is_authenticated else None
    
    # Check for purchase success
    if request.args.get('purchase_success'):
        flash("Thank you for your purchase! Your order has been confirmed.", "success")
    
    if username:
        your_items = MarketItem.query.filter_by(username=username, sold=False).all()
        other_items = MarketItem.query.filter(MarketItem.username != username, MarketItem.sold == False).all()
    else:
        your_items = []
        other_items = MarketItem.query.all()

    # Sort other items by card set
    other_items.sort(key=lambda x: x.card_set)

    return render_template('marketplace.html', 
                         your_items=your_items, 
                         other_items=other_items, 
                         username=username)

@app.route('/search') 
@login_required
def search():
    query = request.args.get('query', '')
    if not query:
        flash('Please enter a search term', 'error')
        return redirect(url_for('marketplace'))

    # Search the database for matching cards
    results = MarketItem.query.filter(
        db.or_(
            MarketItem.card_name.ilike(f'%{query}%'),
            MarketItem.item.ilike(f'%{query}%')
        )
    ).order_by(
        # Order by similarity to search query
        db.case(
            (MarketItem.card_name.ilike(f'{query}%'), 1),  # Exact start match
            (MarketItem.card_name.ilike(f'%{query}%'), 2),  # Contains match
            else_=3
        )
    ).limit(50).all() 

    you_may_like = []
    if len(results) == 0: 
        you_may_like_results = (MarketItem.query.order_by(func.random()).limit(8).all()) 
        you_may_like.extend(you_may_like_results)

    return render_template('search_results.html', results=results, you_may_like=you_may_like, query=query)

@app.route('/shipping-address', methods=['GET', 'POST'])
@login_required
def shipping_address():
    if request.method == 'POST':
        address = request.form.get('address')
        if address:
            current_user.shipping_address = address
            db.session.commit()
            flash('Shipping address added successfully!', 'success')
            return redirect(url_for('marketplace'))
        else:
            flash('Please enter a valid address', 'error')
    
    return render_template('shipping_address.html')

if __name__ == "__main__":   
    socketio.run(app, debug=True) 
