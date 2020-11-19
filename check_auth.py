from functools import wraps
from flask import session, abort, request, current_app, render_template

def check_query_access(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session['user_group'] != "Worker":
            return render_template('access_denied.html', needed="Worker")
        else:
            return func(*args,**kwargs)
    return wrapper
