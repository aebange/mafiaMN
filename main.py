import gc
import os
import sys
from math import ceil
from msvcrt import getch, kbhit
from time import perf_counter

import cursor
from colorama import init, Fore

import xboxController
from abilities import *
from classes import Player, Role
from file_directory import *
from globalVars import *
from roles import scriptedMafiaRole

# TODO: Improve/Investigate slow import time.

## Dependencies list (beyond included libs)
# pip install pyglet
# pip install colorama


# Used to initialize colorama
init(convert=True)
# Used to fetch current working directory of filesystem
cwd = os.getcwd()
# Used to fetch sound file locations

SCREEN_WIDTH = 110

########################################################################################################################
# CONFIG AND SETTINGS
########################################################################################################################

# If this value is false, the game will seek input from an xbox controller
keyboardController = False

# If this value is true, the game will not erase lines as they are printed for controller input
globalDebug = False

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
# GAME LOOP FUNCTIONS
########################################################################################################################

# Start the game and explain the rules
def startup():
    os.system('cls')
    type_writer("Welcome to ", delay=.1), sleep(1), print(Fore.RED + "MAFIA." + Fore.RESET)
    sniperShot2.play()
    sleep(3)
    print(" ")
    print(" ")
    print("CUSTOM VARIANT.")
    woosh3.play()
    sleep(2)
    goodNightBell.play()
    print(" ")
    print(" ")
    print("\033[91mPlease close your eyes\033[0m so the first night may begin.")
    sleep(5)
    os.system('cls')


