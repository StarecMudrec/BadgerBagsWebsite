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
from models import db, AuthToken, Item, AllowedUser, AdminToken
from config import Config
from datetime import datetime, timedelta

app = Flask(__name__)
app.config.from_object(Config)

UPLOAD_FOLDER = '../frontend/public/bag_imgs'  # Changed from just 'bag_imgs'
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

# @app.after_request
# def apply_csp(response):
#     response.headers['Content-Security-Policy'] = (
#         "frame-ancestors 'self' https://dahole.online; "
#         "frame-src 'self' https://oauth.telegram.org;"
#     )
#     return response


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

@app.route('/card_imgs/<filename>')
def serve_card_image(filename):
    # Создаем папку если ее нет
    os.makedirs('card_imgs', exist_ok=True)
    return send_from_directory('card_imgs', filename)

# @app.route("/api/seasons")
# def get_seasons():
#     seasons = Season.query.order_by(Season.id.asc()).all()
#     season_ids = [season.id for season in seasons]
#     # print(season_names)
#     return jsonify(season_ids), 200

# @app.route("/api/seasons", methods=["POST"])
# def add_season():
#     is_auth, user_id = is_authenticated(request, session)
#     if not is_auth:
#         return jsonify({'error': 'Unauthorized'}), 401

#     # Check if the current user is allowed to add seasons (same logic as adding cards)
#     current_user_username = session.get('telegram_username') # Assuming username is stored in session
#     logging.debug(f"Attempting to add season. User: {current_user_username}")
#     allowed_user = AllowedUser.query.filter_by(username=current_user_username).first()
#     logging.debug(f"AllowedUser query result: {allowed_user}")

#     if not current_user_username or not allowed_user:
#         return jsonify({'error': 'You are not allowed to add seasons'}), 403

#     # Generate a UUID for the new season
#     new_season_uuid = str(uuid.uuid4())

#     # Create a new Season entry with the UUID as both id and name
#     new_season = Season(uuid=new_season_uuid, name="_")
#     db.session.add(new_season)
#     db.session.commit()
#     return jsonify({'message': 'Season added successfully', 'uuid': new_season.uuid, 'name': new_season.name}), 201

# @app.route("/api/seasons/<season_uuid>", methods=["PUT"])
# def update_season(season_uuid):
#     is_auth, user_id = is_authenticated(request, session)
#     if not is_auth:
#         return jsonify({'error': 'Unauthorized'}), 401

#     # Check if the current user is allowed to update seasons
#     current_user_username = session.get('telegram_username') # Assuming username is stored in session
#     if not current_user_username or not AllowedUser.query.filter_by(username=current_user_username).first():
#         return jsonify({'error': 'You are not allowed to update seasons'}), 403

#     season = Season.query.filter_by(uuid=season_uuid).first()
#     if not season:
#         return jsonify({'error': 'Season not found'}), 404

#     data = request.get_json()
#     if not data:
#         return jsonify({'error': 'No data provided'}), 400

#     try:
#         if 'name' in data:
#             season.name = data['name']
#         db.session.commit()
#         return jsonify({'message': 'Season updated successfully', 'uuid': season.uuid, 'name': season.name}), 200
#     except Exception as e:
#         db.session.rollback()
#         logging.error(f"Error updating season: {e}")
#         return jsonify({'error': 'Error updating season'}), 500
    
# @app.route("/api/seasons/<season_uuid>", methods=["DELETE"])
# def delete_season(season_uuid):
#     is_auth, user_id = is_authenticated(request, session)
#     if not is_auth:
#         return jsonify({'error': 'Unauthorized'}), 401

#     # Check if the current user is allowed to delete seasons
#     current_user_username = session.get('telegram_username')
#     if not current_user_username or not AllowedUser.query.filter_by(username=current_user_username).first():
#         return jsonify({'error': 'You are not allowed to delete seasons'}), 403

#     season = Season.query.filter_by(uuid=season_uuid).first()
#     if not season:
#         return jsonify({'error': 'Season not found'}), 404

#     try:
#         db.session.delete(season)
#         db.session.commit()
#         return jsonify({'message': 'Season deleted successfully'}), 200
#     except Exception as e:
#         db.session.rollback()
#         logging.error(f"Error deleting season: {e}")
#         return jsonify({'error': 'Error deleting season'}), 500
    
