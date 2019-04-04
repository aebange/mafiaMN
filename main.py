import gc
import os
import sys
from time import sleep

from colorama import init, Fore, Back

from abilities import *
from classes import Player, Role
from file_directory import *
from roles import neutralRolesList, mafiaRolesList, townRolesList

## Dependencies list
# pip install pyglet
# pip install colorama


# Used to initialize colorama
init(convert=True)
# Used to fetch current working directory of filesystem
cwd = os.getcwd()
# Used to fetch sound file locations

nightNumber = 0

SCREEN_WIDTH = 110


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
    player_list.append(Player("Alex", 0, None, True, {}, "NULL", "NULL", [], []))
    player_list.append(Player("Maddie", 1, None, True, {}, "NULL", "NULL", [], []))
    player_list.append(Player("Tyler", 2, None, False, {}, "NULL", "NULL", [], []))
    player_list.append(Player("Will", 3, None, True, {}, "NULL", "NULL", [], []))
    player_list.append(Player("Jason", 4, None, True, {}, "NULL", "NULL", [], []))
    player_list.append(Player("Andrew", 5, None, True, {}, "NULL", "NULL", [], []))
    player_list.append(Player("Gillian", 6, None, True, {}, "NULL", "NULL", [], []))
    player_list.append(Player("Nick", 7, None, True, {}, "NULL", "NULL", [], []))
    # while True:
    #     current_player = Player("AWAITING_INSTANTIATION", i, None, True, {}, "NULL", "NULL", [], [])
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
    sleep(1)
    goodNightBell.play()
    sleep(5)
    os.system('cls')


# Run through the first night
def night_sequence():
    music_list = [nightSequence1, nightSequence2, nightSequence3, nightSequence4, nightSequence5, nightSequence6]
    music_list[nightNumber].play()
    nightSounds1.play()
    for player in playerList:
        if player.living:
            # Prompt the user to begin their turn
            woosh2.play()
            print(Fore.LIGHTMAGENTA_EX + player.name + Fore.RESET + " press any key to begin your turn please.")
            input()
            os.system('cls')
            # Inform the user about what they are and what they do
            night_type_writer("Good evening " + Fore.LIGHTMAGENTA_EX + player.name + Fore.RESET + ", you are a " + (
                player.role.role_color()) + str(player.role.name) + "." + Back.RESET + Fore.RESET)
            print("You are {0}".format(player.role.description))
            print(player.role.hint)
            if player.role.name == "Serial Killer":
                print(" ")
                print(Fore.LIGHTRED_EX + "Select one person to attempt to kill tonight by typing their number:" + Fore.RESET)
                print("-" * SCREEN_WIDTH)
                print_remaining_players()
                # Check to make sure the input is actually a number
                serial_killer_target = get_user_input(player)
                if serial_killer_target == "S":
                    print("You will stay inside with your pet cat 'Clumpy' tonight.")
                    player.target = None
                else:
                    print("You went to kill {0} tonight, ".format(playerList[serial_killer_target].name) + Fore.LIGHTRED_EX + "press any key to end your turn." + Fore.RESET)
                    player.target = serial_killer_target
                    input()
                    os.system('cls')
            elif player.role.name == "Citizen":
                # TODO: Add functionality to this, he cannot use his vest yet.
                print(" ")
                print("You can't do anything at night, but " + Fore.LIGHTRED_EX + "enter some random number to make people think you can." + Fore.RESET)
                input()
                print("Good job," + Fore.LIGHTRED_EX + " press any key to end your turn." + Fore.RESET)
                player.target = None
                input()
                os.system('cls')
            elif player.role.name == "Mayor":
                print(" ")
                print("You can't do anything at night, but " + Fore.LIGHTRED_EX + "enter some random number to make people think you can." + Fore.RESET)
                input()
                print("Good job," + Fore.LIGHTRED_EX + " press any key to end your turn." + Fore.RESET)
                player.target = None
                input()
                os.system('cls')
            elif player.role.name == "Bodyguard":
                print(" ")
                print(Fore.LIGHTRED_EX + "Select one person to attempt to guard tonight by typing their number:" + Fore.RESET)
                print("-" * SCREEN_WIDTH)
                print_remaining_players()
                # Check to make sure the input is actually a number
                bodyguard_target = get_user_input(player)
                if bodyguard_target == "S":
                    print("You will stay inside with your pet cat 'Shadow' tonight.")
                    player.target = None
                else:
                    print("You went to guard {0} tonight, ".format(playerList[bodyguard_target].name) + Fore.LIGHTRED_EX + "press any key to end your turn." + Fore.RESET)
                    player.target = bodyguard_target
                    input()
                    os.system('cls')
            elif player.role.name == "Escort":
                print(" ")
                print(Fore.LIGHTRED_EX + "Select one person to attempt to distract tonight by typing their number:" + Fore.RESET)
                print("-" * SCREEN_WIDTH)
                print_remaining_players()
                # Check to make sure the input is actually a number
                escort_target = get_user_input(player)
                if escort_target == "S":
                    print("You will stay inside with your pet cat 'Bubble' tonight.")
                    player.target = None
                else:
                    print("You went to distract {0} tonight, ".format(playerList[escort_target].name) + Fore.LIGHTRED_EX + "press any key to end your turn." + Fore.RESET)
                    player.target = None
                    input()
                    os.system('cls')
            elif player.role.name == "Lookout":  # Gonna need to be informed who visited their target last night at some point
                print(" ")
                print(Fore.LIGHTRED_EX + "Select one person to attempt to watch tonight by typing their number:" + Fore.RESET)
                print("-" * SCREEN_WIDTH)
                print_remaining_players()
                # Check to make sure the input is actually a number
                lookout_target = get_user_input(player)
                if lookout_target == "S":
                    print("You will stay inside with your pet cat 'Lana' tonight.")
                    player.target = None
                else:
                    print("You went to watch {0} tonight, ".format(playerList[lookout_target].name) + Fore.LIGHTRED_EX + "press any key to end your turn." + Fore.RESET)
                    player.Target = lookout_target
                    input()
                    os.system('cls')
            elif player.role.name == "Sheriff":
                print(" ")
                print(Fore.LIGHTRED_EX + "Select one person to attempt to search tonight by typing their number:" + Fore.RESET)
                print("-" * SCREEN_WIDTH)
                print_remaining_players()
                # Check to make sure the input is actually a number
                sheriff_target = get_user_input(player)
                if sheriff_target == "S":
                    print("You will stay inside with your pet cat 'Luna' tonight.")
                    player.target = None
                else:
                    print("You went to investigate {0} tonight, ".format(playerList[sheriff_target].name) + Fore.LIGHTRED_EX + "press any key to end your turn." + Fore.RESET)
                    player.target = sheriff_target
                    input()
                    os.system('cls')
            elif player.role.name == "Vigilante":
                print(" ")
                print(Fore.LIGHTRED_EX + "Select one person to attempt to shoot tonight by typing their number:" + Fore.RESET)
                print("-" * SCREEN_WIDTH)
                print_remaining_players()
                # Check to make sure the input is actually a number
                vigilante_target = get_user_input(player)
                if vigilante_target == "S":
                    print("You will stay inside with your pet cat 'Max' tonight.")
                    player.target = None
                else:
                    print("You went to shoot {0} tonight, ".format(playerList[vigilante_target].name) + Fore.LIGHTRED_EX + "press any key to end your turn." + Fore.RESET)
                    player.target = vigilante_target
                    os.system('cls')
            # Conduct actual night activities
            # Role blockers/ Vests/ Bodyguards/ Deceptive roles
            for player in priority0Roles:
                commit_role_action(player)
            # Killing Roles
            for player in priority1Roles:
                commit_role_action(player)
            # Healing roles
            for player in priority2Roles:
                commit_role_action(player)
            # Investigative roles
            for player in priority3Roles:
                commit_role_action(player)


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


