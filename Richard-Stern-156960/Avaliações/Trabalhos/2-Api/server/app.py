from flask import Flask, request, jsonify, session
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from datetime import timedelta
from flask_cors import CORS
import bcrypt
from env_vars import API_SECRET_KEY
import db_connect as db

app = Flask(__name__)
app.secret_key = API_SECRET_KEY
app.config['SECRET_KEY'] = 'your_strong_secret_key'
app.config["JWT_SECRET_KEY"] = 'your_jwt_secret_key'
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

jwt = JWTManager(app)

CORS(app, supports_credentials=True)

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'error': 'Not found'}), 404

@app.route('/')
def index():
    if 'userId' in session:
        return jsonify({'message': 'User logged'}), 200
    return jsonify({'message': 'Please log in'}), 401

@app.post('/login')
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    user = db.getUserByUsername(username)
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        additional_claims = {"username": user['username']}
        access_token = create_access_token(identity=user['id'], additional_claims=additional_claims)
        return jsonify({'access_token': access_token})
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.post('/register')
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    name = request.json.get('name')

    if not username or not password or not name:
        return jsonify({'error': 'All fields are required'}), 400

    response = db.createUser(username, password, name)
    if response:
        return jsonify({'message': 'User created successfully'}), 201
    
    return jsonify({'error': 'User could not be created'}), 500

@app.get('/dashboard')
@jwt_required()
def dashboard():
    works = db.getWorksByUserId(get_jwt_identity())
    return jsonify(works)

@app.post('/works')
@jwt_required()
def createWork():
    authorId = get_jwt_identity()
    courseId = request.json.get('course')
    title = request.json.get('title')
    description = request.json.get('description')
    price = request.json.get('price')

    if authorId and courseId and title and description and price:
        if db.createWork(courseId, authorId, title, description, price):
            return jsonify({'message': 'Work created successfully'}), 201
    
    return jsonify({'error': 'Missing required fields'}), 400

@app.get('/works/<id>')
@jwt_required()
def getWork(id):
    work = db.getWorkById(id)

    if work == None:
        return jsonify({'error': 'Work not found'}), 404

    return jsonify(work), 200

@app.route('/works/<id>', methods=['PUT'])
@jwt_required()
def updateWork(id):
    work = db.getWorkById(id)
    
    if work == None:
        return jsonify({'error': 'Work not found'}), 404
    
    if work['author'] != get_jwt()['username']:
        return jsonify({'error': 'Forbidden'}), 403
    
    authorId = get_jwt_identity()
    courseId = request.json.get('course')
    title = request.json.get('title')
    description = request.json.get('description')
    price = request.json.get('price')

    if authorId and courseId and title and description and price:
        if db.updateWork(id, title, courseId, description, price):
            return jsonify({'message': 'Work updated successfully'})
    
    return jsonify({'error': 'Missing required fields'}), 400

@app.delete('/works/<id>')
@jwt_required()
def deleteWork(id):
    work = db.getWorkById(id)
    if work['author'] != get_jwt()['username']:
        return jsonify({'error': 'Forbidden'}), 403
    
    db.deleteWork(id)
    return jsonify({'message': 'Work deleted successfully'})

@app.get('/users')
@jwt_required()
def getUsers():
    users = db.getUsers()
    return jsonify(users)

@app.get('/courses')
@jwt_required()
def getCourses():
    courses = db.getCourses()
    return jsonify(courses)

@app.get('/works')
@jwt_required()
def getWorks():
    works = db.getWorks()
    return jsonify(works)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
