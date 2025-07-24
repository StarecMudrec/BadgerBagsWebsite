import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import uuid
from datetime import datetime, timedelta
from functools import wraps
from app import app, db
from models import AdminToken, AllowedAdmin

# Get bot token from environment
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN environment variable set")

bot = telebot.TeleBot(BOT_TOKEN)

# Define the with_app_context decorator
def with_app_context(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with app.app_context():
            return func(*args, **kwargs)
    return wrapper

# Create main menu keyboard
def create_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton('/addadmin'),
        KeyboardButton('/getlink'),
        KeyboardButton('/listadmins'),
        KeyboardButton('/help')
    )
    return markup

# Help command
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    help_text = """
    🤖 *Admin Bot Commands*:

    /addadmin - Add new admin (Main admin only)
    /getlink - Generate admin login link
    /listadmins - List all admins (Main admin only)
    /help - Show this help message
    """
    bot.reply_to(message, help_text, parse_mode='Markdown', reply_markup=create_main_menu())

# Add admin command
@bot.message_handler(commands=['addadmin'])
@with_app_context
def add_admin(message):
    main_admin_id = int(os.getenv('MAIN_ADMIN_ID', 0))
    if message.from_user.id != main_admin_id:
        bot.reply_to(message, "❌ Only the main admin can add new admins!")
        return

    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "Please enter the username after the command:\n`/addadmin username`", 
                        parse_mode='Markdown', reply_markup=create_main_menu())
            return
            
        username = parts[1].replace('@', '')
        
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("✅ Confirm", callback_data=f"confirm_add:{username}"),
            InlineKeyboardButton("❌ Cancel", callback_data="cancel_add")
        )
        
        bot.reply_to(message, f"Add @{username} as admin?", reply_markup=markup)
        
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

# List admins command
@bot.message_handler(commands=['listadmins'])
@with_app_context
def list_admins(message):
    main_admin_id = int(os.getenv('MAIN_ADMIN_ID', 0))
    if message.from_user.id != main_admin_id:
        bot.reply_to(message, "❌ Only the main admin can view admin list!")
        return

    admins = AllowedAdmin.query.filter_by(is_active=True).all()
    if not admins:
        bot.reply_to(message, "No active admins found", reply_markup=create_main_menu())
        return

    markup = InlineKeyboardMarkup(row_width=1)
    for admin in admins:
        btn_text = f"@{admin.telegram_username}"
        if admin.telegram_id:
            btn_text += f" (ID: {admin.telegram_id})"
        markup.add(InlineKeyboardButton(btn_text, callback_data=f"admin_detail:{admin.id}"))

    markup.add(InlineKeyboardButton("🔙 Back", callback_data="back_to_main"))
    bot.reply_to(message, "Active admins:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "back_to_main")
def handle_back_to_main(call):
    with app.app_context():  # Add application context
        try:
            help_text = """
            🤖 *Admin Bot Commands*:

    /addadmin - Add new admin (Main admin only)
    /getlink - Generate admin login link
    /listadmins - List all admins (Main admin only)
    /help - Show this help message
            """
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(
                call.message.chat.id,
                help_text,
                parse_mode='Markdown',
                reply_markup=create_main_menu()
            )
        except Exception as e:
            bot.answer_callback_query(call.id, f"Error: {str(e)}")
        finally:
            bot.answer_callback_query(call.id)

# Update the back_to_list callback handler
@bot.callback_query_handler(func=lambda call: call.data == "back_to_list")
def handle_back_to_list(call):
    main_admin_id = int(os.getenv('MAIN_ADMIN_ID', 0))
    if call.from_user.id != main_admin_id:
        bot.answer_callback_query(call.id, "❌ Only the main admin can view admin list!")
        return
    
    with app.app_context():  # Add application context
        try:
            admins = AllowedAdmin.query.filter_by(is_active=True).all()
            if not admins:
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text="No active admins found"
                )
                return

            markup = InlineKeyboardMarkup(row_width=1)
            for admin in admins:
                btn_text = f"@{admin.telegram_username}"
                if admin.telegram_id:
                    btn_text += f" (ID: {admin.telegram_id})"
                markup.add(InlineKeyboardButton(btn_text, callback_data=f"admin_detail:{admin.id}"))

            markup.add(InlineKeyboardButton("🔙 Back", callback_data="back_to_main"))
            
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Active admins:",
                reply_markup=markup
            )
        except Exception as e:
            bot.answer_callback_query(call.id, f"Error: {str(e)}")
        finally:
            bot.answer_callback_query(call.id)

# Admin detail view
@bot.callback_query_handler(func=lambda call: call.data.startswith("admin_detail:"))
def show_admin_detail(call):
    admin_id = call.data.split(":")[1]
    with app.app_context():
        admin = AllowedAdmin.query.get(admin_id)
        if admin:
            text = (
                f"👤 *Admin Details*\n"
                f"Username: @{admin.telegram_username}\n"
                f"Telegram ID: `{admin.telegram_id or 'Not set'}`\n"
                f"Added: {admin.created_at.strftime('%Y-%m-%d')}"
            )
            
            markup = InlineKeyboardMarkup()
            markup.row(
                InlineKeyboardButton("❌ Remove", callback_data=f"remove_admin:{admin.id}"),
                InlineKeyboardButton("✏️ Edit", callback_data=f"edit_admin:{admin.id}")
            )
            markup.row(InlineKeyboardButton("🔙 Back", callback_data="back_to_list"))
            
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=text,
                parse_mode='Markdown',
                reply_markup=markup
            )
        bot.answer_callback_query(call.id)

