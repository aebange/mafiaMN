from time import sleep
from colorama import init, Fore, Back, Style
import sys
import pyglet
import os
import random

## Dependencies list
# pip install pyglet
# pip install colorama


# Used to instantiate colorama
init(convert=True)
# Used to fetch current working directory of filesystem
cwd = os.getcwd()
# Used to fetch sound file locations
newLineBeep = pyglet.resource.media("sounds/misc/newLineBeep1.wav",streaming=False)


def startup():
    type_writer("Welcome to ", "WHITE")
    pass

########################################################################################################################
# ROLES AND USER RELATED FUNCTIONS
########################################################################################################################


# Create the class structure for players
class Player:
    def __init__(self, name, number, role, living, status):
        self.name = name
        self.number = number
        self.role = role
        self.living = living
        self.status = status


# Create the class structure for roles
class Role:
    def __init__(self, name, alignment, type, night_abilities, uses, immunities, traits, description):
        self.name = name
        self.alignment = alignment
        self.type = type
        self.night_abilities = night_abilities
        self.uses = uses
        self.immunities = immunities
        self.traits = traits
        self.description = description


# Define Town Roles
citizen = Role(
    "Citizen",              # Name (What the role is called)
    ["Town"],               # Affiliation (How the role wins)
    ["Government"],         # Type (What the role does)
    ["Bulletproof Vest"],   # Abilities (What the role can do at night)
    "1",                    # Uses (How many times the ability can be used)
    ["None"],               # Immunities (What the role cant be killed or detected by at night)
    ["None"],               # Traits (Special details about the role)
    "A regular person who believes in truth and justice.")

bodyguard = Role(
    "Bodyguard",            # Name (What the role is called)
    ["Town"],               # Affiliation (How the role wins)
    ["Protective"],         # Type (What the role does)
    ["Guard"],              # Abilities (What the role can do at night)
    "INF",                  # Uses (How many times the ability can be used)
    ["None"],               # Immunities (What the role cant be killed or detected by at night)
    ["No-Heal"],            # Traits (Special details about the role)
    "A war veteran who secretly makes a living by selling protection.")

lookout = Role(
    "Lookout",              # Name (What the role is called)
    ["Town"],               # Affiliation (How the role wins)
    ["Investigative"],      # Type (What the role does)
    ["Watch"],              # Abilities (What the role can do at night)
    "INF",                  # Uses (How many times the ability can be used)
    ["None"],               # Immunities (What the role cant be killed or detected by at night)
    ["Self-Target"],        # Traits (Special details about the role)
    "A war veteran who secretly makes a living by selling protection.")



# Define Neutral Roles

# Define Mafia Roles


# Included roles
townRolesList = [citizen,bodyguard]
neutralRolesList = []
mafiaRolesList = []



########################################################################################################################
# VISUAL AND AUDIO EFFECT RELATED FUNCTIONS
########################################################################################################################


# Generate a list of the paths to utilized audio
def generate_clicklist():
    click_list = []
    i = 0
    while True:
        i+=1
        temp = pyglet.resource.media("sounds/clicks/keyboardTyping%d.wav" % i,streaming=False)
        click_list.append(temp)
        if i == 11:
            return click_list
        else:
            pass


# Types out provided strings of text with sound
def type_writer(string, color):
    newLineBeep.play()
    sleep(.2)
    if color == "WHITE":
        print(Fore.WHITE)
    elif color == "RED":
        print(Fore.RED)
    else:
        pass

    # Filter through the values in the string provided to the function
    for x in string:
        if x == ".":
            random.choice(clickList).play()
            print(x)
            sys.stdout.flush()
            print("\n",end='')
            sleep(.4)
        else:
            random.choice(clickList).play()
            print(x,end='')
            sys.stdout.flush()
            sleep(.02)


########################################################################################################################

clickList = generate_clicklist()

type_writer("Simon was Killed last night.", "WHITE")
type_writer("He had several stabs about his torso and was dragged outside into the street.", "WHITE")
type_writer("His role was ", "WHITE")
print(Fore.RED + "Arsonist.")

input()