# Run through the night
def night_sequence(night_number):
    desired_track = (musicList[night_number])
    sleep(.1)
    nightPlayer.next_source()
    sleep(.1)
    nightPlayer.queue(desired_track)
    sleep(.1)
    nightPlayer.play()
    deathList.clear()
    nightAmbientPlayer.queue(random.choice(soundsList))
    dayAmbientPlayer.pause()
    nightAmbientPlayer.play()
    if keyboardController:
        end_turn_instruction = "press ENTER to end your turn."
        end_turn_instruction_2 = "Press ENTER to end your turn."
        begin_turn_instruction = ", \033[91mpress ENTER to begin your turn please.\033[0m"
        skip_turn_instruction = " Press ENTER to skip them."
        learn_event_instruction = "press ENTER to learn what happened tonight."
    else:
        end_turn_instruction = "press A to end your turn."
        end_turn_instruction_2 = "Press A to end your turn."
        begin_turn_instruction = ", \033[91mpress A to begin your turn please.\033[0m"
        skip_turn_instruction = " Press A to skip them."
        learn_event_instruction = "press A to learn what happened tonight."
    mafia_kill_vote = {}
    # Clear all player targets from the night before
    for player in playerList:
        player.target = None
    for player in playerList:
        if player.living:
            # Prompt the user to begin their turn
            woosh2.play()
            print("{}{}".format(player.name, begin_turn_instruction))
            press_enter_key()
            os.system('cls')
            # Inform the user about what they are and what they do
            print("\033[33mIt is night number {0}.\033[0m".format(night_number))
            night_type_writer("Good evening " + Fore.LIGHTMAGENTA_EX + player.name + Fore.RESET + ", you are a " + (
                player.role.role_color()) + str(player.role.name) + Back.RESET + Fore.RESET + ".")
            print("You are {0}".format(player.role.description))
            print(" ")
            # Print how many more uses of a night ability the player has (if any)
            if player.uses != 666:
                print(Fore.LIGHTRED_EX + "Remaining night ability uses: {}".format(player.uses) + Fore.RESET)
            # Print a list of players in the users team (if any)
            if player in teamDict["Mafia"]:
                if player.role.alignment == "Mafia":
                    print_remaining_players("MAFIA")
            if player.role.name == "Serial Killer":
                print(Fore.LIGHTRED_EX + "Select one person to attempt to kill tonight by selecting their name:" + Fore.RESET)
                print("-" * SCREEN_WIDTH)
                print_remaining_players()
                # Check to make sure the input is actually a number
                serial_killer_target = get_user_night_action_input(player)
                if serial_killer_target == "S":
                    # TODO: Clean up these "Press Enter/A" statements, they are extremely inefficient and sloppy
                    print("You will stay inside with your pet cat 'Clumpy' tonight, " + Fore.LIGHTRED_EX + end_turn_instruction + Fore.RESET)
                    press_enter_key()
                    os.system('cls')
                    player.target = None
                else:
                    print("You went to kill {0} tonight, ".format(playerList[serial_killer_target].name) + Fore.LIGHTRED_EX + end_turn_instruction + Fore.RESET)
                    player.target = get_player_target(serial_killer_target)
                    press_enter_key()
                    os.system('cls')
            elif player.role.name == "Godfather":
                # How much the role's vote is worth
                mafia_vote_value = 2
                print(Fore.LIGHTRED_EX + "Vote on one person for the mafia to hit tonight by selecting their name:" + Fore.RESET)
                print("-" * SCREEN_WIDTH)
                print_remaining_players()
                # Check to make sure the input is actually a number
                godfather_target = get_user_night_action_input(player)
                # Convert the target (int) to a player object
                if godfather_target == "S":
                    print("You voted to skip the night tonight.                            ")
                else:
                    print("You voted to kill {0} tonight, ".format(playerList[godfather_target].name) + Fore.LIGHTRED_EX + end_turn_instruction + Fore.RESET)
                godfather_vote_target = get_player_target(godfather_target)
                # Nobody in the mafia has voted yet
                if bool(mafia_kill_vote) is False:
                    mafia_kill_vote.update({godfather_vote_target : mafia_vote_value})
                else:
                    # Someone else has already voted to kill this person
                    if godfather_vote_target in mafia_kill_vote:
                        local_vote_value = mafia_kill_vote[godfather_vote_target]
                        # Add the godfathers vote value to the previous vote value
                        local_vote_value += mafia_vote_value
                        # Update the votes towards the target in the dictionary
                        mafia_kill_vote.update({godfather_vote_target : local_vote_value})
                press_enter_key()
                os.system('cls')
            elif player.role.name == "Mafioso":
                # How much the role's vote is worth
                mafia_vote_value = 2
                print(Fore.LIGHTRED_EX + "Vote on one person for the mafia to hit tonight by selecting their name:" + Fore.RESET)
                print("-" * SCREEN_WIDTH)
                print_remaining_players()
                # Check to make sure the input is actually a number
                mafioso_target = get_user_night_action_input(player)
                # Convert the target (int) to a player object
                if mafioso_target == "S":
                    print("You voted to skip the night tonight.                            ")
                else:
                    print("You voted to kill {0} tonight, ".format(playerList[mafioso_target].name) + Fore.LIGHTRED_EX + end_turn_instruction + Fore.RESET)
                mafioso_vote_target = get_player_target(mafioso_target)
                # Nobody in the mafia has voted yet
                if bool(mafia_kill_vote) is False:
                    mafia_kill_vote.update({mafioso_vote_target : mafia_vote_value})
                else:
                    # Someone else has already voted to kill this person
                    if mafioso_vote_target in mafia_kill_vote:
                        local_vote_value = mafia_kill_vote[mafioso_vote_target]
                        # Add the mafiosos vote value to the previous vote value
                        local_vote_value += mafia_vote_value
                        # Update the votes towards the target in the dictionary
                        mafia_kill_vote.update({mafioso_vote_target : local_vote_value})
                press_enter_key()
                os.system('cls')
            elif player.role.name == "Consort":
                mafia_vote_value = 1
                print(" ")
                print(Fore.LIGHTRED_EX + "Select one person to attempt to distract tonight by selecting their name:" + Fore.RESET)
                print("-" * SCREEN_WIDTH)
                print_remaining_players()
                # Check to make sure the input is actually a number
                consort_target = get_user_night_action_input(player)
                if consort_target == "S":
                    local_decision_notifier = ("You will stay inside with your pet cat 'Bubble' tonight, " + Fore.LIGHTRED_EX + end_turn_instruction + Fore.RESET)
                    player.target = None
                else:
                    local_decision_notifier = ("You went to distract {0} tonight, ".format(playerList[consort_target].name) + Fore.LIGHTRED_EX + end_turn_instruction + Fore.RESET)
                    player.target = get_player_target(consort_target)
                os.system('cls')
                print(local_decision_notifier)
                print(Fore.LIGHTRED_EX + "Vote on one person for the mafia to hit tonight by selecting their name:" + Fore.RESET)
                print("-" * SCREEN_WIDTH)
                print_remaining_players()
                # Check to make sure the input is actually a number
                consort_vote_target = get_user_night_action_input(player)
                if consort_vote_target == "S":
                    print("You voted to skip the night tonight.                            ")
                else:
                    print("You voted to kill {0} tonight, ".format(playerList[consort_vote_target].name) + Fore.LIGHTRED_EX + end_turn_instruction + Fore.RESET)
                consort_vote_target = get_player_target(consort_vote_target)
                # Nobody in the mafia has voted yet
                if bool(mafia_kill_vote) is False:
                    mafia_kill_vote.update({consort_vote_target: mafia_vote_value})
                else:
                    # Someone else has already voted to kill this person
                    if consort_vote_target in mafia_kill_vote:
                        local_vote_value = mafia_kill_vote[consort_vote_target]
                        # Add the godfathers vote value to the previous vote value
                        local_vote_value += mafia_vote_value
                        # Update the votes towards the target in the dictionary
                        mafia_kill_vote.update({consort_vote_target: local_vote_value})
                press_enter_key()
                os.system('cls')
            elif player.role.name == "Agent":
                mafia_vote_value = 1
                print(" ")
                print(Fore.LIGHTRED_EX + "Select one person to attempt to watch tonight by selecting their name:" + Fore.RESET)
                print("-" * SCREEN_WIDTH)
                print_remaining_players()
                # Check to make sure the input is actually a number
                agent_target = get_user_night_action_input(player)
                if agent_target == "S":
                    local_decision_notifier = ("You will stay inside with your pet cat 'Lana' tonight, " + Fore.LIGHTRED_EX + end_turn_instruction + Fore.RESET)
                    player.target = None
                else:
                    local_decision_notifier= ("You went to watch {0} tonight, ".format(playerList[agent_target].name) + Fore.LIGHTRED_EX + end_turn_instruction + Fore.RESET)
                    player.target = get_player_target(agent_target)
                os.system('cls')
                print(local_decision_notifier)
                print(Fore.LIGHTRED_EX + "Vote on one person for the mafia to hit tonight by selecting their name:" + Fore.RESET)
                print("-" * SCREEN_WIDTH)
                print_remaining_players()
                # Check to make sure the input is actually a number
                agent_vote_target = get_user_night_action_input(player)
                if agent_vote_target == "S":
                    print("You voted to skip the night tonight.                            ")
                else:
                    print("You voted to kill {0} tonight, ".format(playerList[agent_vote_target].name) + Fore.LIGHTRED_EX + end_turn_instruction + Fore.RESET)
                agent_vote_target = get_player_target(agent_vote_target)
                # Nobody in the mafia has voted yet
                if bool(mafia_kill_vote) is False:
                    mafia_kill_vote.update({agent_vote_target: mafia_vote_value})
                else:
                    # Someone else has already voted to kill this person
                    if agent_vote_target in mafia_kill_vote:
                        local_vote_value = mafia_kill_vote[agent_vote_target]
                        # Add the godfathers vote value to the previous vote value
                        local_vote_value += mafia_vote_value
                        # Update the votes towards the target in the dictionary
                        mafia_kill_vote.update({agent_vote_target: local_vote_value})
                press_enter_key()
                os.system('cls')
            elif player.role.name == "Citizen":
                # TODO: Add functionality to this, he cannot use his vest yet.
                print(" ")
                print("You can't do anything at night, but " + Fore.LIGHTRED_EX + "press some random button to make people think you can." + Fore.RESET)
                press_enter_key()
                print("Good job," + Fore.LIGHTRED_EX + end_turn_instruction + Fore.RESET)
                player.target = None
                press_enter_key()
                os.system('cls')
            elif player.role.name == "Mayor":
                print(" ")
                print("You can't do anything at night, but " + Fore.LIGHTRED_EX + "press some random button to make people think you can." + Fore.RESET)
                press_enter_key()
                print("Good job," + Fore.LIGHTRED_EX + end_turn_instruction + Fore.RESET)
                player.target = None
                press_enter_key()
                os.system('cls')
            elif player.role.name == "Bodyguard":
                print(" ")
                print(Fore.LIGHTRED_EX + "Select one person to attempt to guard tonight by selecting their name:" + Fore.RESET)
                print("-" * SCREEN_WIDTH)
                print_remaining_players()
                # Check to make sure the input is actually a number
                bodyguard_target = get_user_night_action_input(player)
                if bodyguard_target == "S":
                    print("You will stay inside with your pet cat 'Shadow' tonight, " + Fore.LIGHTRED_EX + end_turn_instruction + Fore.RESET)
                    press_enter_key()
                    os.system('cls')
                    player.target = None
                else:
                    print("You went to guard {0} tonight, ".format(playerList[bodyguard_target].name) + Fore.LIGHTRED_EX + end_turn_instruction + Fore.RESET)
                    player.target = get_player_target(bodyguard_target)
                    press_enter_key()
                    os.system('cls')
            elif player.role.name == "Escort":
                print(" ")
                print(Fore.LIGHTRED_EX + "Select one person to attempt to distract tonight by selecting their name:" + Fore.RESET)
                print("-" * SCREEN_WIDTH)
                print_remaining_players()
                # Check to make sure the input is actually a number
                escort_target = get_user_night_action_input(player)
                if escort_target == "S":
                    print("You will stay inside with your pet cat 'Bubble' tonight, " + Fore.LIGHTRED_EX + end_turn_instruction + Fore.RESET)
                    press_enter_key()
                    os.system('cls')
                    player.target = None
                else:
                    print("You went to distract {0} tonight, ".format(playerList[escort_target].name) + Fore.LIGHTRED_EX + end_turn_instruction + Fore.RESET)
                    player.target = get_player_target(escort_target)
                    press_enter_key()
                    os.system('cls')
            elif player.role.name == "Lookout":
                print(" ")
                print(Fore.LIGHTRED_EX + "Select one person to attempt to watch tonight by selecting their name:" + Fore.RESET)
                print("-" * SCREEN_WIDTH)
                print_remaining_players()
                # Check to make sure the input is actually a number
                lookout_target = get_user_night_action_input(player)
                if lookout_target == "S":
                    print("You will stay inside with your pet cat 'Lana' tonight, " + Fore.LIGHTRED_EX + end_turn_instruction + Fore.RESET)
                    press_enter_key()
                    os.system('cls')
                    player.target = None
                else:
                    print("You went to watch {0} tonight, ".format(playerList[lookout_target].name) + Fore.LIGHTRED_EX + end_turn_instruction + Fore.RESET)
                    player.target = get_player_target(lookout_target)
                    press_enter_key()
                    os.system('cls')
            elif player.role.name == "Sheriff":
                print(" ")
                print(Fore.LIGHTRED_EX + "Select one person to attempt to search tonight by selecting their name:" + Fore.RESET)
                print("-" * SCREEN_WIDTH)
                print_remaining_players()
                # Check to make sure the input is actually a number
                sheriff_target = get_user_night_action_input(player)
                if sheriff_target == "S":
                    print("You will stay inside with your pet dog 'Luna' tonight, " + Fore.LIGHTRED_EX + end_turn_instruction + Fore.RESET)
                    press_enter_key()
                    os.system('cls')
                    player.target = None
                else:
                    print("You went to investigate {0} tonight, ".format(playerList[sheriff_target].name) + Fore.LIGHTRED_EX + end_turn_instruction + Fore.RESET)
                    player.target = get_player_target(sheriff_target)
                    press_enter_key()
                    os.system('cls')
            elif player.role.name == "Vigilante":
                print(" ")
                print(Fore.LIGHTRED_EX + "Select one person to attempt to shoot tonight by selecting their name:" + Fore.RESET)
                print("-" * SCREEN_WIDTH)
                print_remaining_players()
                # Check to make sure the input is actually a number
                vigilante_target = get_user_night_action_input(player)
                if vigilante_target == "S":
                    print("You will stay inside with your pet cat 'Max' tonight, " + Fore.LIGHTRED_EX + end_turn_instruction + Fore.RESET)
                    press_enter_key()
                    os.system('cls')
                    player.target = None
                else:
                    print("You went to shoot {0} tonight, ".format(playerList[vigilante_target].name) + Fore.LIGHTRED_EX + end_turn_instruction + Fore.RESET)
                    player.target = get_player_target(vigilante_target)
                    press_enter_key()
                    os.system('cls')
            elif player.role.name == "Doctor":
                print(" ")
                print(Fore.LIGHTRED_EX + "Select one person to attempt to heal tonight by selecting their name:" + Fore.RESET)
                print("-" * SCREEN_WIDTH)
                print_remaining_players()
                # Check to make sure the input is actually a number
                doctor_target = get_user_night_action_input(player)
                if doctor_target == "S":
                    print("You will stay inside with your pet dog 'Rex' tonight, " + Fore.LIGHTRED_EX + end_turn_instruction + Fore.RESET)
                    press_enter_key()
                    os.system('cls')
                    player.target = None
                else:
                    print("You went to heal {0} tonight, ".format(playerList[doctor_target].name) + Fore.LIGHTRED_EX + end_turn_instruction + Fore.RESET)
                    player.target = get_player_target(doctor_target)
                    press_enter_key()
                    os.system('cls')
        else:
            # TODO: Add stuff for dead people to do.
            pass
    for player in playerList:
        if player.role.name == "Godfather":
            if player.living:
                # Set the Godfather target to the user with the most votes
                player.target = max(mafia_kill_vote, key=mafia_kill_vote.get)
        elif player.role.name == "Mafioso":
            if player.living:
                player.target = max(mafia_kill_vote, key=mafia_kill_vote.get)
    # Player night_ability execution, create randomized form of player list to make things fair
    randomized_player_list = playerList.copy()
    random.shuffle(randomized_player_list)
    # randomized_player_list contains a shuffled version of playerList before that gets sorted by priority
    sorted_player_list = sorted(randomized_player_list, key=lambda x: x.role.priority, reverse=False)
    # sorted_player_list contains the roles sorted based on priority
    os.system('cls')
    dayTime.play()
    print("Tonight's events will now transpire...")
    fade_out(nightPlayer)
    sleep(4)
    os.system('cls')
    for player in sorted_player_list:
            if player.target is None or player.target == "NULL":
                # Player decided to skip the night or cannot do anything
                pass
            else:
                commit_role_action(player)
    # Night phase one is complete and role actions have been executed, now output user night info
    os.system('cls')
    chatSound.play()
    print("Tonight's events have concluded, \033[91mplease close your eyes\033[0m so you may learn what transpired last night.")
    sleep(1)
    goodNightBell.play()
    sleep(3)
    os.system('cls')
    for player in playerList:
        if player in permaDeathList:
            pass
        else:
            woosh2.play()
            print(player.name + ", " + Fore.LIGHTRED_EX + learn_event_instruction + Fore.RESET)
            press_enter_key()
            os.system('cls')
            if not player.info:
                print("Nothing exciting happened to you tonight, but at least you're alive right?")
            else:
                for info in player.info:
                    print(info)
                if not player.living:
                    # Check to see if the player was the Godfather
                    mafioso_replacement(player)
                    # This player is now 100% dead
                    permaDeathList.append(player)
            print(Fore.LIGHTRED_EX + end_turn_instruction_2 + Fore.RESET)
            press_enter_key()
            os.system('cls')
    # The night has concluded
    night_number += 1
    return night_number


