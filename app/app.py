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


@app.route('/api/v1/cities', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblCities order by Id desc')
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


@app.route('/api/v1/cities', methods=['POST'])
def api_add() -> str:
    content = request.json
    cursor = mysql.get_db().cursor()
    inputData = (content['LatD'], content['LatM'], content['LatS'], content['NS']
                 , content['LonD'], content['LonM'], content['LonS'], content['EW']
                 , content['City'], content['State'])
    sql_insert_query = 'INSERT INTO tblCities (LatD,LatM,LatS,NS,LonD,LonM,LonS,EW,City,State) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/cities/<int:Id>', methods=['PUT'])
def api_edit(Id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['LatD'], content['LatM'], content['LatS'], content['NS']
                 , content['LonD'], content['LonM'], content['LonS'], content['EW']
                 , content['City'], content['State'], Id)
    sql_update_query = """UPDATE tblCities t 
                            SET t.LatD = %s, t.LatM = %s, t.LatS = %s, t.NS = %s
                            , t.LonD = %s, t.LonM = %s, t.LonS = %s, t.EW = %s
                            , t.City = %s, t.State = %s
                            WHERE t.Id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/cities/<int:Id>', methods=['DELETE'])
def api_delete(Id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblCities WHERE id = %s """
    cursor.execute(sql_delete_query, Id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)