# Handle all callbacks
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    if call.data.startswith("confirm_add:"):
        username = call.data.split(":")[1]
        with app.app_context():
            try:
                existing_admin = AllowedAdmin.query.filter_by(telegram_username=username).first()
                if existing_admin:
                    bot.answer_callback_query(call.id, f"@{username} is already an admin!")
                    return
                    
                new_admin = AllowedAdmin(
                    telegram_username=username,
                    telegram_id=call.from_user.id,
                    is_active=True
                )
                db.session.add(new_admin)
                db.session.commit()
                bot.answer_callback_query(call.id, f"✅ @{username} added!")
                bot.send_message(call.message.chat.id, 
                                f"Admin @{username} added successfully!",
                                reply_markup=create_main_menu())
            except Exception as e:
                db.session.rollback()
                bot.answer_callback_query(call.id, f"Error: {str(e)}")
                
    elif call.data == "cancel_add":
        bot.answer_callback_query(call.id, "Cancelled")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, 
                        "Admin addition cancelled.",
                        reply_markup=create_main_menu())
    
    elif call.data == "back_to_list":
        list_admins(call.message)
    
    elif call.data == "back_to_main":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        send_welcome(call.message)
    
    elif call.data.startswith("remove_admin:"):
        admin_id = call.data.split(":")[1]
        with app.app_context():
            admin = AllowedAdmin.query.get(admin_id)
            if admin:
                db.session.delete(admin)
                db.session.commit()
                bot.answer_callback_query(call.id, "Admin removed!")
                bot.send_message(call.message.chat.id,
                                f"Admin @{admin.telegram_username} has been removed.",
                                reply_markup=create_main_menu())
    
    elif call.data.startswith("edit_admin:"):
        admin_id = call.data.split(":")[1]
        bot.answer_callback_query(call.id, "Edit feature coming soon!")
        # Implement your edit logic here

# Get link command
@bot.message_handler(commands=['getlink'])
def generate_admin_link(message):
    token = str(uuid.uuid4())
    if save_admin_token(message.from_user.id, token):
        params = {
            'id': message.from_user.id,
            'first_name': message.from_user.first_name or '',
            'last_name': message.from_user.last_name or '',
            'username': message.from_user.username or '',
            'auth_date': int(datetime.now().timestamp()),
            'admin_token': token
        }
        
        # Generate the hash correctly
        data_check_string = "\n".join(
            f"{k}={v}" for k, v in sorted(params.items()) if k != 'hash'
        )
        
        secret_key = hmac.new(
            bytes(Config.BOT_TOKEN, 'utf-8'),  # Use raw token string
            msg=b"WebAppData",
            digestmod=sha256
        ).digest()
        
        params['hash'] = hmac.new(
            secret_key,
            data_check_string.encode(),
            sha256
        ).hexdigest()
        
        # Build URL for YOUR domain
        query_string = "&".join(f"{k}={v}" for k, v in params.items())
        admin_link = f"https://dahole.online/auth/telegram-callback?{query_string}"
        
        # Debug output
        print(f"Generated Login URL: {admin_link}")
        
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(
            "🔑 Login as Admin", 
            url=admin_link
        ))
        
        bot.send_message(
            message.chat.id,
            "Your admin login link (expires in 5 minutes):",
            reply_markup=markup
        )
    else:
        bot.reply_to(message, "❌ Failed to generate link. Try again later.")

# Database functions
@with_app_context
def is_user_allowed(user_id):
    return AllowedAdmin.query.filter_by(
        telegram_id=user_id,
        is_active=True
    ).first() is not None

@with_app_context
def save_admin_token(user_id, token, expires_minutes=5):
    try:
        AdminToken.query.filter_by(telegram_id=user_id).update({'is_used': True})
        db.session.commit()
        
        expires_at = datetime.utcnow() + timedelta(minutes=expires_minutes)
        new_token = AdminToken(
            telegram_id=user_id,
            token=token,
            expires_at=expires_at
        )
        db.session.add(new_token)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error saving admin token: {e}")
        return False

# Remove the infinity_polling line and replace with:
if __name__ == '__main__':
    print("Starting Telegram bot...")
    # if os.environ.get('PRODUCTION') == 'true':
    #     # Webhook mode for production
    #     bot.remove_webhook()
    #     bot.set_webhook(
    #         url='https://dahole.oline/telegram-webhook',
    #         certificate=open('/path/to/cert.pem', 'r') if os.path.exists('/path/to/cert.pem') else None
    #     )
    # else:
    #     # Polling mode for development
    bot.infinity_polling()