def day_sequence(day_number):
    dayAmbientPlayer.queue(daySounds)
    nightAmbientPlayer.pause()
    dayAmbientPlayer.play()
    day_number += 1
    os.system('cls')
    print("\033[33mDay number {0}.\033[0m".format(day_number))
    # Generate a list of the remaining players
    local_remaining_players = []
    for local_player in playerList:
        # Clear the player info from the night before
        local_player.info = []
        if local_player.living:
            local_remaining_players.append(local_player)
    dayTime.play()
    sleep(3)
    if len(deathList) >= 4:
        chatSound.play()
        print("\033[41mMany of us perished in the night...\033[0m")
    elif len(deathList) >= 2:
        chatSound.play()
        print("\033[31mSome of us perished in the night...\033[0m")
    elif len(deathList) == 1:
        chatSound.play()
        print("\033[91mOne of us perished in the night...\033[0m")
    else:
        print("Fortunately, \033[32mnobody was found dead last night\033[0m.")
    sleep(4)
    for player in deathList:
        deathNotification.play()
        print("-" * SCREEN_WIDTH)
        print("\033[94m{0}\033[0m was found dead last night.".format(player.name))
        sleep(1)
        print()
        chatSound.play()
        print(player.death_description)
        sleep(1)
        print(" ")
        # TODO: Color the role name here
        roleReveal.play()
        sleep(1)
        print("Their role was " + (player.role.role_color()) + "{0}\033[0m".format(player.role.name) + ".")
        sleep(2.5)
    sleep(3)
    countdown_timer = 25
    start_time = perf_counter()
    new_time_difference = perf_counter()
    # Clear the previous queue and initialize a new one
    clear_playlist(dayPlayer)
    dayPlayer.queue(dayMusicList[0])
    dayPlayer.queue(dayMusicList[0])
    dayPlayer.queue(dayMusicList[0])
    dayPlayer.play()
    while countdown_timer >= 0:
        if not keyboardController:
            # Countdown timer is used differently here than it was in keyboard version (sorry patience ran out)
            # This entire section is a complete disasterous mess that somehow works
            # TODO: Clean up this abomination at some point
            current_time = perf_counter()
            time_difference = ceil(current_time) - ceil(start_time)
            actual_time_difference = countdown_timer - time_difference
            if new_time_difference < time_difference:
                os.system('cls')
                print("\033[91mDiscuss anything you may have learned last night or any suspicions you may have.\033[0m")
                print("You will vote after deliberation on who to hang.")
                print(" ")
                if globalDebug:
                    print("Time left to deliberate: \033[1m{} seconds\033[0m".format(actual_time_difference))
                else:
                    print("Time left to deliberate: \033[1m{} seconds\033[0m".format(actual_time_difference), end='\r')
            if actual_time_difference <= 0:
                break
            local_input = xboxController.sample_first_joystick()
            if local_input == [13, 1]:
                local_deliberation_options = ["\033[96mSKIP ENTIRE DAY\033[0m", "\033[96mSKIP DELIBERATION\033[0m", "\033[96mCONTINUE DELIBERATION\033[0m"]
                os.system('cls')
                if globalDebug:
                    print("Time left to deliberate: \033[1m{} seconds\033[0m".format(actual_time_difference))
                else:
                    print("Time left to deliberate: \033[1m{} seconds\033[0m".format(actual_time_difference), end='\r')
                chatSound.play()
                print(
                    "\033[91mPlease select an option from the menu below.\033[0m.")
                i = user_day_input(local_deliberation_options)
                if i == 1:
                    chatSound.play()
                    print("\033[45mYou have opted to skip deliberation and go straight to the gallows.\033[0m")
                    sleep(1.5)
                    break
                elif i == 0:
                    end_day()
                    return day_number
            new_time_difference = time_difference
        if keyboardController:
            current_time = perf_counter()
            time_difference = ceil(current_time) - ceil(start_time)
            actual_time_difference = countdown_timer - time_difference
            if new_time_difference < time_difference:
                os.system('cls')
                print("\033[91mDiscuss anything you may have learned last night or any suspicions you may have.\033[0m")
                print("You will vote after deliberation on who to hang.")
                print(" ")
                if globalDebug:
                    print("Time left to deliberate: \033[1m{} seconds\033[0m".format(actual_time_difference))
                else:
                    print("Time left to deliberate: \033[1m{} seconds\033[0m".format(actual_time_difference), end='\r')
            if actual_time_difference <= 0:
                break
            if kbhit():
                local_deliberation_options = ["SKIP ENTIRE DAY", "SKIP DELIBERATION", "CONTINUE DELIBERATION"]
                os.system('cls')
                if globalDebug:
                    print("Time left to deliberate: \033[1m{} seconds\033[0m".format(actual_time_difference))
                else:
                    print("Time left to deliberate: \033[1m{} seconds\033[0m".format(actual_time_difference), end='\r')
                chatSound.play()
                print(
                    "\033[91mPlease select an option from the menu below.\033[0m.")
                i = user_day_input(local_deliberation_options)
                if i == 1:
                    chatSound.play()
                    print("\033[45mYou have opted to skip deliberation and go straight to the gallows.\033[0m")
                    sleep(1.5)
                    break
                elif i == 0:
                    end_day()
                    return day_number
                else:
                    end_time = perf_counter()
                    lost_time = int(end_time) - int(start_time)
                    countdown_timer -= int(lost_time)
                    pass
            new_time_difference = time_difference
    vote_number = 1
    if len(local_remaining_players) < 4:
        clear_playlist(trialPlayer)
        trialPlayer.queue(questioningMusicINTENSE)
    else:
        clear_playlist(trialPlayer)
        trialPlayer.queue(questioningMusic)
    while vote_number <= 2:
        os.system('cls')
        chatSound.play()
        if vote_number == 2:
            print("There is still time to prosecute one more person...")
            dayPlayer.play()
            if len(local_remaining_players) < 4:
                clear_playlist(trialPlayer)
                trialPlayer.queue(questioningMusicINTENSE)
            else:
                clear_playlist(trialPlayer)
                trialPlayer.queue(questioningMusic)
        print("Who has the town selected to put on trial?")
        print("-" * SCREEN_WIDTH)
        print_remaining_players("Day")
        # Get desired target from town
        player_number = get_town_trial_vote()
        if player_number == "S":
            # Players have opted to skip the vote
            voteSound.play()
            print("\033[45mThe town has selected to skip the day.\033[0m                                       ")
            sleep(3)
            end_day()
            return day_number
        # Convert target number into player object
        local_day_player = get_player_target(player_number)
        voteSound.play()
        print("The town has selected to place {} on trial. Their defense will now begin.".format(local_day_player.name))
        sleep(3)
        countdown_timer = 2
        dayPlayer.pause()
        trialPlayer.play()
        while countdown_timer >= 0:
            os.system('cls')
            print("{}, you stand accused of conspiring against the town.".format(local_day_player.name))
            print("{}, you have \033[1m{} seconds\033[0m to defend yourself.".format(local_day_player.name, countdown_timer))
            print("\033[41mNo-one else may speak during this period.\033[0m")
            countdown_timer -= 1
            sleep(1)
        countdown_timer = 2
        chatSound2.play()
        while countdown_timer >= 0:
            os.system('cls')
            print("The remaining town members have \033[1m{} seconds\033[0m to deliberate.".format(countdown_timer))
            print("Voters may abstain.")
            print("\033[41mAll may now speak including the defendant.\033[0m")
            countdown_timer -= 1
            sleep(1)
        os.system('cls')
        # Remove the player on trial from remaining players list
        local_remaining_players.remove(local_day_player)
        # Get the number of users who voted innocent
        completed_vote = get_user_verdict_input(local_remaining_players, local_day_player)
        # Get the number of users who voted guilty
        voteComplete.play()
        trialPlayer.pause()
        os.system('cls')
        print("The votes have been collected and counted...")
        sleep(4)
        if completed_vote.upper() == "GUILTY":
            # Player was found guilty
            print("The town has found {} \033[31mGUILTY\033[0m of the accusations made against them.".format(local_day_player.name))
            guiltyVerdict.play()
            # TODO: Add execution methods
            sleep(2)
            last_word_countdown = 8
            while last_word_countdown >= 0:
                os.system('cls')
                print("If you have any last words {0}, you may speak them now".format(local_day_player.name))
                print("Time remaining: {} seconds".format(last_word_countdown))
                sleep(1)
                last_word_countdown -= 1
            hangedSound.play()
            print("{} has been \033[31mHANGED\033[0m.".format(local_day_player.name))
            local_day_player.living = False
            # The player is now 100% dead
            # Check to see if they were the Godfather and if they were, replace them
            mafioso_replacement(local_day_player)
            permaDeathList.append(local_day_player)
            sleep(2)
            roleReveal.play()
            sleep(1)
            print("Their role was " + (local_day_player.role.role_color()) + "{0}\033[0m.".format(local_day_player.role.name))
            sleep(5)
            end_day()
            return day_number
        elif completed_vote.upper() == "INNOCENT":
            # Player was found innocent
            print("The town has found {} \033[32mINNOCENT\033[0m of the accusations made against them.".format(local_day_player.name))
            votedInnocent.play()
            vote_number += 1
            local_remaining_players.append(local_day_player)
            sleep(5)
        elif completed_vote.upper() == "DRAW":
            # Player was found innocent, but through an even vote
            print("\033[45mThere was a draw.\033[0m")
            print("The town has found {} \033[32mINNOCENT\033[0m of the accusations made against them.".format(local_day_player.name))
            votedInnocent.play()
            vote_number += 1
            local_remaining_players.append(local_day_player)
            sleep(5)
        else:
            # Player was found innocent
            print("The town has found {} \033[32mINNOCENT\033[0m of the accusations made against them.".format(local_day_player.name))
            votedInnocent.play()
            vote_number += 1
            sleep(5)
        trialPlayer.next_source()
    end_day()
    return day_number


