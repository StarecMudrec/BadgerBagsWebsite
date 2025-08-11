import os
from werkzeug.utils import secure_filename
import hmac
from hashlib import sha256
import uuid  # For generating unique tokens
import time  # Add this line with the other imports
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify, send_from_directory, session
from flask_migrate import Migrate
import requests  # Import the requests library
# import jwt
from joserfc.errors import JoseError
import logging
from flask_sqlalchemy import SQLAlchemy  # Database integration
from models import db, AuthToken, Item, AllowedUser, AdminToken, ItemImage
from config import Config
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(2)  # Background threads for file ops

app = Flask(__name__)
app.config.from_object(Config)

UPLOAD_FOLDER = os.path.join('/app', 'frontend', 'public', 'bags_imgs')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure logging
logging.basicConfig(level=logging.DEBUG)

db.init_app(app)

migrate = Migrate(app, db)

# Create the database tables
with app.app_context():
    db.create_all()


def validate_admin_token(user_id, token):
    """Check if the admin token is valid and unused"""
    try:
        token_record = AdminToken.query.filter_by(
            telegram_id=user_id,
            token=token,
            is_used=False
        ).first()
        
        if not token_record:
            logging.warning(f"Token not found or already used: {token}")
            return False
            
        if datetime.utcnow() > token_record.expires_at:
            logging.warning(f"Expired token used: {token}")
            return False
            
        # Mark token as used
        token_record.is_used = True
        db.session.commit()
        return True
        
    except Exception as e:
        logging.error(f"Token validation error: {e}")
        db.session.rollback()
        return False

def create_admin_token(user_id, expires_minutes=5):
    """Generate a new admin token (for bot use)"""
    try:
        # First expire any existing tokens
        AdminToken.query.filter_by(telegram_id=user_id).update({'is_used': True})
        
        # Create new token
        new_token = AdminToken(
            telegram_id=user_id,
            token=str(uuid.uuid4()),
            expires_at=datetime.utcnow() + timedelta(minutes=expires_minutes)
        )
        db.session.add(new_token)
        db.session.commit()
        return new_token.token
    except Exception as e:
        logging.error(f"Token creation error: {e}")
        db.session.rollback()
        return None

# Authentication Helper Function
def is_authenticated(request, session):
    token = request.args.get("token") or request.cookies.get("token")
    if not token:
        return False, None

    try:
        auth_token = AuthToken.query.filter_by(token=token).first()
        if not auth_token:
            return False, None

        session['user_id'] = auth_token.user_id
        session['is_admin'] = getattr(auth_token, 'is_admin', False)
        
        return True, auth_token.user_id
    except Exception as e:
        logging.exception(f"Auth error: {e}")
        return False, None


# Function to download avatar image
def download_avatar(url, user_id):
    if not url:
        return None
    avatar_dir = 'backend/avatars'
    os.makedirs(avatar_dir, exist_ok=True)
    filename = os.path.join(avatar_dir, f"{user_id}.jpg")  # Assuming avatars are JPEGs, adjust if needed
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return filename
    except requests.exceptions.RequestException as e:
        logging.error(f"Error downloading avatar from {url}: {e}")
        return None

# Telegram OAuth Callback Route
@app.route('/auth/telegram-callback')
def telegram_callback():
    try:
        # Verify required parameters
        required_params = ['id', 'auth_date', 'hash', 'admin_token']
        if not all(p in request.args for p in required_params):
            return "Missing required parameters", 400

        params = request.args.to_dict()
        
        # Verify auth_date is recent (within 5 minutes)
        auth_date = int(params['auth_date'])
        if abs(time.time() - auth_date) > 300:  # 5 minutes
            return "Authentication expired", 401

        # Reconstruct data_check_string
        data_check_string = "\n".join(
            f"{k}={v}" for k, v in sorted(params.items()) if k != 'hash'
        )
        
        # Generate validation hash
        secret_key = hmac.new(
            bytes(Config.BOT_TOKEN, 'utf-8'),
            msg=b"WebAppData",
            digestmod=sha256
        ).digest()
        
        computed_hash = hmac.new(
            secret_key,
            data_check_string.encode(),
            sha256
        ).hexdigest()

        # Verify hash
        if not hmac.compare_digest(computed_hash, params['hash']):
            app.logger.error(f"Hash mismatch: {params['hash']} vs {computed_hash}")
            return "Invalid Telegram authentication", 401

        # Validate admin token
        if not validate_admin_token(params['id'], params['admin_token']):
            return "Invalid or expired admin token", 403

        # Create session
        session.update({
            'telegram_id': params['id'],
            'is_admin': True,
            'user_data': {
                'first_name': params.get('first_name'),
                'last_name': params.get('last_name'),
                'username': params.get('username')
            }
        })

        return redirect(url_for('home'))

    except Exception as e:
        app.logger.error(f"Callback error: {str(e)}")
        return "Authentication failed", 500

