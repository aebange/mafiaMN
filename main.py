import os
import random
import sys
from time import sleep

import pyglet
from colorama import init, Fore, Back

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
    type_writer("Welcome to ",delay=.1), print(Fore.RED + "MAFIA.")
    sleep(1)
    type_writer("A game by Alex Bange.", beep=False)
    user1 = Player("Alex", "1", serial_killer, "Alive", "Well", "")
    type_writer("Good evening "), print(user1.name + "."), type_writer("Your role is ",beep=False), print((user1.role.role_color()) + str(user1.role.name) + "."), print(Back.RESET)
    type_writer(user1.role.summary())


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
        self.objective = "Awaiting instantiation in def summary line 59..."
        self.color = Fore.WHITE
        self.back = Back.BLACK

    def summary(self):
        if self.alignment == "Town":
            self.objective = objectiveList[0]
        elif self.alignment == "Mafia":
            self.objective = objectiveList[1]
        elif self.alignment == "Serial Killer":
            self.objective = objectiveList[2]
        elif self.alignment == "Any":
            self.objective = objectiveList[3]
        elif self.alignment == "Evil":
            self.objective = objectiveList[4]
        else:
            print("ERROR: INVALID self.alignment OF '%s' HAS ATTEMPTED TO PASS THROUGH def summary(self) LINE 59." % str(self.alignment))
        return "You are {} aligned with the {}.To win, you must {}".format(self.description, self.alignment, self.objective)

    def role_color(self):
        if self.alignment == "Town":
            self.color = Fore.GREEN
            self.back = Fore.BLACK
        elif self.alignment == "Mafia":
            self.color = Fore.RED
            self.back = Fore.BLACK
        elif self.alignment == "Serial Killer":
            self.color = Fore.WHITE
            self.back = Back.MAGENTA
        elif self.alignment == "Any":
            self.color = Fore.WHITE
            self.back = Fore.BLACK
        elif self.alignment == "Evil":
            self.color = Fore.WHITE
            self.back = Fore.BLACK
        else:
            print("ERROR, INVALID self.alignment PRESENTED TO role_color METHOD LINE 76")
        return self.color + self.back


# Define alignment objectives
objectiveList = ["lynch all criminals and evildoers to restore justice to the town.",  # Town Alignment
                 "lynch and murder all of those who would oppose the mafia.",  # Mafia Alignment
                 "be the last person left alive.",  # Serial Killer Alignment
                 "survive until a victor has emerged."]  # Any Alignment


# Define Town Roles
citizen = Role(
    "Citizen",  # Name (What the role is called)
    "Town",  # Affiliation (How the role wins)
    ["Town Government"],  # Type (What the role does)
    ["Bulletproof Vest"],  # Abilities (What the role can do at night)
    "1",  # Uses (How many times the ability can be used)
    ["None"],  # Immunities (What the role cant be killed or detected by at night)
    ["None"],  # Traits (Special details about the role)
    "a regular person who believes in truth and justice,")  # Summary (A lore-based description of the role)

bodyguard = Role(
    "Bodyguard",
    "Town",
    ["Town Protective"],
    ["Guard"],
    "INF",
    ["None"],
    ["Heal Immune"],
    "a war veteran who secretly makes a living by selling protection,")

lookout = Role(
    "Lookout",
    "Town",
    ["Town Investigative"],
    ["Watch"],
    "INF",
    ["None"],
    ["Self-Target", "Ignore Detection Immunity"],
    "a war veteran who secretly makes a living by selling protection,")

escort = Role(
    "Escort",
    "Town",
    ["Town Protective"],
    ["Role-block"],
    "INF",
    ["None"],
    ["None"],
    "a scantily-clad escort, working in secret,")

doctor = Role(
    "Doctor",
    "Town",
    ["Town Protective"],
    ["Heal"],
    "INF",
    ["None"],
    ["Attack Alert"],
    "a secret surgeon skilled in trauma care,")

sheriff = Role(
    "Sheriff",
    "Town",
    ["Town Investigative"],
    ["Check Affiliation"],
    "INF",
    ["None"],
    ["None"],
    "a member of law enforcement, forced into hiding because of the threat of murder,")

mayor = Role(
    "Mayor",
    "Town",
    ["Town Government"],
    ["Day Reveal"],
    "1",
    ["Heal Immune"],
    ["None"],
    "the governor of the town, hiding in anonymity to avoid assassination,")

vigilante = Role(
    "Vigilante",
    "Town",
    ["Town Killing"],
    ["Murder"],
    "2",
    ["Heal Immune"],
    ["None"],
    "a dirty ex-cop who will ignore the law to enact justice,")

# Define Neutral Roles
serial_killer = Role(
    "Serial Killer",
    "Serial Killer",
    ["Neutral Killing"],
    ["Murder"],
    "INF",
    ["Detect Immune","Night Immune"],
    ["None"],
    "a deranged criminal who hates the world,")

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
# By default, writing color is white with a typing delay of .02
def type_writer(string, beep=True, color="W", delay=.02):
    if beep:
        newLineBeep.play()
        sleep(.4)
    else:
        pass
    if color == "W":
        print(Fore.WHITE)
    elif color == "R":
        print(Fore.RED)
    elif color == "G":
        print(Fore.GREEN)
    elif color == "O":
        print(Fore.ORANGE)
    elif color == "B":
        print(Fore.BLUE)
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
            sleep(delay)


########################################################################################################################

clickList = generate_click_list()

startup()

input()
