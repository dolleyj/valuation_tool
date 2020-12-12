import json
import requests
from conf import av_api_key, av_url
import pandas as pd


def get_from_av(sym, query_type):
    return requests.get(av_url, params={
        "function": query_type,
        "symbol": sym,
        "apikey": av_api_key
    }).json()

def get_stock_data(sym):
    '''retrieve data from Alpha Vantage: OVERVIEW, BALANCE_SHEET, TIME_SERIES_MONTHLY_ADJUSTED'''
    data = {}
    query_types = []
    data['overview'] = get_from_av(sym, 'OVERVIEW')
    data['income'] = get_from_av(sym, 'INCOME_STATEMENT')['annualReports']
    data['balance'] = get_from_av(sym, 'BALANCE_SHEET')['annualReports']
    data['monthly_quotes'] = get_from_av(sym, 'TIME_SERIES_MONTHLY_ADJUSTED')['Monthly Adjusted Time Series']
    # return data

    overview_data = data['overview']
    overview_data['fair_values'] = {} # NOTE: HISTORICAL FAIR VALUES WILL BE STORED HERE
    historical_data = restructure_data(data)

    # Load data into pandas dataframe 
    df = pd.read_json(json.dumps(historical_data), orient="index", )

    # Drop Years that are missing data 
    # Balance sheets and Income Statements only give 5 yrs data compared to Monthly Quote data
    df = df.dropna(axis=0)
    df = df.replace(["None"], float(0)) #replace all 'None' strings with zeros (0)
    # df

    # Calculate EPS for each year
    # TODO: Need to account for 'None' in preferredStockTotalEquity
    # df["eps"] = round( (df['netIncome'] - df['preferredStockTotalEquity']) / float(df['commonStockSharesOutstanding']), 2)
    df["eps"] = round(df['netIncome'] / df['commonStockSharesOutstanding'], 2)

    # Calculate each yr's PE Ratio and the historical average
    df['peRatio'] = round(df['average_price'] / df['eps'], 2)
    pe_ratios = list(pd.array(df['peRatio']))
    overview_data['historical_peratio'] = round(sum(pe_ratios) / len(pe_ratios), 2)
    print("Average Historical PE Ratio: ", overview_data['historical_peratio'])

    # Calculate average historical price from historical_peratio
    eps_array = list(pd.array(df['eps']))
    pe_ratio_fair_value = overview_data['historical_peratio'] * round(sum(eps_array) / len(eps_array), 2)
    overview_data['fair_values']['pe_ratio'] = pe_ratio_fair_value

    print("\n----- Not sure about these --------")
    print("Current EPS: ", overview_data['EPS'])
    print("Current PERatios: ", overview_data['PERatio'])
    print("Fair Value from Historic PE * Current EPS: ", overview_data['historical_peratio'] * float(overview_data['EPS']))
    print("Current PE * EPS = ", float(overview_data['PERatio']) * float(overview_data['EPS']))
    print("Forward PE * EPS = ", float(overview_data['ForwardPE']) * float(overview_data['EPS']))
    print("-----------------------------------")
    print("\nStock Price from historical PE Ratio: ", overview_data['fair_values']['pe_ratio'])

    # Calculate Average Historical Yield
    # Price = Current annual dividend / yield I want to buy at (Historical Average is this case)
    overview_data['fair_values']['dividend_yield'] = float(overview_data['DividendPerShare']) /  df['dividend_yield'].mean()
    print("\nStock Price from historical Dividend Yield: ", overview_data['fair_values']['dividend_yield'] )

    # PAAY - Percent Above Average Yield (+ undervalued, - overvalued)
    # PAAY = ((Current Yield - Average Yield) / Average Yield) * 100
    print(df['dividend_yield'][:1])
    print("Current Yield: ", overview_data['DividendYield'])
    print("5yr Average Yield: ", df['dividend_yield'][:4].mean())
    paay_long_term = ( float(overview_data['DividendYield']) - df['dividend_yield'][:4].mean() ) / df['dividend_yield'][:4].mean() * 100
    overview_data["5yr_paay"] = round(paay_long_term, 2)

    print("1yr Average Yield: ", df['dividend_yield'][:1].mean())
    paay_short_term = ( float(overview_data['DividendYield']) - df['dividend_yield'][:1].mean() ) / df['dividend_yield'][:1].mean() * 100
    overview_data["1yr_paay"] = round(paay_short_term, 2)
    print("5yr PAAY: ", overview_data['5yr_paay'])
    print("1yr PAAY: ", overview_data['1yr_paay'])


    # Equity value = Market Capitialization = stock price * outstanding shares
    # Enterprise value = [Equity value AKA Market Cap] + Debt + preferred stock - cash and equivalents
    #                    
    # 2 ways to calculate Equity value:
    #   Equity value = stock price * outstanding shares
    #      OR
    #   Equity value = Enterprise value - Debt - preferred stock + cash and equivalents
    df['market_cap'] = df['average_price'] * df['commonStockSharesOutstanding']
    df['enterprise_value'] = df['market_cap'] + df['totalLiabilities'] + pd.to_numeric(df['preferredStockTotalEquity']) - df['cashAndShortTermInvestments']
    # df['equity_value'] = df['market_cap'] + pd.to_numeric(df['preferredStockTotalEquity']) + df['cashAndShortTermInvestments']
    df['equity_value'] = df['enterprise_value'] - df['totalLiabilities'] - pd.to_numeric(df['preferredStockTotalEquity']) + df['cashAndShortTermInvestments']


    # Historical price = Equity Value / Outstanding Shares
    overview_data['fair_values']['equity_value'] = (df['equity_value'] / df['commonStockSharesOutstanding']).mean()
    print("\nStock Price from historical Equity Value (from enterprise value): ", overview_data['fair_values']['equity_value'], " # Seems too low(!?)")

    # Calculate Historical Fair Value (11 years) from:
    # PE Ratio (my addition) - DONE
    # 5-yr average yield - DONE
    # 12-yr median yield - DONE(skip for now. TODO: don't drop NaN rows )
    # Earnings ---> Earnings what? per share??
    # Owner earnings
    # Operating cash flow
    # Free cash flow
    # EBITDA - Can't find formula for this
    # EBIT - Can't find formula for this
    ## Then average these all together
    # TODO TODO TODO was trying to use EBIT as substitute for Market Value (then dividing that by Outstanding Shares)
    print("Historical EBIT: ", df['ebit'].mean()/ df['commonStockSharesOutstanding'].mean())
    print("EBIT / Outstanding shares: ", (df['ebit'] / df['commonStockSharesOutstanding']).mean() )
    print("EBIT/share * Current PE: ", (df['ebit'] / df['commonStockSharesOutstanding']).mean() * float(overview_data['PERatio']) )

    print("\n\nFair Values: ", overview_data['fair_values'])


    # # Calculate share price from Operating Cash Flow
    # # operating_cash_flow = net_income + depreciation - accounts_receivable - accounts_payable
    # df['operating_cash_flow'] = df['netIncome'] + df['accumulatedDepreciation'] - (df['accountsPayable'] + df['netReceivables'])
    # print(df['accumulatedDepreciation'])
    # print(df['operating_cash_flow']) # TODO WHY IS 2017 -10061999999 ????


    # # calculate equity value from EV/EBITDA
    # # https://www.wallstreetoasis.com/forums/evebidta-to-target-price#:~:text=With%20the%20EV%2FEBITDA%20multiple,the%20equity%20value%20per%20share.
    # enterprise_value = float(data['overview']['EVToEBITDA']) * float(data['overview']['EBITDA'])
    # total_debt = float(data['annual_reports'][0]['shortTermDebt']) + float(data['annual_reports'][0]['longTermDebt'])
    # equity_value = float(enterprise_value) - float(total_debt)
    # share_price = round(float(equity_value) / float(data['overview']['SharesOutstanding']), 2)
    # print("SHARE PRICE from EBITDA: ", share_price) # NOTE: SEEMS TO BE CURRENT YEAR. 

    # #TODO: Calculate share price from EBITDA for past 11-yrs

    return overview_data