@app.route('/telegram-webhook', methods=['POST'])
def telegram_webhook():
    if request.method == 'POST':
        update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
        bot.process_new_updates([update])
    return 'OK', 200

# Logout Route (Clears the Token)
@app.route("/auth/logout", methods=['GET', 'POST'])
def logout():
    token = request.cookies.get("token")

    if token:
        try:
            auth_token = AuthToken.query.filter_by(token=token).first()
            if auth_token:
                db.session.delete(auth_token)
                db.session.commit()
                logging.debug(f"Deleted token {token} from database")

        except Exception as e:
            db.session.rollback()
            logging.exception(f"Database error deleting token: {e}")
            return "Database error", 500

    session.clear() # Clear the user's session data
    response = make_response(jsonify({'status': 'logged_out'}))
    response.delete_cookie("token")
    return response

@app.after_request
def add_cache_control(response):
    if request.path.startswith('/bags_imgs/'):
        response.headers['Cache-Control'] = 'no-store, max-age=0'
    return response


# Main Route (Checks for Authentication)
@app.route("/")
def return_home():
    return redirect(url_for("home"))
    
# Main Route (Checks for Authentication)
@app.route("/login")
def login():
    is_auth, user_id = is_authenticated(request, session)
    if is_auth:
        return redirect(url_for("home"))
    else:
        if request.args.get('check_auth'):
            is_auth, user_id = is_authenticated(request, session)
            return jsonify({
                'type': 'auth-status',
                'isAuthenticated': is_auth,
                'userId': user_id
            }), 200

        #return render_template("login.html")


# Home Route (Protected Page)
@app.route("/home")
def home():
    is_auth, _ = is_authenticated(request, session)
    return render_template("homepage.html", is_auth=is_auth)



#API ROUTES
    
@app.route('/api/check_permission', methods=['GET'])
def check_permission():
    username = request.args.get('username')
    if not username:
        return jsonify({'error': 'Username not provided'}), 400

    user = AllowedUser.query.filter_by(username=username).first()
    is_allowed = user is not None

    return jsonify({'is_allowed': is_allowed})

@app.route("/api/bags", methods=["GET"])
def get_bags():
    items = Item.query.all()
    bags_data = []
    for item in items:
        # Get the first image as the preview image
        preview_image = item.images[0].filename if item.images else None
        
        bags_data.append({
            'id': item.id,
            'image': preview_image,  # Use the first image as preview
            'price': item.price,
            'name': item.name  # Include name if needed
        })
    return jsonify(bags_data), 200

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/bags_imgs/<filename>')
def serve_bag_image(filename):
    try:
        print(f"Attempting to serve: {filename}")
        print(f"Full path: {os.path.join(app.config['UPLOAD_FOLDER'], filename)}")
        print(f"File exists: {os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename))}")
        return send_from_directory(
            app.config['UPLOAD_FOLDER'],
            filename
        )
    except FileNotFoundError:
        app.logger.error(f"Missing file: {filename} in {app.config['UPLOAD_FOLDER']}")

@app.route('/api/bags', methods=['POST'])
def add_bag():
    try:
        # Check if files were uploaded
        if 'images[]' not in request.files:
            return jsonify({'status': 'error', 'error': 'No files uploaded'}), 400
        
        files = request.files.getlist('images[]')
        if not files or files[0].filename == '':
            return jsonify({'status': 'error', 'error': 'No files selected'}), 400

        # Validate form data
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        
        if not all([name, description, price]):
            return jsonify({'status': 'error', 'error': 'Missing required fields'}), 400

        # Create upload directory if it doesn't exist
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        # Create the item
        new_item = Item(
            name=name,
            description=description,
            price=price
        )
        db.session.add(new_item)
        db.session.flush()  # Get the ID before commit

        # Process images
        saved_filenames = []
        for i, file in enumerate(files):
            if file and allowed_file(file.filename):
                # Secure the filename
                original_ext = os.path.splitext(file.filename)[1].lower()
                filename = f"{uuid.uuid4()}{original_ext}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                
                try:
                    file.save(filepath)
                    
                    new_image = ItemImage(
                        item_id=new_item.id,
                        filename=filename,
                        position=i
                    )
                    db.session.add(new_image)
                    saved_filenames.append(filename)
                except Exception as e:
                    app.logger.error(f"Error saving file {filename}: {str(e)}")
                    continue

        db.session.commit()

        return jsonify({
            'status': 'success',
            'item_id': new_item.id,
            'filenames': saved_filenames
        }), 201

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error in add_bag: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': 'Internal server error'
        }), 500

