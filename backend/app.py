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
from models import db, AuthToken, Item, AdminToken, ItemImage
from config import Config
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
from functools import wraps

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

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            return jsonify({'status': 'error', 'error': 'Admin access required. User is admin: ' + str(session.get('is_admin'))}), 403
        return f(*args, **kwargs)
    return decorated_function

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
        })
    return jsonify(bags_data), 200

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/bags_imgs/<filename>')
def serve_bag_image(filename):
    try:
        # Add security check to prevent directory traversal
        if not filename or '../' in filename:
            raise FileNotFoundError
        
        return send_from_directory(
            app.config['UPLOAD_FOLDER'],
            filename,
            mimetype='image/jpeg'  # Adjust based on your image types
        )
    except FileNotFoundError:
        app.logger.error(f"Missing file: {filename} in {app.config['UPLOAD_FOLDER']}")
        # Return a default image or 404 response
        return send_from_directory('static', 'default-image.jpg', mimetype='image/jpeg'), 404

@app.route('/api/bags', methods=['POST'])
@admin_required
def add_bag():
    try:
        # Check if files were uploaded
        if 'images[]' not in request.files:
            return jsonify({'status': 'error', 'error': 'No files uploaded'}), 400
        
        files = request.files.getlist('images[]')
        if not files or files[0].filename == '':
            return jsonify({'status': 'error', 'error': 'No files selected'}), 400

        # Validate form data
        description = request.form.get('description')
        price = request.form.get('price')
        
        if not all([description, price]):
            return jsonify({'status': 'error', 'error': 'Missing required fields'}), 400

        # Create upload directory if it doesn't exist
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        # Create the item
        new_item = Item(
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
@admin_required
def delete_bag(bag_id):
    try:
        # Start a transaction
        db.session.begin()
        
        # Find the bag
        bag = Item.query.get(bag_id)
        if not bag:
            return jsonify({'error': 'Bag not found'}), 404
        
        # First delete all associated images
        images = ItemImage.query.filter_by(item_id=bag_id).all()
        for image in images:
            try:
                # Delete the file from filesystem
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
                if os.path.exists(file_path):
                    os.remove(file_path)
            except OSError as e:
                logging.warning(f"Error deleting image file: {e}")
            
            # Delete the image record
            db.session.delete(image)
        
        # Now delete the bag
        db.session.delete(bag)
        db.session.commit()
        
        return jsonify({'message': 'Deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error deleting bag {bag_id}: {str(e)}")
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
        'description': item.description,
        'price': item.price,
        'images': [{
            'id': img.id,
            'url': url_for('serve_bag_image', filename=img.filename, _external=True),
            'position': img.position
        } for img in images]
    })

@app.route('/api/bags/<int:bag_id>', methods=['PUT'])
@admin_required
def update_bag(bag_id):
    
    bag = Item.query.get(bag_id)
    if not bag:
        return jsonify({'error': 'Bag not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        if 'description' in data:
            bag.description = data['description']
        
        if 'price' in data:
            bag.price = data['price']
        
        db.session.commit()
        return jsonify({'message': 'Bag updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/bags/<int:bag_id>/images/<int:image_id>', methods=['PUT'])
@admin_required
def update_bag_image(bag_id, image_id):
    try:
        # Check if the image exists
        image = ItemImage.query.filter_by(id=image_id, item_id=bag_id).first()
        if not image:
            return jsonify({'error': 'Image not found'}), 404

        # Check if file was uploaded
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400

        file = request.files['image']
        if not file or file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400

        # Generate new filename (keep same extension)
        original_ext = os.path.splitext(image.filename)[1].lower()
        new_filename = f"{uuid.uuid4()}{original_ext}"
        new_filepath = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)

        # Save the new file
        try:
            file.save(new_filepath)
        except Exception as e:
            app.logger.error(f"Error saving new image file: {str(e)}")
            return jsonify({'error': 'Failed to save image'}), 500

        # Delete the old file
        old_filepath = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        try:
            if os.path.exists(old_filepath):
                os.remove(old_filepath)
        except OSError as e:
            app.logger.warning(f"Error deleting old image file: {str(e)}")

        # Update the image record
        image.filename = new_filename
        db.session.commit()

        return jsonify({
            'status': 'success',
            'url': url_for('serve_bag_image', filename=new_filename, _external=True)
        }), 200

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error updating image {image_id} for bag {bag_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/bags/<int:bag_id>/images/order', methods=['PUT'])
@admin_required
def update_image_order(bag_id):
    data = request.get_json()
    if not data or 'order' not in data:
        return jsonify({'error': 'No order data provided'}), 400
    
    try:
        # First get all existing images for this bag
        existing_images = ItemImage.query.filter_by(item_id=bag_id).all()
        existing_image_ids = {str(img.id) for img in existing_images}
        
        # Check for images to delete (present in DB but not in the order)
        submitted_image_ids = set(data['order'].keys())
        images_to_delete = existing_image_ids - submitted_image_ids
        
        # Delete images not in the new order
        for image_id in images_to_delete:
            try:
                image_id_int = int(image_id)
                image = ItemImage.query.filter_by(id=image_id_int, item_id=bag_id).first()
                if image:
                    # Delete the file from filesystem
                    try:
                        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
                    except OSError as e:
                        logging.warning(f"Error deleting image file: {e}")
                    
                    db.session.delete(image)
            except ValueError:
                continue
        
        # Process the order updates
        for image_id, position in data['order'].items():
            try:
                image_id_int = int(image_id)
                image = ItemImage.query.filter_by(id=image_id_int, item_id=bag_id).first()
                if image:
                    image.position = position
            except ValueError:
                continue
        
        db.session.commit()
        return jsonify({'message': 'Image order updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error updating image order: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/bags/<int:bag_id>/images', methods=['POST'])
@admin_required
def add_bag_images(bag_id):
    # Check if files were uploaded
    if 'images[]' not in request.files:
        return jsonify({'error': 'No files uploaded'}), 400

    files = request.files.getlist('images[]')
    if not files or files[0].filename == '':
        return jsonify({'error': 'No files selected'}), 400

    try:
        # Verify the bag exists
        bag = Item.query.get(bag_id)
        if not bag:
            return jsonify({'error': 'Bag not found'}), 404

        # Get current max position to append new images
        max_position = db.session.query(db.func.max(ItemImage.position)).filter_by(item_id=bag_id).scalar() or 0
        
        saved_filenames = []
        saved_images = []
        
        # Process files sequentially to avoid conflicts
        for i, file in enumerate(files):
            if file and allowed_file(file.filename):
                try:
                    # Secure the filename
                    original_ext = os.path.splitext(file.filename)[1].lower()
                    filename = secure_filename(f"{uuid.uuid4()}{original_ext}")
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    
                    # Ensure directory exists
                    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                    
                    # Save the file immediately
                    file.save(filepath)
                    
                    # Create new image record
                    new_image = ItemImage(
                        item_id=bag_id,
                        filename=filename,
                        position=max_position + i + 1
                    )
                    db.session.add(new_image)
                    db.session.flush()  # Flush to get the ID
                    
                    saved_filenames.append(filename)
                    saved_images.append({
                        'filename': filename,
                        'id': new_image.id
                    })
                    app.logger.info(f"Successfully saved image {filename} for bag {bag_id}")
                    
                except Exception as e:
                    app.logger.error(f"Error processing file {file.filename}: {str(e)}")
                    # Clean up the file if it was saved but DB operation failed
                    if os.path.exists(filepath):
                        try:
                            os.remove(filepath)
                        except OSError:
                            pass
                    continue

        db.session.commit()
        
        # Get the URLs for the saved images
        image_urls = [url_for('serve_bag_image', filename=img['filename'], _external=True) for img in saved_images]
        image_ids = [img['id'] for img in saved_images]
        
        return jsonify({
            'status': 'success',
            'filenames': saved_filenames,
            'image_urls': image_urls,
            'image_ids': image_ids
        }), 201

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error adding images to bag {bag_id}: {str(e)}")
        # Clean up any saved files if transaction failed
        for filename in saved_filenames:
            try:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            except OSError:
                pass
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/bags/<int:bag_id>/images/<int:image_id>', methods=['DELETE'])
@admin_required
def delete_bag_image(bag_id, image_id):

    try:
        # Find and delete the image
        image = ItemImage.query.filter_by(id=image_id, item_id=bag_id).first()
        if not image:
            return jsonify({'error': 'Image not found'}), 404
        
        # Delete the file from filesystem
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
        except OSError as e:
            logging.warning(f"Error deleting image file: {e}")
        
        db.session.delete(image)
        db.session.commit()
        return jsonify({'message': 'Image deleted successfully'}), 200
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