# Checks to see if the victory conditions have been met
def check_victory_conditions():
    victory_condition = None
    # Step 1. Check to see how many players are left
    remaining_players = []
    remaining_mafia = []
    remaining_town = []
    remaining_sk = []
    for local_overall_player in playerList:
        if local_overall_player.living:
            remaining_players.append(local_overall_player)
    # Step 2. Identify the remaining player's affiliations
    for local_remaining_player in remaining_players:
        if local_remaining_player.role.alignment == "Serial Killer":
            remaining_sk.append(local_remaining_player)
        elif local_remaining_player.role.alignment == "Mafia":
            remaining_mafia.append(local_remaining_player)
        else:
            remaining_town.append(local_remaining_player)
    # Step 3. Figure out who has won (if anyone)
    # The SK and Mafia are all dead, Town wins
    if remaining_town and not remaining_sk and not remaining_mafia:
        victory_condition = "Town"
        return victory_condition
    # The SK is dead but the Mafia is still alive and holds majority, Mafia wins
    elif not remaining_sk and len(remaining_town) < len(remaining_mafia):
        victory_condition = "Mafia"
        return victory_condition
    # The Mafia are all dead and the SK holds majority, SK wins
    elif not remaining_mafia and len(remaining_town) <= len(remaining_sk):
        victory_condition = "Serial Killer"
        return victory_condition
    # The game is still going on, nobody wins yet
    else:
        return victory_condition


