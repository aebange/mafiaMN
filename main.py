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
# GAME LOOP FUNCTIONS
########################################################################################################################

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
    print("\033[91mPlease close your eyes\033[0m so the first night may begin.")
    sleep(5)
    os.system('cls')


# Run through the night
def night_sequence(night_number):
    print("NIGHT NUMBER {}".format(night_number))
    desired_track = (musicList[night_number])
    sleep(.5)
    print("SKIPPED SONG.")
    nightPlayer.next_source()
    sleep(.5)
    print("QUEING {}".format(str(desired_track)))
    nightPlayer.queue(desired_track)
    sleep(.5)
    print("ATTEMPTING TO START PLAYER")
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
            print("\033[33mIt is night number {0}.\033[0m".format(night_number))
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
    chatSound.play()
    print("Tonight's events have concluded, \033[91mplease close your eyes\033[0m so you may learn what transpired last night.")
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
    print("\033[33mDay number {0}.\033[0m".format(day_number))
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
        print("Fortunately, \033[32mnobody was found dead last night.\033[0m")
    sleep(4)
    for player in deathList:
        deathNotification.play()
        print("\033[94m{0}\033[0m was found dead last night.".format(player.name))
        sleep(3)
        print(" ")
        # TODO: Color the role name here
        roleReveal.play()
        sleep(1)
        print("Their role was " + (player.role.role_color())+ "{0}\033[0m".format(player.role.name))
        sleep(4)
    countdown_timer = 65
    while countdown_timer >= 0:
        mins, secs = divmod(countdown_timer,60)
        time_format = '{:02d}:{:02d}'.format(mins, secs)
        if countdown_timer == 60:
            os.system('cls')
            print("Time left to deliberate: \033[1m{}\033[0m".format(time_format, end='\r'))
            chatSound.play()
            print("\033[91mHit enter to continue, type 's' if you'd like to skip, or 'skip day'\033[0m if you'd like to skip the entire day.")
            i = input()
            if i.upper() == 'S':
                chatSound.play()
                print("\033[45mYou have opted to skip deliberation and go straight to the gallows.\033[0m")
                sleep(3)
                break
            elif i.upper() == "SKIP DAY":
                return day_number
            else:
                countdown_timer -= 1
                pass
        else:
            os.system('cls')
            print("\033[91mDiscuss anything you may have learned last night or any suspicions you may have.\033[0m")
            print("You will vote after deliberation on who to hang.")
            print(" ")
            print("Time left to deliberate: \033[1m{}\033[0m".format(time_format, end='\r'))
            sleep(1)
            countdown_timer -= 1
    vote_number = 1
    trialPlayer.queue(questioningMusic)
    while vote_number <= 2:
        os.system('cls')
        chatSound.play()
        if vote_number == 2:
            print("There is still time to prosecute one more person...")
        print("Who has the town selected to put on trial?")
        print("-" * SCREEN_WIDTH)
        print_remaining_players("Day")
        # Get desired target from town
        player_number = get_user_input_vote()
        if player_number == 666:
            # Players have opted to skip the vote
            voteSound.play()
            print("\033[45mThe town has selected to skip the day.\033[0m")
            sleep(3)
            os.system('cls')
            dayEnd.play()
            print("\033[33mThe hour is too late to continue, we shall reconvene tomorrow...\033[0m")
            sleep(4)
            return day_number
        # Convert target number into player object
        local_day_player = get_player_target(player_number)
        voteSound.play()
        print("The town has selected to place \033[94m{}\033[0m on trial. Their defense will now begin.".format(local_day_player.name))
        sleep(3)
        countdown_timer = 10
        trialPlayer.play()
        while countdown_timer >= 0:
            os.system('cls')
            print("\033[94m{}\033[0m, you stand accused of conspiring against the town.".format(local_day_player.name))
            print("\033[94m{}\033[0m, you have \033[1m{} seconds\033[0m to defend yourself.".format(local_day_player.name, countdown_timer))
            print("\033[41mNo-one else may speak during this period.\033[0m")
            countdown_timer -= 1
            sleep(1)
        countdown_timer = 10
        chatSound2.play()
        while countdown_timer >= 0:
            os.system('cls')
            print("The remaining town members have \033[1m{} seconds\033[0m to deliberate.".format(countdown_timer))
            print("Voters may abstain.")
            print("\033[41mAll may now speak including the defendant.\033[0m")
            countdown_timer -= 1
            sleep(1)
        os.system('cls')
        # Get the number of users who voted innocent
        innocent_vote = get_integer_vote("\033[32minnocent\033[0m")
        voteSound.play()
        # Get the number of users who voted guilty
        guilty_vote = get_integer_vote("\033[31mguilty\033[0m")
        voteComplete.play()
        trialPlayer.pause()
        os.system('cls')
        print("The votes have been collected and counted...")
        sleep(4)
        if guilty_vote > innocent_vote:
            # Player was found guilty
            print("The town has found \033[94m{}\033[0m \033[31mGUILTY\033[0m of the accusations made against them.".format(local_day_player.name))
            guiltyVerdict.play()
            # TODO: Add execution sounds and methods
            sleep(4)
            print("\033[94m{}\033[0m has been \033[31mHANGED\033[0m.".format(local_day_player.name))
            local_day_player.living = False
            permaDeathList.append(local_day_player)
            sleep(2)
            roleReveal.play()
            sleep(1)
            # TODO: Hanging the serial killer crashes the game for some reason
            print("Their role was " + (player.role.role_color()) + "{0}\033[0m".format(local_day_player.role.name))
            sleep(5)
            dayEnd.play()
            print("\033[33mThe hour is too late to continue, we shall reconvene tomorrow...\033[0m")
            return day_number
        elif guilty_vote == innocent_vote:
            # Player was found innocent
            print("\033[45mThere was a draw.\033[0m")
            print("The town has found \033[94m{}\033[0m \033[32mINNOCENT\033[0m of the accusations made against them.".format(local_day_player.name))
            votedInnocent.play()
            vote_number += 1
            sleep(5)
        else:
            # Player was found innocent
            print("The town has found \033[94m{}\033[0m \033[32mINNOCENT\033[0m of the accusations made against them.".format(local_day_player.name))
            votedInnocent.play()
            vote_number += 1
            sleep(5)
        trialPlayer.next_source()
        trialPlayer.queue(questioningMusic)
        guilty_vote = 0
        innocent_vote = 0
    os.system('cls')
    dayEnd.play()
    print("\033[33mThe hour is too late to continue, we shall reconvene tomorrow...\033[0m")
    sleep(4)
    goodNightBell.play()
    print("\033[91mPlease close your eyes\033[0m so the first night may begin.")
    sleep(5)
    os.system('cls')
    return day_number


