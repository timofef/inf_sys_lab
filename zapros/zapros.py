from DBCM import UseDatabase
from flask import render_template, request, Blueprint, current_app
from check_auth import check_access

zapros_blueprint = Blueprint('zapros_blueprint', __name__, template_folder='templates')

@zapros_blueprint.route('/', methods=['GET', 'POST'])
@check_access("2")
def input():
    if 'send' in request.form and request.form['send'] == 'send':
        data = request.form.get('department')
        if data:
            with UseDatabase(current_app.config['dbconfig']["Worker"]) as cursor:
                workers = get_workers(cursor, data)
            return render_template('results.html', workers=workers)
        else:
            return render_template('input.html')
    else:
        return render_template('input.html')


def get_workers(cursor, data):
    SQL = f"select name from worker where department_number = {data}"
    cursor.execute(SQL)
    result = cursor.fetchall()
    res = []
    schema = ['name']
    for row in result:
        res.append(dict(zip(schema, row)))
    return res