########################################################################################################################
# UTILITY
########################################################################################################################


# Initialize global lists to store what roles apply to which type
townGovernmentRoles = []
townProtectiveRoles = []
townInvestigativeRoles = []
townKillingRoles = []
neutralKillingRoles = []
mafiaKillingRoles = []
mafiaSupportRoles = []

# Clears the playlist queue
def clear_playlist(audio_player):
    # How many items in the queue the function will skip, can be infinite
    local_skips = 10
    while local_skips != 0:
        audio_player.next_source()
        local_skips -= 1


# Gradually decreases the volume level of a selected track
def fade_out(audio_player, local_type="reset"):
    while audio_player.volume > 0:
        audio_player.volume -= .005
        sleep(.02)
    audio_player.pause()
    if local_type == "reset":
        while audio_player.volume < 1:
            audio_player.volume += .005


# Gradually increases the volume level of a selected track
def fade_in(audio_player):
    audio_player.play()
    while audio_player.volume < 1:
        audio_player.volume += .005
        sleep(.02)


# Initialize global lists to store what roles apply to which type
priority0Roles = []
priority1Roles = []
priority2Roles = []
priority3Roles = []


def end_day():
    os.system('cls')
    dayEnd.play()
    trialPlayer.pause()
    dayPlayer.pause()
    print("\033[33mThe hour is too late to continue, we shall reconvene tomorrow...\033[0m")
    sleep(3)
    goodNightBell.play()
    print("\033[91mPlease close your eyes\033[0m so the night may begin.")
    sleep(3)
    os.system('cls')


# Build a dictionary containing keys with corresponding lists of all the players in each respective team
def generate_teams_dict():
    local_mafia_team_list = []
    local_town_team_list = []
    for local_player in playerList:
        if local_player.role.alignment == "Mafia":
            local_mafia_team_list.append(local_player)
        if local_player.role.alignment == "Town":
            local_town_team_list.append(local_player)
    local_team_list_dictionary = {
                                  "Mafia": local_mafia_team_list,
                                  "Town": local_town_team_list,
                                  }
    return local_team_list_dictionary

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


########################################################################################################################
# GAME MECHANIC FUNCTIONS
########################################################################################################################


# Checks to see if a player who died was the godfather and replaces him if he was
def mafioso_replacement(player):
    # If the godfather is dead at this point, choose a mafia member to make into a mafioso
    if player.role.name == "Godfather" or player.role.name == "Mafioso":
        local_mafia_list = []
        for local_player in playerList:
            if local_player.living:
                if local_player.role.alignment == "Mafia":
                    # This player is alive and in the mafia, a possible candidate
                    local_mafia_list.append(local_player)
        # Check to see if there's anything in this list since random.choice doesn't like empty lists
        if local_mafia_list:
            # Set this player's role to mafioso
            local_selected_mafia = random.choice(local_mafia_list)
            local_selected_mafia.role = scriptedMafiaRole[0]
            return


