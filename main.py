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

# DISPLAY TITLE
def display_title(page_title_string=""):
    clear_console()
    print(zt_logo)
    print(page_title_string)

# WELCOME SCREEN
def welcome_user():
    app_description = """\nEnter a valid US zip code to see the city name and weather forecast. \nSearch as a guest or create a profile to save destinations. \n\nCreating a profile takes less than 30 seconds and allows you \nto save destinations for your future travels.
    """
    welcome_menu = """------ Menu ------  \n[R] Register (New User) \n[L] Login (Existing User) \n[G] Guest User \n[Q] Quit\n------------------"""
    display_title(app_description)
    print(welcome_menu)
    choice = input("""\nMake a selection: """)
    if choice.lower() == "r":
        create_profile()
    elif choice.lower() == "l":
        returning_user()
    elif choice.lower() == "g":
        user_dashboard("Guest")
    elif choice.lower() == "q":
        print("Goodbye\n")
    else:
        print("Invalid choice")
        welcome_user()
        
# RETURNING USER
def returning_user():
    display_title("Welcome Back!\n")
    user_name = input("Enter the name of your profile to login (case sensitive): ")
    if User.get_user_by_name({'name': user_name}):
        user_dashboard(user_name)
    else:
        print(f"No profile found under the name {user_name}.")
        login_again = input("Would you like to try a different profile? Enter 'y' to try again, or any other key to return to the main menu: ")
        if login_again.lower() == "y":
            returning_user()
        else:
            welcome_user()


# NEW USER
def new_user():
    display_title("""Welcome New User!\n""")
    menu = """------ Menu ------  \n[C] Create Profile \n[M] Back to Main Menu\n------------------"""
    print(f"{menu}\n")
    choice = input("""Make a selection: """)
    if choice.lower() == "c":
        create_profile()
    elif choice.lower() == "m":
        welcome_user()
    else:
        print("Invalid choice")
        new_user()

# CREATE PROFILE
def create_profile():
    display_title("""Welcome New User!\n""")
    menu = """------ Menu ------  \n[C] Create Profile \n[M] Back to Main Menu\n------------------"""
    print(f"{menu}\n")
    choice = input("""Make a selection: """)
    if choice.lower() == "c":
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
    elif choice.lower() == "m":
        welcome_user()
    else:
        print("Invalid choice")
        new_user()

# USER DASHBOARD
def user_dashboard(user):
    if user == "Guest":
        dash_title = "\nWelcome, Guest!\n"
        menu = """------ Menu ------  \n[S] Destination Search \n[M] Main Menu\n------------------"""
    else:
        dash_title = f"""{user}'s Dashboard\n"""
        menu = """------ Menu ------  \n[S] Destination Search \n[V] View Saved Destinations \n[M] Main Menu\n------------------"""
    display_title(dash_title)
    print(f"{menu}\n")
    choice = input("""Make a selection: """)
    if choice.lower() == "s":
        destination_search(user)
    elif choice.lower() == "v":
        view_saved_destinations(user)
    elif choice.lower() == "m":
        welcome_user()
    else:
        user_dashboard(user)


# DESTINATION SEARCH
def destination_search(user, first_run=True):
    if first_run:
        display_title("""Destination Search\n""")
    menu = """------ Menu ------  \n[Z] Search by Zip Code \n[C] Search by City Name \n[M] Main Menu\n------------------"""
    print(f"{menu}\n")
    choice = input("""Make a selection: """)
    if choice.lower() == "z":
        zip = input("Enter a valid US zip code to search: ")
        dest_info = get_destination_name_from_zip(zip)
        print("""Search Results:\n""")
        print(f"You searched for: {zip}\n")
        print(dest_info[1])
        if dest_info[0]: # valid search
            user_choice_save = input("Save this search? y/n: ")
            if user_choice_save.lower() == 'y':
                save_search_to_db(dest_info[1], user)
            else:
                destination_search(user)
        else: # invalid search
            print("Invalid entry. Please try again.")
            destination_search(user, first_run=False)
    
    # SEARCH BY CITY, STATE
    elif choice.lower() == "c":
        city = input("Enter a valid US city name to search: ")
        state = input("Enter a US state abbreviation: ")
        dest_info = get_destination_from_city_name(city, state)
        print("""Search Results:\n""")
        if dest_info: # valid search
            print(f"You searched for: {city, state}\n")
            user_choice_save = input("Save this search? y/n: ")
            if user_choice_save.lower() == 'y':
                dest_data = {'name': dest_info[1]['name'], 'lat': dest_info[1]['lat'], 'lon': dest_info[1]['lon']}
                save_search_to_db(dest_data, user)
        else: # invalid search
            redirect_to_zip_input = input(f"Your search for {city}, {state} did not return any results. Try again using a zip code instead? y/n: ")
            if redirect_to_zip_input.lower() == "y":
                destination_search(user, first_run=False)
    elif choice.lower() == "m":
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

