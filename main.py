# Citation for ZipTrip logo font:
# Slant by Glenn Chappell 3/93 -- based on Standard
# Includes ISO Latin-1
# figlet release 2.1 -- 12 Aug 1994

import os
import json
import pymysql
import time
from models import User, Destination, Search
import requests
from dotenv import load_dotenv

load_dotenv()

OW_API_KEY = os.getenv('OPEN_WEATHER_API_KEY')


zt_logo = """
        _____   _          ______     _     
       /__  /  (_)___     /_  __/____(_)___ 
         / /  / / __ \\     / / / ___/ / __ \\
        / /__/ / /_/ /    / / / /  / / /_/ /
       /____/_/ .___/    /_/ /_/  /_/ .___/ 
             /_/                   /_/      
    """


# CLEAR CONSOLE
def clear_console():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')


# WELCOME SCREEN
def welcome_user():
    clear_console()

    print(zt_logo)
    welcome_message = """------ Menu ------  \n[1] New User - Register \n[2] Returning User - Login \n[3] Search as Guest \n[Q] Quit\n------------------"""
    # app_description = """
    # Search for travel destinations and view popular
    # restaurants and attractions, weather forecasts,
    # and packing list recommendations all in one place."""
    app_description = """Enter a valid US zip code to see the city name and weather forecast. \nSearch as a guest or create a profile to save destinations. \n\nCreating a profile takes less than 30 seconds and allows you \nto save destinations for your future travels.
    """
    print(app_description)
    print(welcome_message)
    choice = input("""\nMake a selection: """)
    if choice == "1":
        new_user()
    elif choice == "2":
        print("You selected Returning User")
    elif choice == "3":
        user_dashboard("Guest")
    elif choice == "Q" or "q":
        print("Goodbye\n")
    else:
        print("Invalid choice")
        welcome_user()


# NEW USER
def new_user():
    clear_console()
    print(zt_logo)
    print("""Welcome New User!\n""")
    menu = """------ Menu ------  \n[1] Create Profile \n[0] Go Back\n------------------"""
    print(f"{menu}\n")
    choice = input("""Make a selection: """)
    if choice == "1":
        create_profile()
    elif choice == "0":
        welcome_user()
    else:
        print("Invalid choice")
        new_user()


# USER DASHBOARD
def user_dashboard(user):
    clear_console()
    print(zt_logo)
    if user == "Guest":
        print("\nWelcome, Guest!\n")
        menu = """------ Menu ------  \n[1] Destination Search \n[0] Go Back\n------------------"""
    else:
        print(f"""{user}'s Dashboard\n""")
        menu = """------ Menu ------  \n[1] Destination Search \n[2] View Saved Destinations \n[0] Go Back\n------------------"""
    print(f"{menu}\n")
    choice = input("""Make a selection: """)
    if choice == "1":
        destination_search(user)
    elif choice == "2":
        view_saved_destinations(user)
    elif choice == "0":
        welcome_user()


# CREATE PROFILE
def create_profile():
    clear_console()
    print(zt_logo)
    print("\nCreate a Profile\n")
    new_user = input("Please enter your name to save a profile: ")
    print(f"\nYou entered: {new_user}")
    if User.get_user_by_name({'name': new_user}):
        user_choice = input(f"{new_user} already has a profile. Login as {new_user}? y/n: ")
        if user_choice.lower() == 'y':
            user_dashboard(new_user)
        elif user_choice.lower() == 'n':
            welcome_user()
    else:
        print("This will be the name of your profile.")
        confirm = input("\nIs this correct? y/n: ")
        print("\n")
        if confirm.lower() == 'y':
            user_data = {'name': new_user}
            User.create_user(user_data)
            user_dashboard(new_user)
        elif confirm.lower() == 'n':
            create_profile()
        else:
            print("Invalid entry. Please try again.")
            create_profile()


# DESTINATION SEARCH
def destination_search(user, first_run=True):
    if first_run:
        clear_console()
        print(zt_logo)
    print("""Destination Search\n""")
    menu = """------ Menu ------  \n[1] Enter US Zip Code \n[0] Go Back\n------------------"""
    print(f"{menu}\n")
    choice = input("""Make a selection: """)
    if choice == "1":
        zip = input("Enter a valid US zip code to search: ")
        dest_info = get_destination_name_from_zip(zip)
        print("""Search Results:\n""")
        print(f"You searched for: {zip}\n")
        print(dest_info[1])
        if dest_info[0]: # valid search
            user_choice_save = input("Save this search? y/n: ")
            if user_choice_save.lower() == 'y':
                save_search_to_db(dest_info[1], user)
        else: # invalid search
            destination_search(user, first_run=False)
    elif choice == "0":
        user_dashboard(user)
    else:
        print("Invalid entry. Please try again.")
        destination_search(user, first_run=False)

def get_destination_name_from_zip(zip):
    req = requests.get(f'http://api.openweathermap.org/geo/1.0/zip?zip={zip},US&appid={OW_API_KEY}')
    if req.status_code != 200:
        return (False, "Invalid zip code. Please enter a valid US zip code.")
    else:
        result = req.json()
        return (True, result)

# SAVE SEARCH
def save_search_to_db(dest_info, user):
    clear_console()
    dest_data = {'zip': dest_info['zip'], 'name': dest_info['name'], 'lat': dest_info['lat'], 'lon': dest_info['lon']}
    saved_dest = Destination.save_destination(dest_data)
    user_data = {'name': user}
    user_id = User.get_user_id_by_name(user_data)[0]['id']
    if saved_dest:
        search_data = {'user_id': user_id, 'destination_id': saved_dest}
        saved_search = Search.save_search(search_data)
        print(f"Your search results for {dest_info['zip']}: {dest_info['name']} have been saved.")
    else:
        print("There was a problem saving your destination.")
    menu = """------ Menu ------  \n[0] Return to Dashboard \n[Q] Quit\n------------------"""
    print(f"\n{menu}\n")
    choice = input("Make a selection: ")
    if choice == "Q" or choice == "q":
        pass
    elif choice == "0":
        user_dashboard(user)
    else:
        print("Invalid entry. Please try again.")


# VIEW SAVED DESTINATIONS
def view_saved_destinations(user):
    clear_console()
    print(zt_logo)
    print(f"\n{user}'s Saved Destinations\n")
    user_data = {'name': user}
    user_id = User.get_user_id_by_name(user_data)[0]['id']
    data = {'user_id': user_id}
    saved_searches = Search.get_user_saved_searches(data)
    for i in range(len(saved_searches)):
        print(f"[{i+1}] {saved_searches[i]['name']}: {saved_searches[i]['zip']}")
    selection = input("\nSelect a Saved Destination to view details, or 0 to return to Dashboard: ")
    if selection == '0':
        user_dashboard(user)
    elif selection.isdigit() and int(selection) in range(len(saved_searches)):
        display_details(saved_searches[int(selection)-1], user)
    else:
        print("Invalid entry. Please try again.")
        view_saved_destinations(user)

def display_details(destination, user):
    print(f"Details for {destination['name']}\n")
    


if __name__ == "__main__":
    welcome_user()