import requests
import json
import xlsxwriter

local_currency = 'USD'
local_symbol = '$'

api_key = 'f786a962-2c29-44af-b6b6-515328a96cd9'
headers = {'X-CMC_PRO_API_KEY': api_key}

base_url = 'https://pro-api.coinmarketcap.com'

crypto_workbook = xlsxwriter.Workbook('Cryptocurrencies.xlsx')
crypto_sheet = crypto_workbook.add_worksheet()

crypto_sheet.write('A1', 'Name')
crypto_sheet.write('B1', 'Symbol')
crypto_sheet.write('C1', 'Market Cap')
crypto_sheet.write('D1', 'Price')
crypto_sheet.write('E1', '24H Volume')
crypto_sheet.write('F1', 'Hour Change')
crypto_sheet.write('G1', 'Day Change')
crypto_sheet.write('H1', 'Week Change')

start = 1
row = 1

for i in range(10):
    listings_url = base_url + '/v1/cryptocurrency/listings/latest?convert=' + local_currency + '&start=' + str(start)

    request = requests.get(listings_url, headers=headers)
    results = request.json()

    data = results['data']

    for currency in data:
        name = currency['name']
        symbol = currency['symbol']

        quote = currency['quote'][local_currency]
        market_cap = quote['market_cap']
        hour_change = quote['percent_change_1h']
        day_change = quote['percent_change_24h']
        week_change = quote['percent_change_7d']
        price = quote['price']
        volume = quote['volume_24h']

        volume_string = '{:,}'.format(volume)
        market_cap_string = '{:,}'.format(market_cap)

        crypto_sheet.write(row,0, name)
        crypto_sheet.write(row,1, symbol)
        crypto_sheet.write(row,2, local_symbol + market_cap_string)
        crypto_sheet.write(row,3, local_symbol + str(price))
        crypto_sheet.write(row,4, local_symbol + volume_string)
        crypto_sheet.write(row,5, str(hour_change) + '%')
        crypto_sheet.write(row,6, str(day_change) + '%')
        crypto_sheet.write(row,7, str(week_change) + '%')

        row = row + 1

    start = start + 100

crypto_workbook.close()