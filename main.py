import gc
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

SCREEN_WIDTH = 110


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

    # Assign objectives to the players once they have their roles
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
            print("ERROR: INVALID self.alignment OF '%s' HAS ATTEMPTED TO PASS THROUGH def summary(self)!" % str(
                self.alignment))
        return "You are {} aligned with the {}.To win, you must {}".format(self.description, self.alignment, self.objective)

    # Assign colors to the roles for outputting via type_writer function
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
            print("ERROR: INVALID self.alignment PRESENTED TO role_color METHOD!")
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
    "a regular person who believes in truth and justice.",  # Summary (A lore-based description of the role)
    "The Citizen has a Bulletproof Vest that can be used to save them from death only ONCE each night. If you are attacked by multiple people however, you will die. Be conservative as your vest may have limited uses!")

bodyguard = Role(
    "Bodyguard",
    "Town",
    ["Town Protective"],
    ["Guard"],
    "INF",
    ["None"],
    ["Heal Immune"],
    "a war veteran who secretly makes a living by selling protection.",
    "The bodyguard can guard one person each night. If that person is attacked while you are protecting them, both you and the attacker will die. The person you are protecting however will be spared - EVEN if they aren't town.")

lookout = Role(
    "Lookout",
    "Town",
    ["Town Investigative"],
    ["Watch"],
    "INF",
    ["None"],
    ["Self-Target", "Ignore Detection Immunity"],
    "a war veteran who secretly makes a living by selling protection.",
    "The lookout can stake out at one person's house each night to see who visits them. Remember, not only evil players may be visiting other's houses.")

escort = Role(
    "Escort",
    "Town",
    ["Town Protective"],
    ["Role-block"],
    "INF",
    ["None"],
    ["None"],
    "a scantily-clad escort, working in secret.",
    "The escort can visit one person's house each night, giving them such a good time that they are role-blocked for that night and cannot complete any actions.")

doctor = Role(
    "Doctor",
    "Town",
    ["Town Protective"],
    ["Heal"],
    "INF",
    ["None"],
    ["Attack Alert"],
    "a secret surgeon skilled in trauma care.",
    "The doctor can guard one person each night. If that person is attacked while you are protecting them, you will heal them fully. You can only heal them once though, and multiple attackers will succeed in their mission.")

sheriff = Role(
    "Sheriff",
    "Town",
    ["Town Investigative"],
    ["Check Affiliation"],
    "INF",
    ["None"],
    ["None"],
    "a member of law enforcement, forced into hiding because of the threat of murder.",
    "The sheriff can investigate one person's house each night, identifying who they are affiliated with. Beware however, for you will be a prime target for murder once you reveal your findings to your colleagues.")

mayor = Role(
    "Mayor",
    "Town",
    ["Town Government", "Town Investigative"],
    ["Day Reveal"],
    "1",
    ["Heal Immune"],
    ["None"],
    "the governor of the town, hiding in anonymity to avoid assassination.",
    "The mayor has no night abilities, but can reveal himself during the day. Revealing increases the value of your vote significantly and confirms to the other players that you are indeed the mayor. Use this power to lead the town, but use it carefully, you will be a big target for the evil players.")