# @app.route("/api/cards/<season_id>")
# def get_cards(season_id):  
#     season = Season.query.filter_by(uuid=season_id).first_or_404()
#     cards = (season.cards)
#     cards_uuids = [card.uuid for card in cards]
#     return jsonify(cards_uuids), 200

# @app.route("/api/cards", methods=["POST"])
# def add_card():
#     is_auth, user_id = is_authenticated(request, session)
#     if not is_auth:
#         return jsonify({'error': 'Unauthorized'}), 401

#     # Check if the current user is allowed to add cards
#     current_user_username = session.get('telegram_username') # Assuming username is stored in session
#     if not current_user_username or not AllowedUser.query.filter_by(username=current_user_username).first():
#         return jsonify({'error': 'You are not allowed to add cards'}), 403



#     uuid = request.form.get('uuid')
#     category = request.form.get('category')
#     name = request.form.get('name')
#     description = request.form.get('description')
#     season_id = request.form.get('season_id')
#     img_file = request.files.get('img')

#     img = None
#     if img_file:
#         # Save the image file
#         # Check if the file is an allowed image type
#         allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
#         if '.' not in img_file.filename or img_file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
#             return jsonify({'error': 'Unsupported file type'}), 400

#         img_filename = str(uuid) + os.path.splitext(img_file.filename)[1]  # Use card UUID as filename
#         img_path = os.path.join('card_imgs', img_filename)
#         img_file.save(img_path)
#         img = img_filename # Store just the filename in the database
#     if not all([uuid, img, category, name, description, season_id]):
#         return jsonify({'error': 'Missing required fields'}), 400

#     new_card = Card(uuid=uuid, img=img, category=category, name=name, description=description, season_id=season_id)
#     try:
#         db.session.add(new_card)
#         db.session.commit()
#         return jsonify({'message': 'Card added successfully', 'uuid': new_card.uuid}), 201
#     except Exception as e:
#         db.session.rollback()
#         logging.error(f"Error adding card: {e}")
#         return jsonify({'error': 'Error adding card'}), 500

# @app.route("/api/cards/<card_id>", methods=["DELETE"])
# def delete_card(card_id):
#     is_auth, user_id = is_authenticated(request, session)
#     if not is_auth:
#         return jsonify({'error': 'Unauthorized'}), 401

#     # Check if the current user is allowed to delete cards
#     current_user_username = session.get('telegram_username') # Assuming username is stored in session
#     if not current_user_username or not AllowedUser.query.filter_by(username=current_user_username).first():
#         return jsonify({'error': 'You are not allowed to delete cards'}), 403


#     card = Card.query.filter_by(uuid=card_id).first()

#     if card is None:
#         return jsonify({'error': 'Card not found'}), 404

#     try:
#         # Optionally delete the associated image file
#         if card.img and os.path.exists(os.path.join('card_imgs', card.img)):
#             os.remove(os.path.join('card_imgs', card.img))

#         db.session.delete(card)
#         db.session.commit()
#         return jsonify({'message': 'Card deleted successfully'}), 200
#     except Exception as e:
#         db.session.rollback()
#         logging.error(f"Error deleting card: {e}")
#         return jsonify({'error': 'Error deleting card'}), 500
    
@app.route('/api/check_permission', methods=['GET'])
def check_permission():
    username = request.args.get('username')
    if not username:
        return jsonify({'error': 'Username not provided'}), 400

    user = AllowedUser.query.filter_by(username=username).first()
    is_allowed = user is not None

    return jsonify({'is_allowed': is_allowed})
    
# @app.route("/api/card_info/<card_id>")
# def get_card_info(card_id):  
#     print(card_id)
#     card = Card.query.filter_by(uuid=card_id).first_or_404()
#     return jsonify(card.present()), 200

# @app.route("/api/cards/<card_id>", methods=["PUT"])
# def update_card(card_id):
#     is_auth, user_id = is_authenticated(request, session)
#     if not is_auth:
#         return jsonify({'error': 'Unauthorized'}), 401

#     card = Card.query.filter_by(id=card_id).first()
#     if not card:
#         return jsonify({'error': 'Card not found'}), 404

#     data = request.get_json()
#     if not data:
#         return jsonify({'error': 'No data provided'}), 400

#     try:
#         if 'name' in data:
#             card.name = data['name']
#         if 'description' in data:
#             card.description = data['description']
#         if 'category' in data:
#             card.category = data['category']
#         if 'season_uuid' in data:
#             season = Season.query.filter_by(uuid=data['season_uuid']).first()
#             if not season:
#                 return jsonify({'error': 'Season not found'}), 404
#             card.season_id = season.id