# Identify and define users, instantiating their classes
def user_identification():
    i = 0
    player_list = []
    player_list.append(Player("\033[94mAlex\033[0m", "Alex", 0, None, True, {}, "NULL", "NULL", [], [], "NULL", 0, "NULL"))
    player_list.append(Player("\033[94mMaddie\033[0m", "Maddie", 1, None, True, {}, "NULL", "NULL", [], [], "NULL", 0, "NULL"))
    player_list.append(Player("\033[94mTyler\033[0m", "Tyler",  2, None, True, {}, "NULL", "NULL", [], [], "NULL", 0, "NULL"))
    player_list.append(Player("\033[94mWill\033[0m", "Will",  3, None, True, {}, "NULL", "NULL", [], [], "NULL", 0, "NULL"))
    player_list.append(Player("\033[94mJason\033[0m", "Jason", 4, None, True, {}, "NULL", "NULL", [], [], "NULL", 0, "NULL"))
    player_list.append(Player("\033[94mAndrew\033[0m", "Andrew", 5, None, True, {}, "NULL", "NULL", [], [], "NULL", 0, "NULL"))
    player_list.append(Player("\033[94mGillian\033[0m", "Gillian", 6, None, True, {}, "NULL", "NULL", [], [], "NULL", 0, "NULL"))
    player_list.append(Player("\033[94mNick\033[0m", "Nick",  7, None, True, {}, "NULL", "NULL", [], [], "NULL", 0, "NULL"))
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


# Prompts the user to press the enter key (A button on Xbox Controller)
def press_enter_key():
    if keyboardController:
        input()
    else:
        while True:
            local_input = xboxController.sample_first_joystick()
            if local_input == [13, 1]:
                break


# Adjusts the current index selection value based on which key has been pressed
def change_option(key_answer, starting_selection, local_options):
    if key_answer.upper() == "UP":
        starting_selection += 1
        if starting_selection > (len(local_options)-1):
            new_selection = 0
            return new_selection
        else:
            new_selection = starting_selection
            return new_selection
    if key_answer.upper() == "DOWN":
        starting_selection -= 1
        if starting_selection < 0:
            new_selection = (len(local_options)-1)
            return new_selection
        else:
            new_selection = starting_selection
            return new_selection


# Checks for keypresses, reads which keys are pressed
def keypress(old_selection, local_options):
    while True:
        # If input mode in config is set to keyboard
        if keyboardController:
            if kbhit():
                keycode = ord(getch())
                if keycode == 13:  # Enter
                    return old_selection
                elif keycode == 224:  # Special keys (arrows, f keys, ins, del, etc.)
                    keycode = ord(getch())
                    if keycode == 80:  # Down arrow
                        return change_option("Down", old_selection, local_options)
                    elif keycode == 72:  # Up arrow
                        return change_option("Up", old_selection, local_options)
        # Input mode in config must be set to controller
        else:
            local_input = xboxController.sample_first_joystick()
            if local_input == [13, 1]:
                return old_selection  # Enter key aka "A" button
            elif local_input == [65, 0] or local_input == [2, 1] or local_input == [9, 1]:
                return change_option("Down", old_selection, local_options)  # Down arrow aka down left stick
            elif local_input == [66, 0] or local_input == [1, 1] or local_input == [10, 1]:
                return change_option("Up", old_selection, local_options)  # Up arrow aka up left stick


# Returns the player number of the selected target
# ONLY COMPATIBLE WITH WINDOWS CONSOLE WHEN IN KEYBOARD MODE
def user_target_input(local_options):
    selection = random.randrange(0, (len(local_options)))
    while True:
        if selection == len(local_options)-1:
            if globalDebug:
                print("[\033[35m{}\033[0m] is your selection. \033[91mPress enter to submit.\033[0m    ".format(local_options[selection]))
            else:
                print("[\033[35m{}\033[0m] is your selection. \033[91mPress enter to submit.\033[0m    ".format(local_options[selection]), end="\r")
        else:
            if globalDebug:
                print("[{}] is your selection. \033[91mPress enter to submit.\033[0m    ".format(local_options[selection].name))
            else:
                print("[{}] is your selection. \033[91mPress enter to submit.\033[0m    ".format(local_options[selection].name), end="\r")
        new_selection = keypress(selection, local_options)
        if new_selection == selection:
            if new_selection == len(local_options)-1:
                # The selection is the skip string
                new_selection = "S"
                return new_selection
            # Convert the local_options index value to its corresponding player object
            new_selection = local_options[selection]
            # Convert the player object to its integer number (which corresponds with its playerList index value)
            new_selection = new_selection.number
            # Return the player number (int)
            return new_selection
        selection = new_selection


# Returns a number representing an index selection value from a list of targets
# ONLY COMPATIBLE WITH WINDOWS CONSOLE WHEN IN KEYBOARD MODE
def user_day_input(local_options):
    selection = 2
    while True:
        if globalDebug:
            print("[{}] is your selection. \033[91mPress enter to submit.\033[0m    ".format(local_options[selection]))
        else:
            print("[{}] is your selection. \033[91mPress enter to submit.\033[0m    ".format(local_options[selection]), end="\r")
        new_selection = keypress(selection, local_options)
        if new_selection == selection:
            return new_selection
        selection = new_selection


# Assign relevant roles to the users
# Pass this function the playerList and a list containing all relevant roles
def user_role_distribution(players, roles):
    i = 0
    shuffled_roles = random.sample(roles, len(roles))
    for local_player in players:
        local_player.role = shuffled_roles[i]
        local_player.uses = shuffled_roles[i].uses
        i += 1


# Output a list of all players to the user
def print_remaining_players(local_type="Night"):
    if local_type.upper() == "DAY":
        print("[S] \033[95mSKIP THE DAY AND DO NOTHING\033[0m")
    elif local_type.upper() == "MAFIA":
        print("MAFIA TEAM MEMBERS:")
    else:
        print("[S] \033[95mSKIP THE NIGHT AND DO NOTHING\033[0m")
    if local_type.upper() == "MAFIA":
        for local_player in teamDict["Mafia"]:
            if local_player.living:
                if local_player.target == "NULL" or not local_player.target:
                    print("[{0}] \033[94m{1}\033[0m, \033[31m{2}\033[0m".format(local_player.number, local_player.name, local_player.role.name))
                else:
                    print("[{0}] \033[94m{1}\033[0m, \033[31m{2}\033[0m - \033[4mTargeting {3}".format(local_player.number, local_player.name, local_player.role.name, local_player.target.name))
            else:
                print("[X] \033[31m{0}\033[0m, \033[31m{1}\033[0m".format(local_player.raw_name, local_player.role.name))
    else:
        for local_player in playerList:
            if local_player.living:
                print("[{0}] \033[94m{1}\033[0m".format(local_player.number, local_player.name))
            else:
                print("[X] \033[31m{0}\033[0m, {1}".format(local_player.raw_name, (local_player.role.role_color()) + str(local_player.role.name) + Back.RESET + Fore.RESET))
    print("-" * SCREEN_WIDTH)
    print(" ")


