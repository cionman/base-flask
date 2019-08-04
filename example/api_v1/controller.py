from flask import jsonify, request, render_template
from flask_jwt import jwt_required

from models import Fcuser, db
from . import api


@api.route('/users', methods=['GET'])
@jwt_required()
def users():
    users = Fcuser.query.all()
    return jsonify([user.serialize for user in users])


@api.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    userid = data.get('userid')
    username = data.get('username')
    password = data.get('password')
    re_password = data.get('re_password')
    if not (userid and username and password and re_password):
        return jsonify({'error': 'No arguments'}), 400
    if password != re_password:
        return jsonify({'error': 'Wrong password'}), 400
    fcuser = Fcuser()
    fcuser.userid = userid
    fcuser.username = username
    fcuser.password = password
    db.session.add(fcuser)

    return jsonify(), 201


@api.route('/users/<uid>', methods=['GET', 'PUT', 'DELETE'])
def user_detail(uid):
    if request.method == 'GET':
        user = Fcuser.query.filter(Fcuser.id == uid).first()
        return jsonify(user.serialize)
    elif request.method == 'DELETE':
        Fcuser.query.filter(Fcuser.id == uid).delete()
        return jsonify(), 204  # NO CONTENT
    elif request.method == 'PUT':
        data = request.get_json()
        user = Fcuser.query.filter(Fcuser.id == uid)
        user.update(data)
        return jsonify(user.first().serialize)


@api.route('/test_register')
def test_register():
    return render_template('register.html')


@api.route('/test_login')
def test_login():
    return render_template('login.html')


@api.route('/home')
def home():
    return render_template('home.html')
