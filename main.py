# Citation for ZipTrip logo font:
# Slant by Glenn Chappell 3/93 -- based on Standard
# Includes ISO Latin-1
# figlet release 2.1 -- 12 Aug 1994

import os
import json
import pymysql
import time
from models import User, Destination, Search


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
    welcome_message = """Menu: \n[1] New User - Register \n[2] Returning User - Login \n[3] Search as Guest \n[Q] Quit"""
    # app_description = """
    # Search for travel destinations and view popular
    # restaurants and attractions, weather forecasts,
    # and packing list recommendations all in one place."""
    app_description = """Enter a zip code to see the city name and weather forecast. \nSearch as a guest or create a profile to save destinations. \n\nCreating a profile takes less than 30 seconds and allows you \nto save destinations for your future travels.
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
    menu = """Menu: \n[1] Create Profile \n[0] Go Back"""
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
        menu = """Menu: \n[1] Destination Search \n[0] Go Back"""
    else:
        print(f"""{user}'s Dashboard\n""")
        menu = """Menu: \n[1] Destination Search \n[2] View Saved Destinations \n[0] Go Back"""
    print(f"{menu}\n")
    choice = input("""Make a selection: """)
    if choice == "1":
        destination_search()
    elif choice == "2":
        view_saved_destinations()
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
            data = {'name': new_user}
            User.create_user(data)
            user_dashboard(new_user)
        elif confirm.lower() == 'n':
            create_profile()
        else:
            print("Invalid entry. Please try again.")
            create_profile()


# DESTINATION SEARCH
def destination_search(first_run=True):
    if first_run:
        clear_console()
        print(zt_logo)
    print("""Destination Search\n""")
    menu = """Menu: \n[1] Enter Zip Code \n[0] Go Back"""
    print(f"{menu}\n")
    choice = input("""Make a selection: """)
    if choice == "1":
        zip = input("Enter a zip code to search: ")
        search_by_zip(zip)
    elif choice == "0":
        user_dashboard()
    else:
        print("Invalid entry. Please try again.")
        destination_search(first_run=False)


# SEARCH RESULTS
def search_by_zip(zip):
    clear_console()
    print("""Search Results\n""")
    search_info = f"You searched for: {zip}"
    # city_name = "Boston, MA"
    menu = """Menu: \n[1] Save Search \n[2] Show Details \n[0] Go Back"""
    print(f"{search_info}\n")
    print(f"{city_name}\n")
    print(f"{menu}\n")
    choice = input("Make a selection: ")
    if choice == "1":
        save_search()
    elif choice == "0":
        destination_search()
    else:
        print("Invalid entry. Please try again.")
        search_by_zip()


# SAVE SEARCH
def save_search():
    clear_console()
    print("\nSave Search Results\n")
    print("Your search results for Boston, MA have been saved.")
    menu = """Menu: \n[0] Return to Dashboard \n[Q] Quit"""
    print(f"\n{menu}\n")
    choice = input("Make a selection: ")
    if choice == "Q" or choice == "q":
        pass
    elif choice == "1":
        user_dashboard()
    else:
        print("Invalid entry. Please try again.")
        save_search()


# VIEW SAVED DESTINATIONS
def view_saved_destinations(user):
    pass
    print(f"\n{user}'s Saved Destinations\n")



if __name__ == "__main__":
    welcome_user()