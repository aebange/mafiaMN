import gc
import os
import sys

from colorama import init, Fore, Back

from abilities import *
from classes import Player, Role
from file_directory import *
from globalVars import *
from roles import neutralRolesList, mafiaRolesList, townRolesList

# TODO: Improve/Investigate slow import time.

## Dependencies list
# pip install pyglet
# pip install colorama


# Used to initialize colorama
init(convert=True)
# Used to fetch current working directory of filesystem
cwd = os.getcwd()
# Used to fetch sound file locations

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
        temp = pyglet.resource.media("sounds/clicks/keyboardTyping%d.mp3" % i, streaming=False)
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
    player_list.append(Player("Alex", 0, None, True, {}, "NULL", "NULL", [], [], "NULL", 0))
    player_list.append(Player("Maddie", 1, None, True, {}, "NULL", "NULL", [], [], "NULL", 0))
    player_list.append(Player("Tyler", 2, None, True, {}, "NULL", "NULL", [], [], "NULL", 0))
    player_list.append(Player("Will", 3, None, True, {}, "NULL", "NULL", [], [], "NULL", 0))
    player_list.append(Player("Jason", 4, None, True, {}, "NULL", "NULL", [], [], "NULL", 0))
    player_list.append(Player("Andrew", 5, None, True, {}, "NULL", "NULL", [], [], "NULL", 0))
    player_list.append(Player("Gillian", 6, None, True, {}, "NULL", "NULL", [], [], "NULL", 0))
    player_list.append(Player("Nick", 7, None, True, {}, "NULL", "NULL", [], [], "NULL", 0))
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
        player.uses = shuffled_roles[i].uses
        i += 1


# Start the game and explain the rules
def startup():
    type_writer("Welcome to ", delay=.1), sleep(1), print(Fore.RED + "MAFIA." + Fore.RESET)
    sniperShot2.play()
    sleep(3)
    print(" ")
    print(" ")
    print("CUSTOM VARIANT.")
    woosh3.play()
    sleep(2)
    goodNightBell.play()
    print("Now, please go to sleep so the first night may begin.")
    sleep(5)
    os.system('cls')


