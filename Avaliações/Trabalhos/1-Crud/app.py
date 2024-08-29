from flask import Flask, request, render_template, session, redirect
from env_vars import API_SECRET_KEY
import bcrypt
import db_connect as db
from auth.decorators import login_required

app = Flask(__name__)
app.secret_key = API_SECRET_KEY
app.config['SESSION_PERMANENT'] = True

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def index():
    if 'userId' in session:
        return redirect('/home')
    return redirect('/login')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return render_template('login.html')
        
        user = db.getUserByUsername(username)
        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                session['userId'] = user['id']
                session['username'] = user['username']
                session['name'] = user['name']
                return redirect('/')
            
    return render_template('login.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')

        if not username or not password or not name:
            return render_template('register.html')

        response = db.createUser(username, password, name)
        if response:
            return redirect('/login')
    
    return render_template('register.html')

@app.post('/logout')
@login_required
def logout():
    del session['userId']
    del session['username']
    del session['name']
    return redirect('/')

@app.get('/home')
@login_required
def home():
    works = db.getWorks()
    courses = db.getCourses()
    return render_template('index.html', works=works, courses=courses)

@app.get('/dashboard')
@login_required
def dashboard():
    works = db.getWorksByUserId(session['userId'])
    return render_template('dashboard.html', works=works)

@app.route('/works/create', methods = ['GET', 'POST'])
@login_required
def createWork(): 
    if request.method == 'POST':
        authorId = session['userId']
        courseId = request.form.get('course')
        title = request.form.get('title')
        description = request.form.get('description')
        price = request.form.get('price')

        if authorId and courseId and title and description and price:
            if db.createWork(courseId, authorId, title, description, price):
                return redirect('/dashboard')
    
    courses = {course['id']: course['title'] for course in db.getCourses()}
    return render_template('work-create.html',  courses=courses)

@app.route('/works/update/<id>', methods = ['GET', 'POST'])
@login_required
def updateWork(id):
    work = db.getWorkById(id)
    
    if work == None:
        return render_template('404.html')
    
    if work['author'] != session['username']:
        print(work['author'], session['username'])
        return render_template('403.html')
    
    if request.method == 'POST':
        authorId = session['userId']
        courseId = request.form.get('course')
        title = request.form.get('title')
        description = request.form.get('description')
        price = request.form.get('price')

        if authorId and courseId and title and description and price:
            if db.updateWork(id, title, courseId, description, price):
                return redirect('/dashboard')

    courses = {course['id']: course['title'] for course in db.getCourses()}
    return render_template('work-edit.html', id=id, work=work, courses=courses)

@app.get('/works/delete/<id>')
@login_required
def deleteWork(id):
    work = db.getWorkById(id)
    if work['author'] != session['username']:
        return render_template('403.html')
    
    db.deleteWork(id)
    return redirect('/dashboard')


@app.get('/users')
def getUsers():
    return db.getUsers()

@app.get('/courses')
def getCourses():
    return db.getCourses()

@app.get('/works')
def getWorks():
    return db.getWorks()

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
