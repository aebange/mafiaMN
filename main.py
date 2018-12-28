import os
import random
import sys
from time import sleep

import pyglet
from colorama import init, Fore

## Dependencies list
# pip install pyglet
# pip install colorama


# Used to instantiate colorama
init(convert=True)
# Used to fetch current working directory of filesystem
cwd = os.getcwd()
# Used to fetch sound file locations
newLineBeep = pyglet.resource.media("sounds/misc/newLineBeep1.wav", streaming=False)


def startup():
    type_writer("Welcome to ", "WHITE")
    pass


########################################################################################################################
# ROLES AND USER RELATED FUNCTIONS
########################################################################################################################


# Create the class structure for players
class Player:
    def __init__(self, name, number, role, living, status, last_will):
        self.name = name
        self.number = number
        self.role = role
        self.living = living
        self.status = status
        self.last_will = last_will


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
    "Citizen",  # Name (What the role is called)
    ["Town"],  # Affiliation (How the role wins)
    ["Town Government"],  # Type (What the role does)
    ["Bulletproof Vest"],  # Abilities (What the role can do at night)
    "1",  # Uses (How many times the ability can be used)
    ["None"],  # Immunities (What the role cant be killed or detected by at night)
    ["None"],  # Traits (Special details about the role)
    "A regular person who believes in truth and justice.")

bodyguard = Role(
    "Bodyguard",
    ["Town"],
    ["Town Protective"],
    ["Guard"],
    "INF",
    ["None"],
    ["Heal Immune"],
    "A war veteran who secretly makes a living by selling protection.")

lookout = Role(
    "Lookout",
    ["Town"],
    ["Town Investigative"],
    ["Watch"],
    "INF",
    ["None"],
    ["Self-Target", "Ignore Detection Immunity"],
    "A war veteran who secretly makes a living by selling protection.")

escort = Role(
    "Escort",
    ["Town"],
    ["Town Protective"],
    ["Role-block"],
    "INF",
    ["None"],
    ["None"],
    "A scantily-clad escort, working in secret.")

doctor = Role(
    "Doctor",
    ["Town"],
    ["Town Protective"],
    ["Heal"],
    "INF",
    ["None"],
    ["Attack Alert"],
    "A secret surgeon skilled in trauma care.")

sheriff = Role(
    "Sheriff",
    ["Town"],
    ["Town Investigative"],
    ["Check Affiliation"],
    "INF",
    ["None"],
    ["None"],
    "A member of law enforcement, forced into hiding because of the threat of murder.")

mayor = Role(
    "Mayor",
    ["Town"],
    ["Town Government"],
    ["Day Reveal"],
    "1",
    ["Heal Immune"],
    ["None"],
    "The governor of the town, hiding in anonymity to avoid assassination.")

vigilante = Role(
    "Vigilante",
    ["Town"],
    ["Town Killing"],
    ["Murder"],
    "2",
    ["Heal Immune"],
    ["None"],
    "A dirty ex-cop who will ignore the law to enact justice.")

# Define Neutral Roles
serial_killer = Role(
    "Serial Killer",
    ["Solo"],
    ["Neutral Killing"],
    ["Murder"],
    "INF",
    ["Detect Immune"],
    ["None"],
    "A deranged criminal who hates the world.")

# Define Mafia Roles

# Included roles
townRolesList = [citizen, bodyguard, lookout, escort, doctor, sheriff, mayor, vigilante]
neutralRolesList = [serial_killer]
mafiaRolesList = []


########################################################################################################################
# VISUAL AND AUDIO EFFECT RELATED FUNCTIONS
########################################################################################################################


# Generate a list of the paths to utilized audio
def generate_click_list():
    click_list = []
    i = 0
    while True:
        i += 1
        temp = pyglet.resource.media("sounds/clicks/keyboardTyping%d.wav" % i, streaming=False)
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
            print("\n", end='')
            sleep(.4)
        else:
            random.choice(clickList).play()
            print(x, end='')
            sys.stdout.flush()
            sleep(.02)


########################################################################################################################

clickList = generate_click_list()

type_writer("Simon was Killed last night.", "WHITE")
type_writer("He had several stabs about his torso and was dragged outside into the street.", "WHITE")
type_writer("His role was ", "WHITE")
print(Fore.RED + "Arsonist.")

input()