# Run through the night
def night_sequence(night_number):
    nightPlayer.queue(musicList[night_number])
    nightPlayer.play()
    deathList.clear()
    nightAmbientPlayer.queue(random.choice(soundsList))
    nightAmbientPlayer.play()
    for player in playerList:
        if player.living:
            # Prompt the user to begin their turn
            woosh2.play()
            print(Fore.LIGHTMAGENTA_EX + player.name + Fore.RESET + " press any key to begin your turn please.")
            input()
            os.system('cls')
            # Inform the user about what they are and what they do
            print("It is night number {0}.".format(night_number))
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
                    print("You will stay inside with your pet cat 'Clumpy' tonight." + Fore.LIGHTRED_EX + " Press any key to end your turn." + Fore.RESET)
                    input()
                    os.system('cls')
                    player.target = None
                else:
                    print("You went to kill {0} tonight, ".format(playerList[serial_killer_target].name) + Fore.LIGHTRED_EX + "press any key to end your turn." + Fore.RESET)
                    player.target = get_player_target(serial_killer_target)
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
                    print("You will stay inside with your pet cat 'Shadow' tonight." + Fore.LIGHTRED_EX + " Press any key to end your turn." + Fore.RESET)
                    input()
                    os.system('cls')
                    player.target = None
                else:
                    print("You went to guard {0} tonight, ".format(playerList[bodyguard_target].name) + Fore.LIGHTRED_EX + "press any key to end your turn." + Fore.RESET)
                    player.target = get_player_target(bodyguard_target)
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
                    print("You will stay inside with your pet cat 'Bubble' tonight." + Fore.LIGHTRED_EX + " Press any key to end your turn." + Fore.RESET)
                    input()
                    os.system('cls')
                    player.target = None
                else:
                    print("You went to distract {0} tonight, ".format(playerList[escort_target].name) + Fore.LIGHTRED_EX + "press any key to end your turn." + Fore.RESET)
                    player.target = get_player_target(escort_target)
                    input()
                    os.system('cls')
            elif player.role.name == "Lookout":
                print(" ")
                print(Fore.LIGHTRED_EX + "Select one person to attempt to watch tonight by typing their number:" + Fore.RESET)
                print("-" * SCREEN_WIDTH)
                print_remaining_players()
                # Check to make sure the input is actually a number
                lookout_target = get_user_input(player)
                if lookout_target == "S":
                    print("You will stay inside with your pet cat 'Lana' tonight." + Fore.LIGHTRED_EX + " Press any key to end your turn." + Fore.RESET)
                    input()
                    os.system('cls')
                    player.target = None
                else:
                    print("You went to watch {0} tonight, ".format(playerList[lookout_target].name) + Fore.LIGHTRED_EX + "press any key to end your turn." + Fore.RESET)
                    player.target = get_player_target(lookout_target)
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
                    print("You will stay inside with your pet dog 'Luna' tonight." + Fore.LIGHTRED_EX + " Press any key to end your turn." + Fore.RESET)
                    input()
                    os.system('cls')
                    player.target = None
                else:
                    print("You went to investigate {0} tonight, ".format(playerList[sheriff_target].name) + Fore.LIGHTRED_EX + "press any key to end your turn." + Fore.RESET)
                    player.target = get_player_target(sheriff_target)
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
                    print("You will stay inside with your pet cat 'Max' tonight." + Fore.LIGHTRED_EX + " Press any key to end your turn." + Fore.RESET)
                    input()
                    os.system('cls')
                    player.target = None
                else:
                    print("You went to shoot {0} tonight, ".format(playerList[vigilante_target].name) + Fore.LIGHTRED_EX + "press any key to end your turn." + Fore.RESET)
                    player.target = get_player_target(vigilante_target)
                    input()
                    os.system('cls')
            elif player.role.name == "Doctor":
                print(" ")
                print(
                    Fore.LIGHTRED_EX + "Select one person to attempt to heal tonight by typing their number:" + Fore.RESET)
                print("-" * SCREEN_WIDTH)
                print_remaining_players()
                # Check to make sure the input is actually a number
                doctor_target = get_user_input(player)
                if doctor_target == "S":
                    print("You will stay inside with your pet dog 'Rex' tonight." + Fore.LIGHTRED_EX + " Press any key to end your turn." + Fore.RESET)
                    input()
                    os.system('cls')
                    player.target = None
                else:
                    print("You went to heal {0} tonight, ".format(playerList[doctor_target].name) + Fore.LIGHTRED_EX + "press any key to end your turn." + Fore.RESET)
                    player.target = get_player_target(doctor_target)
                    input()
                    os.system('cls')
        else:
            # TODO: Add shit for dead people to do.
            pass
    # Conduct actual night activities
    sorted_player_list = sorted(playerList, key=lambda x: x.role.priority, reverse=False)
    # Since sorted_player_list contains the roles sorted based on priority, this should work.
    os.system('cls')
    dayTime.play()
    print("Tonight's events will now transpire...")
    fade_out(nightPlayer)
    sleep(5)
    os.system('cls')
    for player in sorted_player_list:
            if player.target is None or player.target == "NULL":
                # Player decided to skip the night or cannot do anything
                pass
            else:
                commit_role_action(player)
    # Night phase one is complete and role actions have been executed, now output user night info
    os.system('cls')
    print("Tonight's events have concluded, please close your eyes so you may learn what transpired last night.")
    sleep(5)
    goodNightBell.play()
    sleep(2)
    os.system('cls')
    for player in playerList:
        if player in permaDeathList:
            # This player has been dead for at least one night and has no turn.
            print(player.name + " is dead and cannot do anything." + Fore.LIGHTRED_EX + " Press enter to skip them." + Fore.RESET)
            input()
            os.system('cls')
            pass
        else:
            print(player.name + ", " + Fore.LIGHTRED_EX + "press enter to learn what happened tonight." + Fore.RESET)
            input()
            os.system('cls')
            if not player.info:
                print("Nothing exciting happened to you tonight, but at least you're alive right?")
            else:
                for info in player.info:
                    print(info)
                if not player.living:
                    # This player is now 100% dead
                    permaDeathList.append(player)
            print(Fore.LIGHTRED_EX + "Press enter to end your turn." + Fore.RESET)
            input()
            os.system('cls')
    # The night has concluded
    night_number += 1
    return night_number


