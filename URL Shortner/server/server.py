from flask import Flask, jsonify, request, abort, redirect, render_template
from flask_cors import CORS
import base64
import sqlite3

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

def get_url_by_id(id):
    '''
        return the url based on the id
    '''
    with sqlite3.connect("url.db") as conn:
        cursor = conn.cursor()
        parameters = (id,)
        cursor.execute('''select url from url where rowid=?''', parameters)
        return cursor.fetchone()[0]

def get_url_data(url_id):
    '''
        Get all the visitor data associated with a perticular URL
    '''
    with sqlite3.connect("url.db") as conn:
        cursor = conn.cursor()
        parameters = (url_id,)
        cursor.execute('''select ip, platform, browser, timestamp from visitor_data where url_id=?''', parameters)
        return cursor.fetchall()

def insert_url(url):
    '''
        Save the new url to the database
    '''
    with sqlite3.connect("url.db") as conn:
        cursor = conn.cursor()
        parameters = (url,)
        cursor.execute('''Insert into url (url) values (?)''', parameters)
        conn.commit()
        return cursor.lastrowid

def insert_visitor(url_id, ip, platform, browser):
    '''
        Save visitor information to the database
    '''
    with sqlite3.connect("url.db") as conn:
        cursor = conn.cursor()
        parameters = (url_id, ip, platform, browser)
        cursor.execute('''Insert into visitor_data (url_id, ip, platform, browser, timestamp) values (?,?,?,?,datetime('now'))''', parameters)
        conn.commit()
        return cursor.lastrowid

@app.route('/api/', methods=['POST'])
def get_encoded_url():
    '''
        Accepts a POST request from the /api/ endpoint. 
        the request must be json and contain an element called 'url'
        It inserts the url to the database and returns the rowid for the new row. 
        The rowid is returned as a base64 encoded string. (acting as the shortened url)
        This avoids the need for having an algorithm that shortens the url and all issues associated 
        with sed algorithm (i.e. checking for duplicates, issues with distributed deployments and so on)
    '''
    if not request.json or 'url' not in request.json:
        abort(400)
    url = request.json['url']
    url_id = insert_url(url)
    return jsonify({'url': base64.urlsafe_b64encode(str(url_id))})

@app.route('/<encoded_url>', methods=['GET'])
def get_decoded_url(encoded_url):
    '''
        Accepts a GET request for a shortened url. 
        It decodes the base64 string and looks it up in the database
        If found, it will save the visitor information and redirect the visitor to the URL
    '''
    try:
        id = base64.urlsafe_b64decode(encoded_url.encode("ascii"))
        result = get_url_by_id(id)
        if result:
            insert_visitor(id, request.remote_addr, request.user_agent.platform, request.user_agent.browser)
            if 'http' not in result:
                result = 'http://' + result
            return redirect(result, code=302)
        else: 
            abort(404)
    except Exception as e:
        print(e)
        abort(404)

@app.route('/stats/<encoded_url>', methods=['GET'])
def get_url_stats(encoded_url):
    '''
        Accepts a GET request for a shortened url on the /stats/ endpoint. 
        It decodes the base64 string and looks it up in the database
        If found, it loads up the data for the visitors to the URL and renders the 'stats.html' page with the data. 
    '''
    try:
        id = base64.urlsafe_b64decode(encoded_url.encode("ascii"))
        url = get_url_by_id(id)
        data = get_url_data(id)
        if url:
            return render_template("stats.html", data=data, url=url)
        else:
            abort(404)
    except Exception as e:
        print(e)
        abort(404)

@app.route('/api/', methods=['GET'])
@app.route('/<encoded_url>', methods=['POST'])
@app.route('/', methods=['GET', 'POST'])
def bad_request():
    abort(400)

if __name__ == '__main__':
    app.run()
