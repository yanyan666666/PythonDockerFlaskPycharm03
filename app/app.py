from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'faithfuldata'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Faithful Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM faithfultable')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, times=result)


@app.route('/view/<int:eruption_id>', methods=['GET'])
def record_view(eruption_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM faithfultable WHERE id=%s', eruption_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', time=result[0])


@app.route('/edit/<int:eruption_id>', methods=['GET'])
def form_edit_get(eruption_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM faithfultable WHERE id=%s', eruption_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', time=result[0])


@app.route('/edit/<int:eruption_id>', methods=['POST'])
def form_update_post(eruption_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('eruptLgth'), request.form.get('eruptWait'), eruption_id)
    sql_update_query = """UPDATE faithfultable t SET t.Eruption_length = %s, t.Eruption_wait = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/times/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Eruption Time Form')


@app.route('/times/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('id'), request.form.get('eruptLgth'), request.form.get('eruptWait'))
    sql_insert_query = """INSERT INTO faithfultable (id, Eruption_length, Eruption_wait) VALUES (%s, %s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/delete/<int:eruption_id>', methods=['POST'])
def form_delete_post(eruption_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM faithfultable WHERE id = %s """
    cursor.execute(sql_delete_query, eruption_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/times', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM faithfultable')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/times/<int:eruption_id>', methods=['GET'])
def api_retrieve(eruption_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM faithfultable WHERE id=%s', eruption_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/times/', methods=['POST'])
def api_add() -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/times/<int:eruption_id>', methods=['PUT'])
def api_edit(eruption_id) -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/times/<int:eruption_id>', methods=['DELETE'])
def api_delete(eruption_id) -> str:
    resp = Response(status=210, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)