from functools import wraps
from flask import session, render_template

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'userId' not in session:
            return render_template('401.html')
        return f(*args, **kwargs)
    return decorated_function
