from flask import make_response, jsonify, render_template, request
from flask import Flask, Response

import json
from conf import be_loc, be_port,av_api_key
import db_utils
import utils


app = Flask(__name__, template_folder="templates")
app.debug = True


@app.route('/')
def hello_world():
    print('\n\nHELLO WORLD')
    # return 'Hello, World!'
    return render_template('index.html')


@app.route('/api/delete_stock')
def delete_stock():
    symbol = request.args.get("symbol")
    print("Inside delete_stock! symbol: ", symbol)

    success = db_utils.delete_stock(symbol)

    data = {"success": success}
    return make_response(jsonify(data))


@app.route('/api/get_stock_info')
def get_stock_info():
    symbol = request.args.get("symbol")
    print("symbol: ", symbol)
    stock_data = None
    stock_data = utils.get_stock_data(symbol)

    # save stock in database
    if stock_data is not None:
        save_successful = db_utils.save_to_db(stock_data)
        print("Stock saved to database: ", save_successful)

    # TODO - Not currently being used. headers are currently hardcorded in index.html
    table_headers = [
        {"human_readable": "Symbol", "name": "symbol"},
        # {"human_readable": "Name", "name": "name"},
        # {"human_readable": "Sector", "name": "sector"},
        {"human_readable": "Current PE", "name": "pe_ratio"},
        {"human_readable": "Current EPS", "name": "eps"},
        {"human_readable": "Current PEG", "name": "peg_ratio"},
        {"human_readable": "Historical PE", "name": "historical_peratio"},
        {"human_readable": "Analyst Target Price", "name": "analyst_target_price"},
        {"human_readable": "FV - Historical PE", "name": "fair_value_from_historical_pe_ratio"},
        {"human_readable": "FV - Historical PE & current EPS", "name": "fair_value_from_historical_pe_ratio_current_eps"},
        {"human_readable": "FV - Fwd PE & Target Price", "name": "fair_value_from_fwd_pe_ratio_analyst_target_price"},
        {"human_readable": "FV - Equity Value", "name": "fair_value_from_equity_value"},
        {"human_readable": "FV - Dividend Yield", "name": "fair_value_from_dividend_yield"},
        {"human_readable": "1 Yr PAAY", "name": "1yr_paay"},
        {"human_readable": "5 Yr PAAY", "name": "5yr_paay"},
        {"human_readable": "Dividend Yield", "name": "forward_annual_dividend_yield"},
        {"human_readable": "Dividend Rate", "name": "forward_annual_dividend_rate"}
        # {"human_readable": "Ex-Dividend Date", "name": "ex_dividend_date"},
        # {"human_readable": "Dividend Date", "name": "dividend_date"}
    ]

    data = {"table_headers": table_headers, "stock": stock_data}
    # print(json.dumps(data, indent=2))
    return make_response(jsonify(data))


@app.route('/api/get_stored_stocks')
def get_stored_stocks():
    data = None
    stocks = None
    stocks = db_utils.get_all_stocks()
    print(stocks)

    # TODO - Not currently being used. headers are currently hardcorded in index.html
    table_headers = [
        {"human_readable": "Symbol", "name": "symbol"},
        # {"human_readable": "Name", "name": "name"},
        # {"human_readable": "Sector", "name": "sector"},
        {"human_readable": "Current PE", "name": "pe_ratio"},
        {"human_readable": "Current EPS", "name": "eps"},
        {"human_readable": "Current PEG", "name": "peg_ratio"},
        {"human_readable": "Historical PE", "name": "historical_peratio"},
        {"human_readable": "Analyst Target Price", "name": "analyst_target_price"},
        {"human_readable": "FV - Historical PE", "name": "fair_value_from_historical_pe_ratio"},
        {"human_readable": "FV - Historical PE & current EPS", "name": "fair_value_from_historical_pe_ratio_current_eps"},
        {"human_readable": "FV - Fwd PE & Target Price", "name": "fair_value_from_fwd_pe_ratio_analyst_target_price"},
        {"human_readable": "FV - Equity Value", "name": "fair_value_from_equity_value"},
        {"human_readable": "FV - Dividend Yield", "name": "fair_value_from_dividend_yield"},
        {"human_readable": "1 Yr PAAY", "name": "1yr_paay"},
        {"human_readable": "5 Yr PAAY", "name": "5yr_paay"},
        {"human_readable": "Dividend Yield", "name": "forward_annual_dividend_yield"},
        {"human_readable": "Dividend Rate", "name": "forward_annual_dividend_rate"}
        # {"human_readable": "Ex-Dividend Date", "name": "ex_dividend_date"},
        # {"human_readable": "Dividend Date", "name": "dividend_date"}
    ]

    data = {"table_headers": table_headers, "stocks": stocks}
    return make_response(jsonify(data))


if __name__ == '__main__':
    extra_files = [
        './utils.py',
        './db_utils.py',
        './static/js/index.js',
        './templates/index.html'
    ]
    app.run(host=be_loc, port=int(be_port), extra_files=extra_files)
