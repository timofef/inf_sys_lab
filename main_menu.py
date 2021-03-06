import json
from flask import Flask, render_template, request, redirect, url_for, session
from zapros.zapros import zapros_blueprint
from auth.auth import auth_blueprint
from purchase.purchase import purchase_blueprint


with open('data_files/menu_config.json', 'r') as conf:
    main_menu = json.load(conf)
with open('data_files/db_config.json', 'r') as db:
    dbconfig = json.load(db)
with open('data_files/query_access.json', encoding='utf-8') as f:
    query_access_items = json.load(f)

app = Flask(__name__)
app.secret_key = "BRUH"
app.config['dbconfig'] = dbconfig
app.config['query_access'] = query_access_items

app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(zapros_blueprint, url_prefix='/request1')
app.register_blueprint(purchase_blueprint, url_prefix='/purchase')


@app.route('/menu/')
def menu():
    if 'user_group' not in session:
        session['user_group'] = 'Guest'

    route_mapping = {'1': url_for('auth_blueprint.authorization'),
                     '2': url_for('zapros_blueprint.input'),
                     '3': url_for('purchase_blueprint.purchase')}
    point = request.args.get('point')
    if point is None:
        return render_template('main_menu.html', menu=main_menu, user_group=session['user_group'])
    elif point in route_mapping:
        print(route_mapping[point])
        return redirect(route_mapping[point])
    else:
        session['user_group'] = 'Guest'
        return render_template('main_menu.html', menu=main_menu, user_group=session['user_group'])


app.run(host='127.0.0.1', port=5001, debug=True)
