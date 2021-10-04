from dataclasses import dataclass, field
from datetime import datetime
import json
import inspect
import requests

# response = requests.get('https://api.weather.gov/gridpoints/TOP/87,64/forecast')
# Open API from the NWS with forecast in Milwaukee

# Create class for holidays
class Holiday:
    def __init__(self, name, date):
        self._name = name
        self._date = date
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, new_name, new_date):
        self._name = new_name
        self._date = new_date

    @name.deleter    
    def name(self):
        self.name = None
        self.date = None
        print('Success: The holiday has been deleted.')

    def formatted(self):
        return '{self.name} ({self.date})'
    
# Import from holidays.json into a list
import json
with open('holidays.json') as f:
    data = json.load(f)
    for holiday in data['holidays']:
        Holiday = holiday['name'], holiday['date']

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
        Holiday = new_name, new_date
        print('Success: The holiday has been added. \n')
    except ValueError:
        print ("Sorry, that is not the correct format. Please try again. \n")

# 2. Remove a Holiday
def remove():
    print('Remove a Holiday')
    print(40 * '-')
    remove_holiday = input('Enter Holiday Name: ')
    if remove_holiday in Holiday:
        del remove_holiday
    else:
        print ("Sorry, that holiday is not found. Please try again. \n")

# 3. View Holidays
def view():
    print('View Holidays')
    print(40 * '-')
    year_option = int(input('Which year? (Please enter a year between 2021 and 2023.) '))
    if year_option in range(2021, 2024):
        week_option = int(input('Which week? (Please enter a number between 1 and 52.) '))
        if week_option in range(1, 53):
            # "Use a lambda function to print holidays for a specified week.""
            # weekly_holidays = list(map(lambda name, date: '{name} ({date})'))
            # I'm not necessarily putting this here, but I want to have it somewhere.
            date_inputs = '{}-W{}'.format(year_option, week_option)
            print(date_inputs)
            week = datetime.strptime(date_inputs, '%G-W%V')
            print(week)
            # "If the current week is selected, ask if the user would like to see the weather forecast.""
            # print('Would you like to see the weather forecast for this week?')
            # weather_option = input('[Y/N] '.upper)
        else:
            print('Sorry, that is not an option. Please try again. \n')
    else:
        print('Sorry, that is not an option. Please try again. \n')

# 4. Save
def save():
    print('Save')
    print(40 * '-')
    print('Are you sure you want to save your changes?')
    save_option = input('[Y/N] '.upper)
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
    exit_option = input('[Y/N] '.upper)
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