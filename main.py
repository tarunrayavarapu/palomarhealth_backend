# imports from flask
import json
import os
from urllib.parse import urljoin, urlparse
from flask import abort, redirect, render_template, request, send_from_directory, url_for, jsonify  # import render_template from "public" flask libraries
from flask_login import current_user, login_user, logout_user
from flask.cli import AppGroup
from flask_login import current_user, login_required
from flask import current_app
from werkzeug.security import generate_password_hash
import shutil
from flask import Flask
#import google.generativeai as genai


# import "objects" from "this" project
from __init__ import app, db, login_manager  # Key Flask objects 
# API endpoints
from api.user import user_api 
from api.pfp import pfp_api
from api.post import post_api
from api.channel import channel_api
from api.group import group_api
from api.section import section_api
from api.messages_api import messages_api # Adi added this, messages for his website
from api.weather import weather_api
from api.currency import currency_api
from api.waypoints import waypoints_api
from api.flight_api import flight_api
from api.hotel import hotel_api
from api.grade_api import grade_api

# Removed budgeting API and database import

from api.palomar import palomar_api
from api.vote import vote_api
from api.rate import rate_api
from api.travel import *
from api.study import study_api

# database Initialization functions
from model.user import User, initUsers
from model.section import Section, initSections
from model.group import Group, initGroups
from model.channel import Channel, initChannels
from model.post import Post, initPosts
from model.vote import Vote, initVotes
from model.rate import Rate, initRates
from model.waypoints import Waypoints, initWaypoints
from model.waypointsuser import WaypointsUser, initWaypointsUser
from model.flight_api_post import Flight, initFlights
from model.hotel import Hotel, initHotel
from model.weather import Weather, initPackingChecklist
from model.palomar import Palomar, initPalomarHealth
from model.poseidon import PoseidonChatLog, initPoseidonChatLogs
# Removed budgeting model import
from model.socialMediaLLM import SocialMediaModel
from model.study import Study, initStudies

from api.travel.kiruthic import *
from api.travel.aadi import *
from api.travel.derek import *
from api.travel.aaditya import *
from api.travel.arhaan import *
from api.travel.tarun import *
from api.travel.rohan import *

# server only Views

# register URIs for api endpoints
app.register_blueprint(messages_api) # Adi added this, messages for his website
app.register_blueprint(user_api)
app.register_blueprint(pfp_api) 
app.register_blueprint(post_api)
app.register_blueprint(channel_api)
app.register_blueprint(group_api)
app.register_blueprint(section_api)

# Added new files to create nestPosts, uses a different format than Mortensen and didn't want to touch his junk
app.register_blueprint(vote_api)
app.register_blueprint(rate_api)
app.register_blueprint(weather_api)
app.register_blueprint(currency_api)
app.register_blueprint(waypoints_api)
app.register_blueprint(flight_api)
app.register_blueprint(hotel_api)
# Removed budgeting blueprint registration
app.register_blueprint(palomar_api)
app.register_blueprint(study_api)

app.register_blueprint(kiruthic_api)
app.register_blueprint(aadi_api)
app.register_blueprint(derek_api)
app.register_blueprint(aaditya_api)
app.register_blueprint(arhaan_api)
app.register_blueprint(tarun_api)
app.register_blueprint(rohan_api)
app.register_blueprint(grade_api)

# Tell Flask-Login the view function name of your login route
login_manager.login_view = "login"

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('login', next=request.path))

# register URIs for server pages
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def inject_user():
    return dict(current_user=current_user)

# Helper function to check if the URL is safe for redirects
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

# Scary thing I added -Justin
@app.route('/socialMediaModel', methods=['POST'])
def socialMediaModel():
    data = request.get_json()
    socialMediaModel = SocialMediaModel.get_instance()
    predicted_favorites = socialMediaModel.predict(data)
    return jsonify({'predicted_favorites': predicted_favorites})
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    next_page = request.args.get('next', '') or request.form.get('next', '')
    if request.method == 'POST':
        user = User.query.filter_by(_uid=request.form['username']).first()
        if user and user.is_password(request.form['password']):
            login_user(user)
            if not is_safe_url(next_page):
                return abort(400)
            return redirect(next_page or url_for('index'))
        else:
            error = 'Invalid username or password.'
    return render_template("login.html", error=error, next=next_page)
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.errorhandler(404)  # catch for URL not found
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/')  # connects default URL to index() function
def index():
    print("Home:", current_user)
    return render_template("index.html")