vigilante = Role(
    "Vigilante",
    "Town",
    ["Town Killing"],
    ["Murder"],
    "2",
    ["Heal Immune"],
    ["None"],
    "a dirty ex-cop who will ignore the law to enact justice.",
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
    "a deranged criminal who hates the world.",
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


# Types out provided strings of text with sound
# By default, writing color is white with a typing delay of .02
def night_type_writer(string, beep=False, color="W", delay=.008):
    if beep:
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
            print(x)
            sys.stdout.flush()
            print("\n", end='')
            sleep(.4)
        else:
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
    player_list.append(Player("Alex", 0, "NULL", True, "Well", " "))
    player_list.append(Player("Maddie", 1, "NULL", True, "Well", " "))
    player_list.append(Player("Tyler", 2, "NULL", False, "Well", " "))
    player_list.append(Player("Will", 3, "NULL", True, "Well", " "))
    player_list.append(Player("Jason", 4, "NULL", True, "Well", " "))
    player_list.append(Player("Andrew", 5, "NULL", True, "Well", " "))
    player_list.append(Player("Gillian", 6, "NULL", True, "Well", " "))
    player_list.append(Player("Nick", 7, "NULL", True, "Well", " "))
    # while True:
    #     current_player = Player("AWAITING_INSTANTIATION", i, "NULL", True, "Well", " ")
    #     print("Would you like to add a new player?")
    #     input_choice = input()
    #     if input_choice.lower() == "yes":
    #         print("Please enter a name for this person:")
    #         current_player.name = (str(input()))
    #         player_list.append(current_player)
    #         print("{0} has been added to the game as player {1}".format(current_player.name, i))
    #         os.system('cls')
    #         i += 1
    #     else:
    #         os.system('cls')
    return player_list


# Assign relevant roles to the users
# Pass this function the playerList and a list containing all relevant roles
def user_role_distribution(players, roles):
    i = 0
    shuffled_roles = random.sample(roles, len(roles))
    for player in players:
        player.role = shuffled_roles[i]
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
def night_sequence():
    music_list = [nightSequence1, nightSequence2, nightSequence3, nightSequence4, nightSequence5, nightSequence6]
    music_list[nightNumber].play()
    for item in playerList:
        if item.living:
            # Prompt the user to begin their turn
            print("{0}, press any key to begin your turn please.".format(item.name))
            garbage = input()
            os.system('cls')
            # Inform the user about what they are and what they do
            night_type_writer("Good evening {0}, you are a ".format(item.name)), print(
                (item.role.role_color()) + str(item.role.name) + "." + Back.RESET + Fore.RESET)
            print("As a {0}, you are {1}".format(item.role.name, item.role.description))
            print(item.role.hint)
            if item.role.name == "Serial Killer":
                print(" ")
                print("Select one person to attempt to kill tonight by typing their number:")
                print("-" * SCREEN_WIDTH)
                print_remaining_players()
                # Check to make sure the input is actually a number
                serial_killer_target = get_user_input()
                if serial_killer_target == "S":
                    print("You will stay inside with your pet cat 'Clumpy' tonight.")
                else:
                    print("You went to kill {0} tonight, press any key to end your turn.".format(
                        playerList[serial_killer_target].name))
                    garbage = input()
                    os.system('cls')
            elif item.role.name == "Citizen":
                print(" ")
                print("You can't do anything at night, but enter some random number to make people think you can.")
                garbage = input()
                print("Good job, press any key to end your turn.")
                garbage = input()
                os.system('cls')
            elif item.role.name == "Mayor":
                print(" ")
                print("You can't do anything at night, but enter some random number to make people think you can.")
                garbage = input()
                print("Good job, press any key to end your turn.")
                garbage = input()
                os.system('cls')
            elif item.role.name == "Bodyguard":
                print(" ")
                print("Select one person to attempt to guard tonight by typing their number:")
                print("-" * SCREEN_WIDTH)
                print_remaining_players()
                # Check to make sure the input is actually a number
                bodyguard_target = get_user_input()
                if bodyguard_target == "S":
                    print("You will stay inside with your pet cat 'Shadow' tonight.")
                else:
                    print("You went to guard {0} tonight, press any key to end your turn.".format(
                        playerList[bodyguard_target].name))
                    garbage = input()
                    os.system('cls')
            elif item.role.name == "Escort":
                print(" ")
                print("Select one person to attempt to distract tonight by typing their number:")
                print("-" * SCREEN_WIDTH)
                print_remaining_players()
                # Check to make sure the input is actually a number
                escort_target = get_user_input()
                if escort_target == "S":
                    print("You will stay inside with your pet cat 'Bubble' tonight.")
                else:
                    print("You went to distract {0} tonight, press any key to end your turn.".format(
                        playerList[escort_target].name))
                    garbage = input()
                    os.system('cls')
            elif item.role.name == "Lookout":  # Gonna need to be informed who visited their target last night at some point
                print(" ")
                print("Select one person to attempt to watch tonight by typing their number:")
                print("-" * SCREEN_WIDTH)
                print_remaining_players()
                # Check to make sure the input is actually a number
                lookout_target = get_user_input()
                if lookout_target == "S":
                    print("You will stay inside with your pet cat 'Lana' tonight.")
                else:
                    print("You went to watch {0} tonight, press any key to end your turn.".format(
                        playerList[lookout_target].name))
                    garbage = input()
                    os.system('cls')
            elif item.role.name == "Sheriff":
                print(" ")
                print("Select one person to attempt to search tonight by typing their number:")
                print("-" * SCREEN_WIDTH)
                print_remaining_players()
                # Check to make sure the input is actually a number
                sheriff_target = get_user_input()
                if sheriff_target == "S":
                    print("You will stay inside with your pet cat 'Luna' tonight.")
                else:
                    print("You went to investigate {0} tonight, press any key to end your turn.".format(
                        playerList[sheriff_target].name))
                    garbage = input()
                    os.system('cls')
            elif item.role.name == "Vigilante":
                print(" ")
                print("Select one person to attempt to shoot tonight by typing their number:")
                print("-" * SCREEN_WIDTH)
                print_remaining_players()
                # Check to make sure the input is actually a number
                vigilante_target = get_user_input()
                if vigilante_target == "S":
                    print("You will stay inside with your pet cat 'Max' tonight.")
                else:
                    print("You went to assassinate {0} tonight, press any key to end your turn.".format(
                        playerList[vigilante_target].name))
                    garbage = input()
                    os.system('cls')
            input()
            os.system('cls')


# Output a list of all players to the user
def print_remaining_players():
    print("[S] SKIP THE NIGHT AND DO NOTHING")
    for player in playerList:
        if player.living:
            print("[{0}] {1}".format(player.number, player.name))
        else:
            print("[X] {0}".format(player.name))


########################################################################################################################
# BACK-END UTILITY
########################################################################################################################


# Instantiate global lists to store what roles apply to which type
townGovernmentRoles = []
townProtectiveRoles = []
townInvestigativeRoles = []
townKillingRoles = []
neutralKillingRoles = []


# Build a list of all objects based on attributes
def generate_object_list():
    for obj in gc.get_objects():
        if isinstance(obj, Role):
            for item in obj.type:
                if item == "Town Government":
                    townGovernmentRoles.append(obj)
                elif item == "Town Protective":
                    townProtectiveRoles.append(obj)
                elif item == "Town Investigative":
                    townInvestigativeRoles.append(obj)
                elif item == "Town Killing":
                    townKillingRoles.append(obj)
                elif item == "Neutral Killing":
                    neutralKillingRoles.append(obj)
                else:
                    print("ERROR: INVALID self.type (Role) PRESENTED TO generate_object_list FUNCTION!")


def get_user_input():
    while True:
        local_target = str(input())
        if not local_target.isdigit():
            if local_target == "S":
                return local_target
            else:
                print("That wasn't the kind of number we were looking for, choose another please.")
                sleep(2)
        else:
            if int(local_target) < len(playerList) and int(local_target) >= 0:
                local_target = int(local_target)
                if not playerList[local_target].living:
                    print("That person is dead, choose another please.")
                else:
                    return local_target
            else:
                print("That person doesn't exist, choose another please.")

########################################################################################################################
# CODE EXECUTION
########################################################################################################################

generate_object_list()
clickList = generate_click_list()
playerList = user_identification()
user_role_distribution(playerList, (neutralRolesList + mafiaRolesList + townRolesList))

startup()
night_sequence()
input()
