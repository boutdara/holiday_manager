from bs4 import BeautifulSoup
from datetime import datetime, date, time, timedelta
from isoweek import Week
import json
import inspect
import requests

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

#Create class for holidays
class Holiday:
    def __init__(self, name, date):
        self.name = name
        self.date = date

    def __str__(self):
        return '{} ({})'.format(self.name, self.date)

    def __repr__(self):
        return '{} ({})'.format(self.name, self.date)

# Load holidays JSON
holidays_list = []
holiday_json = ''

with open('holidays.json') as f:
    holiday_json = json.load(f)
for day in holiday_json['holidays']:
    hol_name = day['name']
    hol_date = day['date']
    one_holiday = Holiday(hol_name, hol_date)
    holidays_list.append(one_holiday)

#Create class for weather
class Weather:
    def __init__(self, wdate, forecast):
        self.wdate = wdate
        self.forecast = forecast

    def __str__(self):
        return '{}: {}'.format(self.wdate, self.forecast)

    def __repr__(self):
        return '{}: {}'.format(self.wdate, self.forecast)

# Load weather JSON
weather_list = []

# Open API from the NWS with forecast in Milwaukee
response = requests.get('https://api.weather.gov/gridpoints/TOP/87,64/forecast')
weather = response.json()['properties']['periods']

# Filter the dictionary
weather = [x for x in weather if x['isDaytime'] is True]
for key in weather:
    key['startTime'] = key['startTime'].replace('T06:00:00-05:00', '').replace('T11:00:00-05:00', '')
    del key['number']
    del key['name']
    del key['endTime']
    del key['isDaytime']
    del key['temperature']
    del key['temperatureUnit']
    del key['temperatureTrend']
    del key['windSpeed']
    del key['windDirection']
    del key['icon']
    del key['detailedForecast']

# I know this is ugly but Python wasn't allowing me to do what I wanted:
# remove = ['number', 'name', 'endTime', 'isDaytime', 'temperature', 'temperatureUnit', 'temperatureTrend', 'windSpeed', 'windDirection', 'icon', 'detailedForecast']
# for key in remove:
    # del weather[key]

for d in weather:
    wea_date = d['startTime']
    wea_forecast = d['shortForecast']
    one_weather = Weather(wea_date, wea_forecast)
    weather_list.append(one_weather)

# Print menu
def menu():
    print('Holiday Menu \n')
    menu_selections = '''1. Add a Holiday
    2. Remove a Holiday
    3. View Holidays
    4. Save
    5. Exit'''
    menu_selections = inspect.cleandoc(menu_selections)
    print(menu_selections)

# 1. Add a Holiday
def add():
    print('Add a Holiday')
    print(5 * '-')
    new_name = input('Enter Holiday Name: ')
    new_date = input('Enter Holiday Date (YYYY-MM-DD): ')
    try: # Check if date format is correct
        date_format = datetime.strptime(new_date, '%Y-%m-%d')
        new_holiday = Holiday(new_name, new_date)
        holidays_list.append(new_holiday)
        print('Success: The holiday has been added.')
        print(5 * '-')
    except ValueError:
        print ('Sorry, that is not the correct format. Please try again.')
        print(5 * '-')

# 2. Remove a Holiday
def remove():
    print('Remove a Holiday')
    print(5 * '-')
    remove_name = input('Enter Holiday Name: ')
    remove_date = input('Enter Holiday Date (YYYY-MM-DD): ')
    remove_holiday = Holiday(remove_name, remove_date)
    try: # I don't think this works
        date_format = datetime.strptime(remove_date, '%Y-%m-%d')
        holidays_list.remove(remove_holiday)
        print('Success: The holiday has been deleted.')
        print(5 * '-')
    except ValueError:
        print ('Sorry, that holiday is not found. Please try again.')
        print(5 * '-')

# 3. View Holidays
def view():
    print('View Holidays')
    print(5 * '-')
    year_option = int(input('Which year? (Please enter a year between 2021 and 2023.) '))
    print(5 * '-')
    if year_option in range(2021, 2024):
        week_option = int(input('Which week? (Please enter a number between 1 and 52.) '))
        print(5 * '-')
        if week_option in range(1, 53):
            week_year = Week(year_option, week_option) # Given year and week
            week_object = week_year.days() # Days of a given week
            week_dates = list(map(lambda object_day: object_day.strftime('%Y-%m-%d'), week_object)) # Formatted days
            current_week = datetime.today().isocalendar()[1] # Current week in the year
            if week_option == current_week: # Show holidays
                results = list(filter(lambda holiday: holiday.date in week_dates, holidays_list))
                for d in results:
                    print(d)
                print(5 * '-')
                weather_option = input('Would you like to see the weather forecast for the remaining days of the week? [Y/N] ').upper()
                print(5 * '-')
                if weather_option == 'Y': # Show weather
                    forecast = list(filter(lambda weather: weather.wdate in week_dates, weather_list))
                    for d in forecast:
                        print(d)
                    print(5 * '-')
                elif weather_option == 'N': # Skip weather
                    pass
                else:
                    print('Sorry, that is not an option. Please try again.')
                    print(5 * '-')
            else: # Show holidays
                results = list(filter(lambda holiday: holiday.date in week_dates, holidays_list))
                for d in results:
                    print(d)
                print(5 * '-')
        else:
            print('Sorry, that is not an option. Please try again.')
            print(5 * '-')
    else:
        print('Sorry, that is not an option. Please try again.')
        print(5 * '-')

# 4. Save
def save():
    print('Save')
    print(5 * '-')
    print('Are you sure you want to save your changes?')
    save_option = input('[Y/N] ').upper()
    if save_option == 'Y': # Save and return to menu
        print('Success: Your changes have been saved.')
        print('Returning to Menu... \n')
        print(5 * '-')
    elif save_option == 'N': # Return to menu
        print('Cancelled: Holiday list save file cancelled.')
        print('Returning to Menu... \n')
        print(5 * '-')
    else:
        print('Sorry, that is not an option. Please try again.')
        print(5 * '-')

# 5. Exit
def exit():
    print('Exit')
    print(5 * '-')
    print('Are you sure you want to exit? Any changes you have made will be lost.')
    exit_option = input('[Y/N] ').upper()
    if exit_option == 'Y':
        print('Goodbye! \n')
        print(5 * '-')
        loop = False
    elif exit_option == 'N': # Return to menu
        print('Returning to Menu... \n')
        print(5 * '-')
    else:
        print('Sorry, that is not an option. Please try again.')
        print(5 * '-')


print('Holiday Management')
print(5 * '-')

loop = True

# Prompt user to make a selection and follow functions
while loop:
    menu()
    menu_input = input('\nMake a Selection: ')
    print(5 * '-')
    if menu_input == '1':
        add()
    elif menu_input == '2':
        remove()
    elif menu_input == '3':
        view()
    elif menu_input == '4':
        save()
    elif menu_input == '5':
        exit()
        if not loop:
            break
    else:
        print('Sorry, that is not an option. Please try again.')
        print(5 * '-')