# Take the target number recieved from the player and swap it for the corresponding player object
# This is only utilized after "S" has been filtered out. Skips will have already been processed
def get_player_target(target_number):
    # Generate the living player list
    local_living_player_list = []
    if target_number == "S":
        return None
    for local_player in playerList:
        if local_player.living:
            local_living_player_list.append(local_player)
    for player in local_living_player_list:
        if player.number == target_number:
            return player


# Get the vote of "ABSTAIN", "GUILTY" or "INNOCENT" from each player other than the player on trial. Compile results and
# generate a verdict
def get_user_verdict_input(remaining_players, player_on_trial):
    innocent_votes = 0
    guilty_votes = 0
    for local_player in remaining_players:
        os.system('cls')
        print("\033[91mWhoever has the controller will answer for everyone to save time. Votes are public information.\033[0m")
        print("{}, do you believe {} is \033[32minnocent\033[0m or \033[31mguilty\033[0m?".format(local_player.name, player_on_trial.name))
        local_options = ["\033[32mINNOCENT\033[0m", "\033[31mGUILTY\033[0m", "ABSTAIN"]
        vote = user_day_input(local_options)
        if vote == 0:
            # User voted innocent
            innocent_votes += 1
            voteSound.play()
        elif vote == 1:
            # User voted guilty
            guilty_votes += 1
            voteSound.play()
        else:
            # User voted to abstain
            voteSound.play()
            pass
    if guilty_votes > innocent_votes:
        complete_vote = "GUILTY"
    elif guilty_votes == innocent_votes:
        complete_vote = "DRAW"
    else:
        complete_vote = "INNOCENT"
    return complete_vote


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
                elif item == "Mafia Killing":
                    mafiaKillingRoles.append(obj)
                elif item == "Mafia Support":
                    mafiaSupportRoles.append(obj)
                else:
                    print("ERROR: INVALID self.type (Role) PRESENTED TO generate_type_list FUNCTION!")


# Used for filtering user input during the night
def get_user_night_action_input(local_player):
    while True:
        # Generate a list of living players
        living_player_list = []
        for inner_player in playerList:
            if inner_player.living:
                living_player_list.append(inner_player)
        living_player_list.append("SKIP")
        # Returns the player number of the selected target
        local_target = user_target_input(living_player_list)
        # Check to see if user prompted to skip
        if local_target == "S":
            return local_target.upper()
        # The player number is valid (not a necessary check anymore, but why not keep it)
        if int(local_target) < len(playerList) and int(local_target) >= 0:
            # Adjust the local target to make sure its an integer object
            local_target = int(local_target)
            # The player is dead and cannot be targeted
            if not playerList[local_target].living:
                print("That person is dead," + Fore.LIGHTRED_EX + " choose another please." + Fore.RESET)
            else:
                # Create a player object version of the player target (still just an int at this point)
                local_target_player = get_player_target(local_target)
                # The player targeted themselves
                if local_target == local_player.number:
                    for trait in local_player.role.traits:
                        if trait == "Self-Target":
                            return local_target
                    print("You cannot target yourself," + Fore.LIGHTRED_EX + " choose another person please." + Fore.RESET)
                # The target is a member of the mafia
                elif local_target_player in teamDict["Mafia"]:
                    # The player is a member of the mafia
                    if local_player in teamDict["Mafia"]:
                        # The player has self-target
                        for trait in local_player.role.traits:
                            if trait == "Self-Target":
                                # Target the mafia teammate
                                return local_target
                        # The player doesn't have self-target
                        print("You cannot target teammates," + Fore.LIGHTRED_EX + " choose another person please." + Fore.RESET)
                    # The player is not a member of the mafia
                    else:
                        # There's nothing wrong with this person
                        return local_target
                else:
                    # There's nothing wrong with this person
                    return local_target
        else:
            print("That person doesn't exist," + Fore.LIGHTRED_EX + " choose another please." + Fore.RESET)


# Used for retrieving the town vote on who to place on trial during the day
def get_town_trial_vote():
    while True:
        # TODO: This function breaks terribly after the first night. Index of remaining players is super butchered.
        # Generate a list of living players
        living_player_list = []
        for other_player in playerList:
            if other_player.living:
                living_player_list.append(other_player)
        living_player_list.append("SKIP")
        # Returns the player number of the selected target
        local_target = user_target_input(living_player_list)
        # Check to see if user prompted to skip
        if local_target == "S":
            return local_target.upper()
        if int(local_target) < len(playerList) and int(local_target) >= 0:
            local_target = int(local_target)
            if not playerList[local_target].living:
                print("That person is dead," + Fore.LIGHTRED_EX + " choose another please." + Fore.RESET)
            else:
                # There's nothing wrong with this person
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


