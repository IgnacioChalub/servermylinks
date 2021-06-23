from flask import blueprints, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from models import User, Link
from request_validators import *

views = blueprints.Blueprint('views', __name__)

@views.route("/", methods=['GET'])
def home():   
    return jsonify({"message": "Welcome!"})

#recives json with username, password and email
@views.route("/signup", methods=['POST'])
def sign_up():

        if not signup_validator(request.json):
            return jsonify({"error": "request format not valid"}), 400

        username = request.json['username']
        password = request.json['password']
        email = request.json['email']

        user_by_email = User.query.filter_by(email=email).first()
        user_by_username = User.query.filter_by(username=username).first()

        if user_by_email or user_by_username:
            return jsonify({"error": "username or email already exist"})
        elif len(email) < 4:
            return jsonify({"error": "email not valid"})
        elif len(username) < 4:
            return jsonify({"error": "username not valid"})
        elif len(password) < 4:
            return jsonify({"error": "password not valid"})
        else:
            new_user = User(username=username, password=generate_password_hash(password, method='sha256'), email=email)
            db.session.add(new_user)
            db.session.commit()
            new_user_json = new_user.to_json_without_password()
            return jsonify({"message": "user added correclty", "user": new_user_json})
        
#recives a json with username and password
@views.route("/login", methods=['POST'])
def login():

    if not login_validator(request.json):
        return jsonify({"error": "request format not valid"}), 400

    username = request.json['username']
    password = request.json['password']
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"error": "incorrect username or password"}), 404

    if check_password_hash(user.password, password):
        login_user(user, remember=True)
        user_json = user.to_json_without_password()
        return jsonify({"message": "user logged in succesully", "user": user_json})
    
    return jsonify({"error": "incorrect username or password"}), 404
    
@views.route("/logout", methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "user logged out succesfully"})

#recives json with title, url and description
@views.route("/add", methods=['POST'])
@login_required
def add_link():

    if not add_link_validator(request.json):
        return jsonify({"error": "request format not valid"}), 400

    links_with_same_title = Link.query.filter_by(title=request.json['title'])
    for link in links_with_same_title:
        if link.user_id == current_user.id:
            return jsonify({"error": "There is already a link with that title"}), 403

    new_link = Link(request.json['title'],request.json['url'],request.json['description'], current_user.id)
    db.session.add(new_link)
    db.session.commit()    
    return jsonify({"message": "Link added succesfully"})

#corregir, all_links no se puede pasar como un json
@views.route("/get_all_links", methods=['GET'])
@login_required
def get_all_links():
    all_links = Link.query.filter_by(user_id = current_user.id)
    #buscar otra manera de hacerlo
    all_links_json = []
    for link in all_links:
        all_links_json.append(link.to_json())
    return jsonify(all_links_json)

#recives json with title 
@views.route("/delete", methods=['DELETE'])
@login_required
def delete_link():

    if not delete_link_validator(request.json):
        return jsonify({"error": "request format not valid"}), 400

    links_witth_same_title = Link.query.filter_by(title=request.json['title'])
    
    if not links_witth_same_title:
        return jsonify({"error": "link not found"}), 404

    for link in links_witth_same_title:
        if link.user_id == current_user.id:
            db.session.delete(link)
            db.session.commit()
            link_json = link.to_json()
            return jsonify({"message": "link deleted succesfully", "link": link_json}) 
    
    return jsonify({"error": "link not found"}), 404

