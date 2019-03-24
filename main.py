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
sniperShot2 = pyglet.resource.media("sounds/gunshots/sniperShot2.wav", streaming=False)
goodNightBell = pyglet.resource.media("sounds/misc/goodNightBell.wav", streaming=False)
nightSequence1 = pyglet.resource.media("sounds/music/nightSequence1.wav", streaming=False)
nightSequence2 = pyglet.resource.media("sounds/music/nightSequence2.wav", streaming=False)
nightSequence3 = pyglet.resource.media("sounds/music/nightSequence3.wav", streaming=False)
nightSequence4 = pyglet.resource.media("sounds/music/nightSequence4.wav", streaming=False)
nightSequence5 = pyglet.resource.media("sounds/music/nightSequence5.wav", streaming=False)
nightSequence6 = pyglet.resource.media("sounds/music/nightSequence6.wav", streaming=False)

nightNumber = 1


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
    def __init__(self, name, alignment, type, night_abilities, uses, immunities, traits, description, hint):
        self.name = name
        self.alignment = alignment
        self.type = type
        self.night_abilities = night_abilities
        self.uses = uses
        self.immunities = immunities
        self.traits = traits
        self.description = description
        self.hint = hint
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
            self.color = Fore.WHITE
            self.back = Fore.GREEN
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
    "a regular person who believes in truth and justice,",  # Summary (A lore-based description of the role)
    "The Citizen has a Bulletproof Vest that can be used to save them from death only ONCE each night. If you are attacked by multiple people however, you will die. Be conservative as your vest may have limited uses!")

bodyguard = Role(
    "Bodyguard",
    "Town",
    ["Town Protective"],
    ["Guard"],
    "INF",
    ["None"],
    ["Heal Immune"],
    "a war veteran who secretly makes a living by selling protection,",
    "The bodyguard can guard one person each night. If that person is attacked while you are protecting them, both you and the attacker will die, but your protectee will be spared - EVEN if they aren't town.")

lookout = Role(
    "Lookout",
    "Town",
    ["Town Investigative"],
    ["Watch"],
    "INF",
    ["None"],
    ["Self-Target", "Ignore Detection Immunity"],
    "a war veteran who secretly makes a living by selling protection,",
    "The lookout can stake out at one person's house each night to see who visits them. Remember, not only evil players may be visiting other's houses.")

escort = Role(
    "Escort",
    "Town",
    ["Town Protective"],
    ["Role-block"],
    "INF",
    ["None"],
    ["None"],
    "a scantily-clad escort, working in secret,",
    "The escort can visit one person's house each night, giving them such a good time that they are role-blocked for that night and cannot complete any actions.")

doctor = Role(
    "Doctor",
    "Town",
    ["Town Protective"],
    ["Heal"],
    "INF",
    ["None"],
    ["Attack Alert"],
    "a secret surgeon skilled in trauma care,",
    "The doctor can guard one person each night. If that person is attacked while you are protecting them, you will heal them back to health after the attacker has left.")

sheriff = Role(
    "Sheriff",
    "Town",
    ["Town Investigative"],
    ["Check Affiliation"],
    "INF",
    ["None"],
    ["None"],
    "a member of law enforcement, forced into hiding because of the threat of murder,",
    "The sheriff can investigate one person's house each night, identifying who they are affiliated with. Beware however, for you will be a prime target for murder once you reveal your findings to your friends.")

mayor = Role(
    "Mayor",
    "Town",
    ["Town Government"],
    ["Day Reveal"],
    "1",
    ["Heal Immune"],
    ["None"],
    "the governor of the town, hiding in anonymity to avoid assassination,",
    "The mayor has no night abilities, but can reveal himself during the day, increasing the value of his vote significantly and confirming to the other players that he is indeed the mayor. Use this power to lead the town.")

vigilante = Role(
    "Vigilante",
    "Town",
    ["Town Killing"],
    ["Murder"],
    "2",
    ["Heal Immune"],
    ["None"],
    "a dirty ex-cop who will ignore the law to enact justice,",
    "The vigilante can choose to murder one person each night. This will not kill anyone who has night immunity - like the Serial Killer, but can work on weaker roles. This ability can kill town members too. Be conservative with your gun, you only have so many bullets.")

# Define Neutral Roles
serial_killer = Role(
    "Serial Killer",
    "Serial Killer",
    ["Neutral Killing"],
    ["Murder"],
    "INF",
    ["Detect Immune","Night Immune"],
    ["None"],
    "a deranged criminal who hates the world,",
    "The serial killer can choose to murder one person each night. You are night-immune and can only die by suicide or hanging during the day. Try to target roles who will lead the town to discovering you first.")


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
# GAME MECHANIC FUNCTIONS
########################################################################################################################

# Identify and define users, instantiating their classes
def user_identification():
    i = 0
    player_list = []
    while True:
        current_player = Player("AWAITING_INSTANTIATION", i, "NULL", "Living", "Well", " ")
        print("Would you like to add a new player?")
        input_choice = input()
        if input_choice.lower() == "yes":
            print("Please enter a name for this person:")
            current_player.name = (str(input()))
            player_list.append(current_player)
            print("{0} has been added to the game as player {1}".format(current_player.name, i))
            os.system('cls')
            i += 1
        else:
            os.system('cls')
            return player_list


# Assign relevant roles to the users
# Pass this function the playerList and a list containing all relevant roles
def user_role_distribution(players, roles):
    i = 0
    shuffled_roles = random.sample(roles, len(roles))
    for player in players:
        player.role = shuffled_roles[i]
        print(player.name + " is now a " + player.role.name)
        i += 1


# Start the game and explain the rules
def startup():
    type_writer("Welcome to ", delay=.1), sleep(1), print(Fore.RED + "MAFIA.")
    sniperShot2.play()
    sleep(1)
    type_writer("We will begin by informing the participants of their occupations.", beep=True)
    sleep(3)
    goodNightBell.play()
    sleep(3)
    os.system('cls')


# Run through the first night
def first_night():
    music_list = [nightSequence1, nightSequence2, nightSequence3, nightSequence4, nightSequence5, nightSequence6]
    music_list[nightNumber].play()
    for item in playerList:
        if item.living:
            print("Good evening {0}, you are a {1}".format(item.name, item.role.name))
            print("As a {0}, you are {1}".format(item.role.name, item.role.description))
            print(item.role.hint)
            input()
            os.system('cls')

########################################################################################################################
# CODE EXECUTION
########################################################################################################################

clickList = generate_click_list()
playerList = user_identification()
user_role_distribution(playerList, (neutralRolesList + mafiaRolesList + townRolesList))

startup()
first_night()
input()
