from dataclasses import dataclass, field
from datetime import datetime
from datetime import date
import json
import inspect
import requests

# Open API from the NWS with forecast in Milwaukee, I'm still working on getting this
response = requests.get('https://api.weather.gov/gridpoints/TOP/87,64/forecast')

def jprint(obj):
    text = json.dumps(obj, sort_keys = True, indent = 4)
    print(text)

weather_properties = response.json()['properties']
# jprint(weather_properties)

time_period = []

for p in weather_properties:
    sun = properties['periods']
    time_period.append(sun)

print(time_period)

# Create class for holidays
class Holiday:
    def __init__(self, name, date):
        self.name = name
        self.date = date
    
    @property
    def name(self):
        return self.name
    
    @name.setter
    def name(self, new_name, new_date):
        self.name = new_name
        self.date = new_date

    @name.deleter    
    def name(self, name, date):
        self.name = None
        self.date = None
        print('Success: The holiday has been deleted.')

    def formatted(self):
        return '{} ({})'.format(self.name, self.date)
    
# Import from holidays.json
import json
with open('holidays_updated.json') as f: # Using the updated JSON file for convenience
    data = json.load(f)
    for holiday in data['holidays']:
        Holiday = holiday['name'], holiday['date']
        # print(Holiday) just to see all holidays

# Print menu
def menu():
    print('Holiday Menu')
    print(40 * '-')
    menu_selections = '''1. Add a Holiday
    2. Remove a Holiday
    3. View Holidays
    4. Save
    5. Exit'''
    menu_selections = inspect.cleandoc(menu_selections)
    print(menu_selections, '\n')

# 1. Add a Holiday
def add():
    print('Add a Holiday')
    print(40 * '-')
    new_name = input('Enter Holiday Name: ')
    new_date = input('Enter Holiday Date (YYYY-MM-DD): ')
    try: # Check if date format is correct
        date_format = datetime.strptime(new_date, '%Y-%m-%d')
        # new_holiday = Holiday(new_name, new_date)
        print('Success: The holiday has been added. \n')
    except ValueError:
        print ('Sorry, that is not the correct format. Please try again. \n')

# 2. Remove a Holiday
def remove():
    print('Remove a Holiday')
    print(40 * '-')
    remove_holiday = input('Enter Holiday Name: ')
    if remove_holiday in Holiday:
        print('some code')
    else:
        print ('Sorry, that holiday is not found. Please try again. \n')

# 3. View Holidays
def view():
    print('View Holidays')
    print(40 * '-')
    year_option = int(input('Which year? (Please enter a year between 2021 and 2023.) '))
    if year_option in range(2021, 2024):
        week_option = int(input('Which week? (Please enter a number between 1 and 52.) '))
        if week_option in range(1, 53):
            current_date = date(2021, 10, 4)
            current_week = current_date.isocalendar().week
            print(current_week)
            if week_option == current_week:
                print('Would you like to see the weather forecast for this week?')
                weather_option = input('[Y/N] ').upper()
                if weather_option == 'Y': # Show holidays with weather
                    print('some code')
                elif weather_option == 'N': # Show only holidays
                    print('some code')
                else:
                    print('Sorry, that is not an option. Please try again. \n')
            else: # Show only holidays
                print('some code')
        else:
            print('Sorry, that is not an option. Please try again. \n')
    else:
        print('Sorry, that is not an option. Please try again. \n')

# 4. Save
def save():
    print('Save')
    print(40 * '-')
    print('Are you sure you want to save your changes?')
    save_option = input('[Y/N] ').upper()
    if save_option == 'Y': # Save and return to menu
        print('Success: Your changes have been saved.')
        print('Returning to Menu... \n')
    elif save_option == 'N': # Return to menu
        print('Cancelled: Holiday list save file cancelled.')
        print('Returning to Menu... \n')
    else:
        print('Sorry, that is not an option. Please try again. \n')

# 5. Exit
def exit():
    print('Exit')
    print(40 * '-')
    print('Are you sure you want to exit? Any changes you have made will be lost.')
    exit_option = input('[Y/N] ').upper()
    if exit_option == 'Y':
        print('Goodbye! \n')
        loop = False
    elif exit_option == 'N': # Return to menu
        print('Returning to Menu... \n')
    else:
        print('Sorry, that is not an option. Please try again. \n')


print('Holiday Management \n')

loop = True

# Prompt user to make a selection and follow functions
while loop:
    menu()
    menu_input = input('Make a Selection: ')
    print(40 * '-')
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
        print('Sorry, that is not an option. Please try again. \n')
        print(40 * '-')