# Checks to see if the victory conditions have been met
def check_victory_conditions():
    victory_condition = None
    serial_killer_alive = False
    # Step 1. Check to see how many players are left
    remaining_players = []
    for player in playerList:
        if player.living == True:
            remaining_players.append(player)
    # Step 2. Check to see if Serial Killer Won
    for player in remaining_players:
        if player.role.name == "Serial Killer":
            serial_killer_alive = True
            if len(remaining_players) <= 2:
                victory_condition = "Serial Killer"
                return victory_condition
    if not serial_killer_alive:
        victory_condition = "Town"
        return victory_condition
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


# Output a list of all players to the user
def print_remaining_players(local_type="Night"):
    if local_type.upper() == "DAY":
        print("[S] \033[95mSKIP THE DAY AND DO NOTHING\033[0m")
    else:
        print("[S] \033[95mSKIP THE NIGHT AND DO NOTHING\033[0m")
    for player in playerList:
        if player.living:
            print("[{0}] \033[94m{1}\033[0m".format(player.number, player.name))
        else:
            print("[X] \033[31m{0}\033[0m".format(player.name))


# Take the target number recieved from the player and swap it for the corresponding player object
def get_player_target(target_number):
    for player in playerList:
        if player.number == target_number:
            return player


def get_integer_vote(verdict):
    number = "NULL"
    while True:
        while not number.isdigit():
                print("Please enter the number of people who voted {}".format(verdict))
                number = input()
        print("{} people voted {}, is this correct?".format(number,verdict))
        local_answer = input()
        if (local_answer.upper() == "Y") or (local_answer.upper() == "YES") or (local_answer.upper() == "YE") or (local_answer.upper() == "YEAH") or (local_answer.upper() == "YEAH!"):
            return number
        else:
            number = "NULL"


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


# Used for filtering user input during the night
def get_user_input(player):
    while True:
        local_target = str(input())
        if not local_target.isdigit():
            if local_target.upper() == "S":
                return local_target.upper()
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


# Used for filtering user input during the day
def get_user_input_vote():
    while True:
        local_target = str(input())
        if local_target.upper() == "S":
            local_target = 666
            return local_target
        if not local_target.isdigit():
            print("That wasn't the kind of number we were looking for," + Fore.LIGHTRED_EX + " choose another please." + Fore.RESET)
            sleep(2)
        else:
            if int(local_target) < len(playerList) and int(local_target) >= 0:
                local_target = int(local_target)
                if not playerList[local_target].living:
                    print("That person is dead," + Fore.LIGHTRED_EX + " choose another please." + Fore.RESET)
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
trialPlayer = pyglet.media.Player()
dayPlayer = pyglet.media.Player()

# Create lists of the music and ambient sounds to be played
musicList = [nightSequence1, nightSequence2, nightSequence3, nightSequence4, nightSequence5, nightSequence6]
soundsList = [nightSounds1, rainSounds1]

# Begin the day/night cycle
while True:
    nightNumber = night_sequence(nightNumber)
    victoryCondition = check_victory_conditions()
    if victoryCondition is not None:
        break
    dayNumber = day_sequence(dayNumber)
    victoryCondition = check_victory_conditions()
    if victoryCondition is not None:
        break

print("VICTORY FOR {}".format(victoryCondition))

# Prevent the screen from closing
input()