@app.route('/api/bags/<int:bag_id>', methods=['DELETE'])
def delete_bag(bag_id):
    # Check Telegram session authentication
    if 'telegram_id' not in session:
        return jsonify({'error': 'Telegram authentication required'}), 401
    
    # Additional admin check if needed
    if not session.get('is_admin', False):
        return jsonify({'error': 'Admin privileges required'}), 403
    
    bag = Item.query.get(bag_id)
    if not bag:
        return jsonify({'error': 'Bag not found'}), 404
    
    try:
        db.session.delete(bag)
        db.session.commit()
        return jsonify({'message': 'Deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/bags/<int:bag_id>')
def get_bag_details(bag_id):
    item = Item.query.get(bag_id)
    if not item:
        return jsonify({'error': 'Bag not found'}), 404
    
    # Get images ordered by position
    images = ItemImage.query.filter_by(item_id=bag_id).order_by(ItemImage.position).all()
    
    return jsonify({
        'id': item.id,
        'name': item.name,
        'description': item.description,
        'price': item.price,
        'images': [{
            'id': img.id,
            'url': url_for('serve_bag_image', filename=img.filename, _external=True),
            'position': img.position
        } for img in images]
    })

@app.route('/api/bags/<int:bag_id>/images/order', methods=['PUT'])
def update_image_order(bag_id):
    data = request.get_json()
    if not data or 'order' not in data:
        return jsonify({'error': 'No order data provided'}), 400
    
    try:
        for image_id, position in data['order'].items():
            image = ItemImage.query.filter_by(id=image_id, item_id=bag_id).first()
            if image:
                image.position = position
        
        db.session.commit()
        return jsonify({'message': 'Image order updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/bags/<int:bag_id>/images', methods=['POST'])
def add_bag_images(bag_id):
    if 'telegram_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401

    # Check if files were uploaded
    if 'images[]' not in request.files:
        return jsonify({'error': 'No files uploaded'}), 400

    files = request.files.getlist('images[]')
    if not files or files[0].filename == '':
        return jsonify({'error': 'No files selected'}), 400

    try:
        # Get current max position to append new images
        max_position = db.session.query(db.func.max(ItemImage.position)).filter_by(item_id=bag_id).scalar() or 0
        
        saved_filenames = []
        for i, file in enumerate(files):
            if file and allowed_file(file.filename):
                # Secure the filename
                original_ext = os.path.splitext(file.filename)[1].lower()
                filename = f"{uuid.uuid4()}{original_ext}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                
                file.save(filepath)
                
                new_image = ItemImage(
                    item_id=bag_id,
                    filename=filename,
                    position=max_position + i + 1  # Append after existing images
                )
                db.session.add(new_image)
                saved_filenames.append(filename)

        db.session.commit()
        return jsonify({
            'status': 'success',
            'filenames': saved_filenames
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route("/api/check_auth")
def check_auth():
    is_auth, user_id = is_authenticated(request, session)
    return jsonify({
        'isAuthenticated': is_auth,
        'userId': user_id
    }), 200

@app.route("/api/user", methods=['GET'])
def get_user_info():
    if 'telegram_id' in session:
        user_data = {
            "id": session.get('telegram_id'),
            "first_name": session.get('user_data', {}).get('first_name'),
            "last_name": session.get('user_data', {}).get('last_name'),
            "username": session.get('user_data', {}).get('username'),
            "is_admin": session.get('is_admin', False)
        }
        return jsonify(user_data), 200
    return jsonify({'error': 'User not authenticated'}), 401


if __name__ == "__main__":
    app.run(debug=True, port=8000)

@app.route('/avatars/<int:user_id>')
def serve_avatar(user_id):
    avatar_dir = 'backend/avatars'
    filename = f"{user_id}.jpg" # Assuming JPG extension

    try:
        return send_from_directory(avatar_dir, filename)
    except FileNotFoundError:
        return "Avatar not found", 404

@app.route('/proxy/avatar')
def proxy_avatar():
    """Proxies avatar images from a given URL."""
    url = request.args.get('url')
    logging.debug(f"Proxying avatar from URL: {url}")
    if not url:
        return "Missing image URL", 400
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        # Return the image data with the appropriate content type
        return response.content, response.status_code, {'Content-Type': response.headers.get('Content-Type', 'image/jpeg')}
        response = make_response(response.content)
        response.headers['Content-Type'] = response.headers.get('Content-Type', 'image/jpeg')
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"Error proxying avatar from {url}: {e}")
        return "Image not found or could not be downloaded.", 404
    
# Export for bot.py
if __name__ != "__main__":
    from app import app, db