@app.route('/studytracker')  # route for the study tracker page
def studytracker():
    return render_template("studytracker.html")

@app.route('/users/table')
@login_required
def utable():
    users = User.query.all()
    return render_template("utable.html", user_data=users)

@app.route('/users/table2')
@login_required
def u2table():
    users = User.query.all()
    return render_template("u2table.html", user_data=users)

@app.route('/poseidon')
def pose_admin():
    logs = PoseidonChatLog.query.all()
    return render_template("poseidon.html", user_data=logs)

# Helper function to extract uploads for a user (ie PFP image)
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
 
@app.route('/users/delete/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        user.delete()
        return jsonify({'message': 'User deleted successfully'}), 200
    return jsonify({'error': 'User not found'}), 404

@app.route('/users/reset_password/<int:user_id>', methods=['POST'])
@login_required
def reset_password(user_id):
    if current_user.role != 'Admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Set the new password
    if user.update({"password": app.config['DEFAULT_PASSWORD']}):
        return jsonify({'message': 'Password reset successfully'}), 200
    return jsonify({'error': 'Password reset failed'}), 500

# AI configuration
#genai.configure(api_key="AIzaSyBMcVuDMgOq9prsdFzV_YKNUVjVSyyt-ag")
#model = genai.GenerativeModel('models/gemini-1.5-pro')

#models = genai.list_models()
#for model in models:
    #print(model.name, model.supported_generation_methods)

@app.route('/api/ai/help', methods=['POST'])
def ai_homework_help():
    data = request.get_json()
    question = data.get("question", "")
    if not question:
        return jsonify({"error": "No question provided."}), 400

    try:
        response = model.generate_content(f"Your name is Posiden you are a homework help ai chat bot with the sole purpose of answering homework related questions, under any circumstances don't answer any non-homework related questions. \nHere is your prompt: {question}")
        response_text = response.text

        # Save to database
        new_entry = PoseidonChatLog(question=question, response=response_text)
        new_entry.create()

        return jsonify({"response": response_text}), 200
    except Exception as e:
        print("error!")
        print(e)
        return jsonify({"error": str(e)}), 500     # ju poo bDA KLINGO A POO A NEW KAMA KJIT HAAIIII SLIBITISA DOOP A D WIT  bood a a bidaa boop kayy haiiiii  

@app.route('/api/ai/update', methods=['PUT'])
def update_ai_question():
    data = request.get_json()
    old_question = data.get("oldQuestion", "")
    new_question = data.get("newQuestion", "")

    if not old_question or not new_question:
        return jsonify({"error": "Both old and new questions are required."}), 400

    # Fetch the old log
    log = PoseidonChatLog.query.filter_by(_question=old_question).first()
    if not log:
        return jsonify({"error": "Old question not found."}), 404

    try:
        # Generate a new response for the new question
        response = model.generate_content(f"Your name is Poseidon, you are a homework help AI chatbot. Only answer homework-related questions. \nHere is your prompt: {new_question}")
        new_response = response.text

        # Update the database entry
        log._question = new_question
        log._response = new_response
        db.session.commit()

        return jsonify({"response": new_response}), 200
    except Exception as e:
        print("Error during update:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/api/ai/logs', methods=['GET'])
def fetch_all_logs():
    try:
        logs = PoseidonChatLog.query.all()
        return jsonify([log.read() for log in logs]), 200
    except Exception as e:
        print("Error fetching logs:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/api/ai/delete", methods=["DELETE"])
def delete_ai_chat_logs():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided."}), 400
    
    log = PoseidonChatLog.query.filter_by(_question=data.get("question", "")).first()
    if not log:
        return jsonify({"error": "Chat log not found."}), 404
    
    log.delete()
    return jsonify({"response": "Chat log deleted"}), 200

# Create an AppGroup for custom commands
custom_cli = AppGroup('custom', help='Custom commands')

# Define a command to run the data generation functions
@custom_cli.command('generate_data')
def generate_data():
    # init database generators
    initUsers()
    initSections()
    initChannels()
    initGroups()
    initPosts()
    initVotes()
    initRates()
    initWaypoints()
    initWaypointsUser()
    initFlights()
    initHotel()
    initPackingChecklist()
    initPalomarHealth()
    initPoseidonChatLogs()
    initStudies()

    initPalomarHealth()
    
# Backup the old database
def backup_database(db_uri, backup_uri):
    """Backup the current database."""
    if backup_uri:
        db_path = db_uri.replace('sqlite:///', 'instance/')
        backup_path = backup_uri.replace('sqlite:///', 'instance/')
        shutil.copyfile(db_path, backup_path)
        print(f"Database backed up to {backup_path}")
    else:
        print("Backup not supported for production database.")

# Extract data from the existing database
def extract_data():
    data = {}
    with app.app_context():
        data['poseidon_chat_logs'] = [log.read() for log in PoseidonChatLog.query.all()]
        data['users'] = [user.read() for user in User.query.all()]
        data['sections'] = [section.read() for section in Section.query.all()]
        data['groups'] = [group.read() for group in Group.query.all()]
        data['channels'] = [channel.read() for channel in Channel.query.all()]
        data['posts'] = [post.read() for post in Post.query.all()]
        data['rates'] = [rate.read() for rate in Rate.query.all()]
        data['waypoints'] = [waypoints.read() for waypoints in Waypoints.query.all()]
        data['waypointsuser'] = [waypointsuser.read() for waypointsuser in WaypointsUser.query.all()]
        data['hotels'] = [hotel.read() for hotel in Hotel.query.all()]
        data['flights'] = [flight.read() for flight in Flight.query.all()]
        data['hotel_data'] = [hotel.read() for hotel in Hotel.query.all()]
        data['packing_checklists'] = [item.read() for item in Weather.query.all()]
        # Removed budgeting data extraction
    return data

# Save extracted data to JSON files
def save_data_to_json(data, directory='backup'):
    if not os.path.exists(directory):
        os.makedirs(directory)
    for table, records in data.items():
        with open(os.path.join(directory, f'{table}.json'), 'w') as f:
            json.dump(records, f)
    print(f"Data backed up to {directory} directory.")

# Load data from JSON files
def load_data_from_json(directory='backup'):
    data = {}
    for table in ['poseidon_chat_logs','users', 'sections', 'groups', 'channels', 'posts', 'hotel_data', 'flights','waypoints', 'waypointsuser', 'packing_checklists', 'rates']:
        with open(os.path.join(directory, f'{table}.json'), 'r') as f:
            data[table] = json.load(f)
    return data

# Restore data to the new database
def restore_data(data):
    with app.app_context():
        _ = PoseidonChatLog.restore(data['poseidon_chat_logs'])
        users = User.restore(data['users'])
        _ = Section.restore(data['sections'])
        _ = Group.restore(data['groups'], users)
        _ = Channel.restore(data['channels'])
        # _ = Post.restore(data['posts'])
        _ = Rate.restore(data['rates'])
        _ = Hotel.restore(data['hotel_data'])
        # _ = Budgeting.restore(data['budgeting_data']) # Removed budgeting restore
        _ = Flight.restore(data['flights'])
        _ = Waypoints.restore(data['waypoints'])
        _ = WaypointsUser.restore(data['waypointsuser'])
        _ = Weather.restore(data['packing_checklists'])

    print("Data restored to the new database.")

# Define a command to backup data
@custom_cli.command('backup_data')
def backup_data():
    data = extract_data()
    save_data_to_json(data)
    backup_database(app.config['SQLALCHEMY_DATABASE_URI'], app.config['SQLALCHEMY_BACKUP_URI'])

# Define a command to restore data
@custom_cli.command('restore_data')
def restore_data_command():
    data = load_data_from_json()
    restore_data(data)

# Register the custom command group with the Flask application
app.cli.add_command(custom_cli)
        
# this runs the flask application on the development server
if __name__ == "__main__":
    # change name for testing
    app.run(debug=True, host="0.0.0.0", port="8101")