def day_sequence(day_number):
    day_number += 1
    os.system('cls')
    print("Day number {0}.".format(day_number))
    dayTime.play()
    sleep(3)
    if len(deathList) >= 4:
        print("Many of us perished in the night...")
    elif len(deathList) >= 2:
        print("Some of us perished in the night...")
    elif len(deathList) == 1:
        print("One of us perished in the night...")
    else:
        print("Fortunately, nobody was found dead last night.")
    sleep(4)
    for player in deathList:
        deathNotification.play()
        print("{0} was found dead last night.".format(player.name))
        sleep(3)
        print(" ")
        # TODO: Color the role name here
        roleReveal.play()
        sleep(1)
        print("Their role was {0}".format(player.role.name))
        sleep(4)
    input()
    return day_number


# Output a list of all players to the user
def print_remaining_players():
    print("[S] SKIP THE NIGHT AND DO NOTHING")
    for player in playerList:
        if player.living:
            print("[{0}] {1}".format(player.number, player.name))
        else:
            print("[X] {0}".format(player.name))


########################################################################################################################
# UTILITY
########################################################################################################################


# Initialize global lists to store what roles apply to which type
townGovernmentRoles = []
townProtectiveRoles = []
townInvestigativeRoles = []
townKillingRoles = []
neutralKillingRoles = []


# Gradually decreases the volume level of a selected track
def fade_out(player):
    while player.volume > 0:
        player.volume -= .005
        sleep(.02)
    player.pause()


# Gradually increases the volume level of a selected track
def fade_in(player):
    player.play()
    while player.volume < 1:
        player.volume += .005
        sleep(.02)


# Take the target number recieved from the player and swap it for the corresponding player object
def get_player_target(target_number):
    for player in playerList:
        if player.number == target_number:
            return player


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
        # Randomize the lists so the order players night_abilities are executed in is fair.
        random.shuffle(priority0Roles)
        random.shuffle(priority1Roles)
        random.shuffle(priority2Roles)
        random.shuffle(priority3Roles)



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
    if not player.living:
        if player in permaDeathList:
            # This player has been dead, do nothing
            return
        else:
            # The player is dead and their ability will not be activated
            player.info.append("\033[31mYou died before you could do anything.\033[39m")
            return
    if player.uses == 0:
        # The player is out of uses and their ability will not be activated
        player.info.append("\033[31mYou are out of uses for that ability and couldn't do anything.\033[39m")
        # TODO: This isn't the best way to handle this, in the future block them out during the first phase of the night
        return
    else:
        if player.role.night_abilities == "None":
            # Player has no night abilities
            pass
        else:
            if not player.uses == 666:
                # Player has a limited number of uses for their ability
                # Subtract one use from their pool of uses
                player.uses -= 1
                # Check for the function to be called for the user's role's ability and apply it
                dispatch[player.role.night_abilities](player)
            else:
                # Player has an unlimited number of uses for their ability
                # Check for the function to be called for the user's role's ability and apply it
                dispatch[player.role.night_abilities](player)


########################################################################################################################
# CODE EXECUTION
########################################################################################################################

# Generate lists of objects based on type from garbage collection
generate_type_list()

# Generate the sequence of sounds used in the typing sound effect
clickList = generate_click_list()

# Prompt the users to identify themselves
playerList = user_identification()

# Distribute roles to the players
user_role_distribution(playerList, (neutralRolesList + mafiaRolesList + townRolesList))

# Start the game
startup()

nightNumber = 0
dayNumber = 0

# Create players for the music and ambient sounds
nightPlayer = pyglet.media.Player()
nightAmbientPlayer = pyglet.media.Player()

# Create lists of the music and ambient sounds to be played
musicList = [nightSequence1, nightSequence2, nightSequence3, nightSequence4, nightSequence5, nightSequence6]
soundsList = [nightSounds1, rainSounds1]

# Run the first night
nightNumber = night_sequence(nightNumber)
dayNumber = day_sequence(dayNumber)

# Prevent the screen from closing
input()