def format_monthly_quote(quote):
    # Removes the prefix number and converts values to int
    # "1. open": "59.9100"
    formatted = {}
    for key in quote:
        cleaned_key = key.split(". ")[1]              # Remove the "1. "
        cleaned_key = cleaned_key.replace(" ", "_") # Replace spaces with "_"
        formatted[cleaned_key] = float(quote[key])    # Convert values to numbers
    return formatted

def restructure_data(data):
    '''
    Flattens the JSON structure
    1. Reduces monthly quotes to last month of each year,
    2. Combines balance sheets, income statements, and monthly quotes into a single dictionary 
       {'2019-12-31': {balance_sheet, income_statement, monthly_quote}, ...}
    '''
    final_data = {}

    # Gathers the monthly stock prices (Groups by year YYYY)
    monthly_close_prices = {}
    yearly_dividend_amounts = {}
    for date in data['monthly_quotes']:
        current_year = date.split("-")[0]
        cleaned_quote = format_monthly_quote(data['monthly_quotes'][date])
        if current_year not in monthly_close_prices:
            monthly_close_prices[current_year] = []
            yearly_dividend_amounts[current_year] = []
        monthly_close_prices[current_year].append(cleaned_quote['close'])

        if cleaned_quote['dividend_amount'] > 0:
            yearly_dividend_amounts[current_year].append(cleaned_quote['dividend_amount'])
    
    # Calculate the average stock price for each year
    for year in monthly_close_prices.keys():
        year_avg_price = round(sum(monthly_close_prices[year]) / len(monthly_close_prices[year]), 2)
        # print("Average price for ", year, ": ", year_avg_price)
        final_data[year] = {"average_price": year_avg_price}

    # Calculate each year's dividend amount and yield
    for year in yearly_dividend_amounts.keys():
        year_dividend_paid = sum(yearly_dividend_amounts[year])
        year_dividend_yield = round(year_dividend_paid / final_data[year]['average_price'], 4)
        final_data[year]["dividend_amount"] = year_dividend_paid
        final_data[year]["dividend_yield"] = year_dividend_yield

    # Add the balance sheet and income statement for each year to final
    for balance, income in list(zip(data['balance'], data['income'])):
        if balance['fiscalDateEnding'] == income['fiscalDateEnding']:
            current_year = balance['fiscalDateEnding'].split("-")[0]
            financials = {**balance, **income}
            final_data[current_year].update(financials)


    return final_data