#         db.session.commit()
#         return jsonify({'message': 'Card updated successfully'}), 200
#     except Exception as e:
#         db.session.rollback()
#         logging.error(f"Error updating card: {e}")
#         return jsonify({'error': 'Error updating card'}), 500
        
# @app.route("/api/cards/<card_uuid>/image", methods=["PUT"])
# def update_card_image(card_uuid):
#     is_auth, user_id = is_authenticated(request, session)

#     if request.method != 'PUT':
#         return jsonify({'error': 'Method Not Allowed'}), 405

#     if not is_auth:
#         return jsonify({'error': 'Unauthorized'}), 401

#     # Check if the current user is allowed to update cards
#     current_user_username = session.get('telegram_username')
#     if not current_user_username or not AllowedUser.query.filter_by(username=current_user_username).first():
#         return jsonify({'error': 'You are not allowed to update card images'}), 403

#     card = Card.query.filter_by(uuid=card_uuid).first()
#     if not card:
#         return jsonify({'error': 'Card not found'}), 404

#     if 'image' not in request.files:
#         return jsonify({'error': 'No image file provided'}), 400

#     img_file = request.files['image']

#     # Check if the file is an allowed image type
#     allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
#     if '.' not in img_file.filename or img_file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
#         return jsonify({'error': 'Unsupported file type'}), 400

#     # Generate a unique filename using the card UUID
#     img_filename = str(card.uuid) + os.path.splitext(img_file.filename)[1].lower()
#     img_path = os.path.join('card_imgs', img_filename)

#     try:
#         # Delete the old image file if it exists and is not the new one
#         if card.img and os.path.exists(os.path.join('card_imgs', card.img)) and card.img != img_filename:
#             os.remove(os.path.join('card_imgs', card.img))
#             logging.debug(f"Deleted old image: {card.img}")

#         # Save the new image file
#         img_file.save(img_path)
#         logging.debug(f"Saved new image: {img_filename}")

#         # Update the card's image field in the database
#         card.img = img_filename
#         db.session.commit()
#         logging.debug(f"Updated card {card.uuid} with new image: {img_filename}")

#         return jsonify({'message': 'Card image updated successfully', 'img': img_filename}), 200
#     except Exception as e:
#         db.session.rollback()
#         logging.error(f"Error updating card image: {e}")
#         return jsonify({'error': 'Error updating card image'}), 500

# @app.route("/api/season_info/<int:season_id>")
# def get_season_info(season_id):  
#     season = Season.query.filter_by(id=season_id).first_or_404()
#     return jsonify(season.present()), 200

# @app.route("/api/comments/<card_id>")
# def get_comments(card_id):
#     card = Card.query.filter_by(id=card_id).first_or_404()
#     comments = [comment.present() for comment in card.comments]
#     return jsonify(comments), 200

@app.route("/api/bags", methods=["GET"])
def get_bags():
    items = Item.query.all()
    bags_data = []
    for item in items:
        bags_data.append({
            'image': item.img,
            'price': item.price
        })
    return jsonify(bags_data), 200

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/bags_imgs/<filename>')
def serve_bag_image(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except FileNotFoundError:
        app.logger.error(f"File not found: {filename} in {app.config['UPLOAD_FOLDER']}")
        # abort(404)

@app.route('/api/bags', methods=['POST'])
def add_bag():
    if 'img' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['img']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not (file and allowed_file(file.filename)):
        return jsonify({'error': 'Invalid file type'}), 400

    try:
        # Create directory if it doesn't exist
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        # Secure the filename and save
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Get other form data
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        
        # Create new bag in database
        new_bag = Item(
            name=name,
            description=description,
            price=price,
            img=filename  # Store just the filename
        )
        db.session.add(new_bag)
        db.session.commit()
        
        return jsonify({
            'message': 'Bag added successfully',
            'bag': {
                'id': new_bag.id,
                'name': new_bag.name,
                'image': filename
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route("/api/bags/<int:bag_id>")
def get_bag_details(bag_id):
    item = Item.query.get_or_404(bag_id)
    return jsonify({
        'id': item.id,
        'name': item.name,
        'description': item.description,
        'price': item.price,
        'image': item.img
    })

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