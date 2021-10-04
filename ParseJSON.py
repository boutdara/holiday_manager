from datetime import datetime
from bs4 import BeautifulSoup
import requests
import json

# Get data from URL
def getHTML(website_url):
    response = requests.get(website_url)
    return response.text
    print(response)

# Append to holidays.json
def write_json(new_data, filename = 'holidays.json'):
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        file_data["holidays"].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent = 3)

# Parse data
def yearly_holidays(website_url, year):
    html = getHTML(website_url)

    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', attrs = {'id':'holidays-table'})
    table_body = table.find('tbody')

    all_holidays = []

    rows = table_body.find_all('tr')
    for row in rows:
        name_cells = row.find_all_next('td')
        date_cells = row.find_all_next('th')
        date_conv = datetime.strptime(date_cells[0].string, '%b %d')
        holiday = {}
        holiday['name'] = name_cells[1].string
        holiday['date'] = date_conv.strftime('{}-%m-%d'.format(year))
        all_holidays.append(holiday)
    
    filtered_holidays = [] # Remove most duplicate holidays
    for i in all_holidays:
        if i not in filtered_holidays:
            filtered_holidays.append(i)

    write_json(filtered_holidays)

# Only 2021-2023 are used because I kept getting "ValueError: day is out of range for month for 2020 and 2024"
yearly_holidays('https://www.timeanddate.com/holidays/us/2021?hol=33554809', 2021) #2021 Holidays and Observances in the US
yearly_holidays('https://www.timeanddate.com/holidays/us/2022?hol=33554809', 2022) #2022 Holidays and Observances in the US
yearly_holidays('https://www.timeanddate.com/holidays/us/2023?hol=33554809', 2023) #2023 Holidays and Observances in the US