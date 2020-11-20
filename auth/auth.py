from flask import Blueprint, redirect, render_template, abort, session, request, current_app
import json
from DBCM import UseDatabase
from check_auth import check_access

auth_blueprint = Blueprint('auth_blueprint', __name__, template_folder='templates')


@auth_blueprint.route('/', methods=['GET', 'POST'])
def authorization():
    if 'send' in request.form and request.form['send'] == 'auth':
        result = []
        login = request.form.get('login')
        password = request.form.get('password')
        print(login)
        print(password)
        if login and password:
            with UseDatabase(current_app.config['dbconfig']['Guest']) as cursor:
                cursor.execute("""SELECT role 
                                  FROM lab1.user_groups
                                  WHERE login='%s'
                                  AND password='%s'""" % (login, password))
                schema = ['user_group']
                for con in cursor.fetchall():
                    result.append(dict(zip(schema, con)))
            if len(result) > 0:
                session['user_group'] = result[0]['user_group']
                return redirect('/menu')
            else:
                return render_template('auth.html')
    else:
        return render_template('auth.html')