# Initialize global lists to store what roles apply to which type
townGovernmentRoles = []
townProtectiveRoles = []
townInvestigativeRoles = []
townKillingRoles = []
neutralKillingRoles = []


# Build a list of all objects based on attributes
def generate_type_list():
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
                    print("ERROR: INVALID self.type (Role) PRESENTED TO generate_type_list FUNCTION!")


# Initialize global lists to store what roles apply to which type
priority0Roles = []
priority1Roles = []
priority2Roles = []
priority3Roles = []


# Build a list of all objects based on attributes
def generate_priority_list():
    for obj in gc.get_objects():
        if isinstance(obj, Role):
            for item in obj.priority:
                if item == 0:
                    priority0Roles.append(obj)
                elif item == 1:
                    priority1Roles.append(obj)
                elif item == 2:
                    priority2Roles.append(obj)
                elif item == 3:
                    priority3Roles.append(obj)
                else:
                    print("ERROR: INVALID self.type (Role) PRESENTED TO generate_priority_list FUNCTION!")


def get_user_input(player):
    while True:
        local_target = str(input())
        if not local_target.isdigit():
            if local_target == "S":
                return local_target
            else:
                print("That wasn't the kind of number we were looking for," + Fore.LIGHTRED_EX + " choose another please." + Fore.RESET)
                sleep(2)
        else:
            if int(local_target) < len(playerList) and int(local_target) >= 0:
                local_target = int(local_target)
                if not playerList[local_target].living:
                    print("That person is dead," + Fore.LIGHTRED_EX + " choose another please." + Fore.RESET)
                else:
                    if local_target == player.number:
                        for trait in player.role.traits:
                            if trait == "Self-Target":
                                return local_target
                        print("You cannot target yourself," + Fore.LIGHTRED_EX + " choose another person please." + Fore.RESET)
                    else:
                        return local_target
            else:
                print("That person doesn't exist," + Fore.LIGHTRED_EX + " choose another please." + Fore.RESET)


# Delegate player actions unto their targets, checking and handling potential remaining uses
def commit_role_action(player):
    if player.role.uses == 0:
        # The player is out of uses and their ability will not be activated
        player.info.append("\033[31mYou are out of uses for that ability and couldn't do anything.\033[39m")
        # TODO: This isn't the best way to handle this, in the future block them out during the first phase of the night
        return
    else:
        if not player.role.uses == 666:
            # Player has a limited number of uses for their ability
            # Subtract one use from their pool of uses
            player.role.uses -= 1
            # Check for the function to be called for the user's role's ability and apply it
            dispatch[player.role.night_abilities](player)
        else:
            # Player has an unlimited number of uses for their ability
            # Check for the function to be called for the user's role's ability and apply it
            dispatch[player.role.night_abilities](player)



########################################################################################################################
# CODE EXECUTION
########################################################################################################################


generate_type_list()
clickList = generate_click_list()
playerList = user_identification()
user_role_distribution(playerList, (neutralRolesList + mafiaRolesList + townRolesList))

startup()
night_sequence()
input()
