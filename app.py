from __future__ import absolute_import
from flask import Flask, request, jsonify
import requests
import os
from coupondunia import search_page
from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

app = Flask(__name__, static_folder='static', static_url_path='')
app.requests_session = requests.Session()
app.secret_key = os.urandom(24)

@app.route('/search', methods=['GET'])
def search():
    try:
        search_string = request.args.get('search')
        if not search_string:
            return jsonify({'status': False})
        val = cache.get(search_string)
        if val is None:
            print "calling api"
            data = search_page(search_string)
            print data
            cache.set(search_string, str(data))
        else:
            print "using cache"
            data = eval(val)
        return_data = {}
        return_data['status'] = True
        return_data['data'] = data
        return jsonify(return_data)
    except Exception, excpt:
        print excpt
        return jsonify({'status': False})

if __name__ == '__main__':
    app.debug = os.environ.get('FLASK_DEBUG', True)
    app.run(port=7000)
