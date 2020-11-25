from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'citiesData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Cities Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblCities')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, cities=result)


@app.route('/view/<int:Id>', methods=['GET'])
def record_view(Id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblCities WHERE Id=%s', Id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', city=result[0])


@app.route('/edit/<int:Id>', methods=['GET'])
def form_edit_get(Id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblCities WHERE Id=%s', Id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', city=result[0])


@app.route('/edit/<int:Id>', methods=['POST'])
def form_update_post(Id):
    cursor = mysql.get_db().cursor()
    input_data = (request.form.get('LatD'), request.form.get('LatM'), request.form.get('LatS'), request.form.get('NS')
                 , request.form.get('LonD'), request.form.get('LonM'), request.form.get('LonS'), request.form.get('EW')
                 , request.form.get('City'), request.form.get('State'), Id)
    sql_update_query = """UPDATE tblCities t 
                            SET t.LatD = %s, t.LatM = %s, t.LatS = %s, t.NS = %s
                            , t.LonD = %s, t.LonM = %s, t.LonS = %s, t.EW = %s
                            , t.City = %s, t.State = %s
                            WHERE t.Id = %s """
    cursor.execute(sql_update_query, input_data)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/cities/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New City Form')


@app.route('/cities/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('LatD'), request.form.get('LatM'), request.form.get('LatS'), request.form.get('NS')
                 , request.form.get('LonD'), request.form.get('LonM'), request.form.get('LonS'), request.form.get('EW')
                 , request.form.get('City'), request.form.get('State'))
    sql_insert_query = """INSERT INTO tblCities (LatD,LatM,LatS,NS,LonD,LonM,LonS,EW,City,State) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:Id>', methods=['POST'])
def form_delete_post(Id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblCities WHERE Id = %s """
    cursor.execute(sql_delete_query, Id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/cities', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblCities')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/cities/<int:Id>', methods=['GET'])
def api_retrieve(Id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblCities WHERE Id=%s', Id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/cities/', methods=['POST'])
def api_add() -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/cities/<int:Id>', methods=['PUT'])
def api_edit(Id) -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/cities/<int:Id>', methods=['DELETE'])
def api_delete(Id) -> str:
    resp = Response(status=210, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)