# Generate a set of roles to be used in this game
def role_generation():
    local_number_of_players = len(playerList)
    # 5 PLYR GAME = 4 TOWN, 1 MAF, 0 SK
    if local_number_of_players == 5:
        local_town_prot = random.choice(townProtectiveRoles)
        local_town_invest = random.choice(townInvestigativeRoles)
        local_town_gov = random.choice(townGovernmentRoles)
        local_town_random = random.choice(random.choice(random.sample((townGovernmentRoles, townInvestigativeRoles, townProtectiveRoles, townKillingRoles), 1)))
        local_town_roles_list = [local_town_prot, local_town_gov, local_town_invest, local_town_random]
        local_godfather = scriptedMafiaRole[1]
        local_mafia_roles_list = [local_godfather]
        return local_town_roles_list, local_mafia_roles_list, None
    # 6 PLYR GAME = 4 TOWN, 2 MAF, 0 SK
    elif local_number_of_players == 6:
        local_town_prot = random.choice(townProtectiveRoles)
        local_town_invest = random.choice(townInvestigativeRoles)
        local_town_gov = random.choice(townGovernmentRoles)
        local_town_random = random.choice(random.choice(random.sample((townGovernmentRoles, townInvestigativeRoles, townProtectiveRoles, townKillingRoles), 1)))
        local_town_roles_list = [local_town_prot, local_town_gov, local_town_invest, local_town_random]
        local_godfather = scriptedMafiaRole[1]
        local_mafia_support = random.choice(mafiaSupportRoles)
        local_mafia_roles_list = [local_godfather, local_mafia_support]
        return local_town_roles_list, local_mafia_roles_list, None
    # 7 PLYR GAME = 4 TOWN, 2 MAF, 1 SK
    elif local_number_of_players == 7:
        local_town_prot = random.choice(townProtectiveRoles)
        local_town_invest = random.choice(townInvestigativeRoles)
        local_town_gov = random.choice(townGovernmentRoles)
        local_town_random = random.choice(random.choice(random.sample((townGovernmentRoles, townInvestigativeRoles, townProtectiveRoles, townKillingRoles), 1)))
        local_town_roles_list = [local_town_prot, local_town_gov, local_town_invest, local_town_random]
        local_godfather = scriptedMafiaRole[1]
        local_mafia_support = random.choice(mafiaSupportRoles)
        local_mafia_roles_list = [local_godfather, local_mafia_support]
        local_serial_killer = neutralKillingRoles
        return local_town_roles_list, local_mafia_roles_list, local_serial_killer
    # 8 PLYR GAME = 5 TOWN, 2 MAF, 1 SK
    elif local_number_of_players == 8:
        local_town_prot = random.choice(townProtectiveRoles)
        local_town_invest = random.choice(townInvestigativeRoles)
        local_town_gov = random.choice(townGovernmentRoles)
        local_town_killing = random.choice(townKillingRoles)
        local_town_random = random.choice(random.choice(random.sample((townGovernmentRoles, townInvestigativeRoles, townProtectiveRoles, townKillingRoles), 1)))
        local_town_roles_list = [local_town_prot, local_town_gov, local_town_invest, local_town_random, local_town_killing]
        local_godfather = scriptedMafiaRole[1]
        local_mafia_support = random.choice(mafiaSupportRoles)
        local_mafia_roles_list = [local_godfather, local_mafia_support]
        local_serial_killer = neutralKillingRoles
        return local_town_roles_list, local_mafia_roles_list, local_serial_killer
    # 9 PLYR GAME = 5 TOWN, 3 MAF, 1 SK
    elif local_number_of_players == 8:
        local_town_prot = random.choice(townProtectiveRoles)
        local_town_invest = random.choice(townInvestigativeRoles)
        local_town_gov = random.choice(townGovernmentRoles)
        local_town_killing = random.choice(townKillingRoles)
        local_town_random = random.choice(random.choice(random.sample((townGovernmentRoles, townInvestigativeRoles, townProtectiveRoles, townKillingRoles), 1)))
        local_town_roles_list = [local_town_prot, local_town_gov, local_town_invest, local_town_random, local_town_killing]
        local_godfather = scriptedMafiaRole[1]
        local_mafia_support1 = random.choice(mafiaSupportRoles)
        local_mafia_support2 = random.choice(mafiaSupportRoles)
        local_mafia_roles_list = [local_godfather, local_mafia_support1, local_mafia_support2]
        local_serial_killer = neutralKillingRoles
        return local_town_roles_list, local_mafia_roles_list, local_serial_killer
    # 10 PLYR GAME = 6 TOWN, 3 MAF, 1 SK
    elif local_number_of_players == 8:
        local_town_prot = random.choice(townProtectiveRoles)
        local_town_invest = random.choice(townInvestigativeRoles)
        local_town_gov = random.choice(townGovernmentRoles)
        local_town_killing = random.choice(townKillingRoles)
        local_town_random1 = random.choice(random.choice(random.sample((townGovernmentRoles, townInvestigativeRoles, townProtectiveRoles, townKillingRoles), 1)))
        local_town_random2 = random.choice(random.choice(random.sample((townGovernmentRoles, townInvestigativeRoles, townProtectiveRoles, townKillingRoles), 1)))
        local_town_roles_list = [local_town_prot, local_town_gov, local_town_invest, local_town_random1, local_town_random2, local_town_killing]
        local_godfather = scriptedMafiaRole[1]
        local_mafia_support1 = random.choice(mafiaSupportRoles)
        local_mafia_support2 = random.choice(mafiaSupportRoles)
        local_mafia_roles_list = [local_godfather, local_mafia_support1, local_mafia_support2]
        local_serial_killer = neutralKillingRoles
        return local_town_roles_list, local_mafia_roles_list, local_serial_killer


########################################################################################################################
# CODE EXECUTION
########################################################################################################################


cursor.hide()
controllerKeyPress = 0

# Generate lists of objects based on type from garbage collection
generate_type_list()

# Generate the sequence of sounds used in the typing sound effect
clickList = generate_click_list()

# Set up the roles for this game
townRolesList, mafiaRolesList, neutralRolesList = role_generation()

# Prompt the users to identify themselves
playerList = user_identification()

# Distribute roles to the players
user_role_distribution(playerList, (neutralRolesList + mafiaRolesList + townRolesList))

teamDict = generate_teams_dict()

# Start the game
startup()

nightNumber = 1
dayNumber = 1

# Create players for the music and ambient sounds
nightPlayer = pyglet.media.Player()
nightAmbientPlayer = pyglet.media.Player()
trialPlayer = pyglet.media.Player()
dayPlayer = pyglet.media.Player()
dayAmbientPlayer = pyglet.media.Player()

# Create lists of the music and ambient sounds to be played
musicList = [nightSequence1, nightSequence2, nightSequence3, nightSequence4, nightSequence5, nightSequence6]
dayMusicList = [day1, day2]
soundsList = [nightSounds1, rainSounds1]
daySoundsList = [daySounds]
random.shuffle(musicList)
random.shuffle(soundsList)

# Begin the day/night cycle
while True:
    nightNumber = night_sequence(nightNumber)
    victoryCondition = check_victory_conditions()
    if victoryCondition is not None:
        break
    random.shuffle(dayMusicList)
    dayNumber = day_sequence(dayNumber)
    victoryCondition = check_victory_conditions()
    if victoryCondition is not None:
        break

victoryAnnounce.play()
print("We have come to a conclusion...")
print(" ")
sleep(6.8)
if victoryCondition == "Mafia":
    endingMusicMafia.play()
    print("VICTORY FOR THE \033[31m{}\033[0m".format(victoryCondition.upper()))
elif victoryCondition == "Town":
    endingMusicTown.play()
    print("VICTORY FOR THE \033[32m{}\033[0m".format(victoryCondition.upper()))
elif victoryCondition == "Serial Killer":
    endingMusicSerialKiller.play()
    print("VICTORY FOR THE \033[45m{}\033[0m".format(victoryCondition.upper()))
else:
    print("ERROR: INVALID VICTORY CONDITION")
sleep(2)
winnerList = []
for players in playerList:
    if players.role.alignment == victoryCondition:
        winnerList.append(players)
sleep(1)
print(" ")
print("Congratulations to:")
for local_players in winnerList:
    woosh3.play()
    print("{0} for winning as {1}".format(local_players.name, (local_players.role.role_color()) + str(local_players.role.name) + Back.RESET + Fore.RESET + "."))
    print(" ")
    sleep(.5)

# Prevent the screen from closing
input()
# Reveal the cursor again
cursor.show()