def get_destination_from_city_name(city, state):
    req = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city},{state},US&limit=1&appid={OW_API_KEY}')
    print(req.json())
    if req.status_code != 200:
        return (False, "Invalid location name. Please enter a valid US city and state.")
    else:
        result = req.json()
        if len(result) == 0:
            return False
        return (True, result[0])

# SAVE SEARCH
def save_search_to_db(dest_info, user):
    display_title()
    if 'zip' in dest_info:
        dest_data = {'zip': dest_info['zip'], 'name': dest_info['name'], 'lat': dest_info['lat'], 'lon': dest_info['lon']}
        saved_dest = Destination.save_destination_with_zip(dest_data)
    else:
        dest_data = {'name': dest_info['name'], 'lat': dest_info['lat'], 'lon': dest_info['lon']}
        saved_dest = Destination.save_destination_without_zip(dest_data)
    user_data = {'name': user}
    user_id = User.get_user_id_by_name(user_data)[0]['id']
    if saved_dest:
        search_data = {'user_id': user_id, 'destination_id': saved_dest}
        Search.save_search(search_data)
        if 'zip' in dest_info:
            print(f"Your search results for {dest_info['zip']}: {dest_info['name']} have been saved.")
        else:
            print(f"Your search results for {dest_info['name']} have been saved.")
    else:
        print("There was a problem saving your destination.")
    choice = input("Press 'D' to return to your dashboard, or any other key to Quit: ")
    if choice.lower() == "d":
        user_dashboard(user)
    else:
        pass

# VIEW SAVED DESTINATIONS
def view_saved_destinations(user):
    display_title(f"\n{user}'s Saved Destinations\n")
    user_data = {'name': user}
    user_id = User.get_user_id_by_name(user_data)[0]['id']
    data = {'user_id': user_id}
    saved_searches = Search.get_user_saved_searches(data)
    
    # USER HAS NO SAVED SEARCHES
    if len(saved_searches) == 0:
        print("No Saved Searches to display.\n")
        menu = """\n------ Menu ------  \n[D] Return to Dashboard \n[Q] Quit\n------------------"""
        print(f"{menu}\n")
        selection = (input("Make a selection: "))
        if selection.lower() == 'd':
            user_dashboard(user)
        elif selection.lower() == 'q':
            pass
        else:
            print("Invalid selection. Please try again")
            view_saved_destinations(user)
            
    # USER HAS SAVED SEARCHES
    else:
        for i in range(len(saved_searches)):
            if saved_searches[i]['zip'] != None:
                print(f"[{saved_searches[i]['id']}] {saved_searches[i]['name']}: {saved_searches[i]['zip']}")
            else:
                print(f"[{saved_searches[i]['id']}] {saved_searches[i]['name']}")
                
        menu = """\n------ Menu ------  \n[R] Return to Dashboard \n[V] View Details of a Saved Destination \n[D] Delete a Saved Destination \n[Q] Quit\n------------------"""
        print(f"\n{menu}\n")
        selection = (input("Make a selection: "))
        if selection.lower() == 'r':
            user_dashboard(user)
            
        # VIEW DETAILS
        elif selection.lower() == 'v':
            display_title()
            for i in range(len(saved_searches)):
                print(f"[{saved_searches[i]['id']}] {saved_searches[i]['name']}: {saved_searches[i]['zip']}")
            search_to_view = input("\nEnter the number of the Destination you would like to see details for: ")
            if search_to_view.isdigit():
                saved_search_details = Destination.get_destination_by_id({'id': int(search_to_view)})
                print(saved_search_details)
                display_details(saved_search_details[0], user)
                nav_away_from_details = input("Enter 'V' to return to your Saved Destinations, or any other key to Quit: ")
                if nav_away_from_details.lower() == 'v':
                    view_saved_destinations(user)
                else:
                    print("Goodbye\n")
                    pass
            else:
                print("Invalid selection. Please try again") #TODO
        
        # DELETE SAVED SEARCH
        elif selection.lower() == 'd':
            display_title(f"{user}'s Saved Destinations:\n")
            for i in range(len(saved_searches)):
                print(f"[{saved_searches[i]['id']}] {saved_searches[i]['name']}: {saved_searches[i]['zip']}")
            search_to_delete = input("\nSelect the search you'd like to delete: ")
            if search_to_delete.isdigit():
                confirm_delete = input(f"Are you sure you want to delete your saved search for {saved_searches[i]['name']}? This action cannot be undone. y/n: ")
                if confirm_delete.lower() == 'y':
                    search_data = {'user_id': user_id, 'destination_id': int(search_to_delete)}
                    Search.delete_search(search_data)
                    view_saved_destinations(user)
                else:
                    view_saved_destinations(user)
            else:
                print("Invalid entry. Please try again.")
                view_saved_destinations(user)
        elif selection.lower() == "q":
            print("Goodbye\n")
            pass
        else:
            print("Invalid entry. Please try again.")
            view_saved_destinations(user)

def display_details(destination, user):
    display_title("Search Details\n")
    print(f"Details for {destination['name']}: \nZip code: {destination['zip']} \nLatitude: {destination['lat']} \nLongitude: {destination['lon']}\n\n")

if __name__ == "__main__":
    welcome_user()