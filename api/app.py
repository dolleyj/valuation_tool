from flask import make_response, jsonify, render_template, request
from flask import Flask

import json
from conf import be_loc, be_port,av_api_key
import utils


app = Flask(__name__, template_folder="templates")
app.debug = True


@app.route('/')
def hello_world():
    print('\n\nHELLO WORLD')
    # return 'Hello, World!'
    return render_template('index.html')

@app.route('/api/get_stock_info')
def get_stock_info():
    # STOCK_SYMBOL = "INTC"
    symbol = request.args.get("symbol")
    print("symbol: ", symbol)
    data = None
    data = utils.get_stock_data(symbol)

    # print(json.dumps(data, indent=2, sort_keys=True))
    print(json.dumps(data, indent=2))
    return make_response(jsonify(data))


if __name__ == '__main__':
    extra_files = [
        './utils.py',
        './db_utils.py',
        './static/js/index.js',
        './templates/index.html'
    ]
    app.run(host=be_loc, port=int(be_port), extra_files=extra_files)