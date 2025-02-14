import os
import csv
import sys
import json
import time
import requests
import datetime
import pyttsx3

local_currency = 'USD'
local_symbol = '$'

api_key = 'f786a962-2c29-44af-b6b6-515328a96cd9'
headers = {'X-CMC_PRO_API_KEY': api_key}

base_url = 'https://pro-api.coinmarketcap.com'

print()
print('$$$$$$$$$$$$$$ ALERTS TRACKING $$$$$$$$$$$$$$')
print()

already_hit_symbols = []

while True:
    with open('my_alerts.csv','r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            if '\ufeff' in line[0]:
                line[0] = line[0][1:].upper()
            else:
                line[0] = line[0].upper()
            symbol = line[0]
            amount = line[1]

            quote_url = base_url + '/v1/cryptocurrency/quotes/latest?convert=' + local_currency + '&symbol=' + symbol

            request = requests.get(quote_url, headers=headers)
            results = request.json()

            currency = results['data'][symbol]

            name = currency['name']
            price = currency['quote'][local_currency]['price']

            if float(price) >= float(amount) and symbol not in already_hit_symbols:
                os.system('PowerShell -Command "Add-Type –AssemblyName System.Speech; (New-Object '
                          'System.Speech.Synthesis.SpeechSynthesizer).Speak(\'ALERT ALERT ALERT\');"')
                os.system(f'PowerShell -Command "Add-Type –AssemblyName System.Speech; (New-Object '
                          f'System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{name} hit {amount}\');"')
                sys.stdout.flush()

                now = datetime.datetime.now()
                current_time = now.strftime("%I:%M %p")
                print(name + ' hit ' + amount + ' at ' + current_time + '!')
                already_hit_symbols.append(symbol)
    print('...')
    time.sleep(10)