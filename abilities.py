import random
from time import sleep

from file_directory import *


# UNRELATED TO ABILITIES
def play_kill_sound(player):
    mafia_kill_sound = random.choice(mafiaKillSounds)
    serial_kill_sound = random.choice(serialKillSounds)
    arson_kill_sound = random.choice(arsonKillSounds)
    if player.role == "Serial Killer":
        serial_kill_sound.play()
        sleep(5)
        return
    elif player.role == "Godfather":
        mafia_kill_sound.play()
        sleep(8)
        return
    elif player.role == "Vigilante":
        mafia_kill_sound.play()
        sleep(8)
        return
    elif player.role == "Arson":
        arson_kill_sound.play()
        sleep(12)
        return
    else:
        mafia_kill_sound.play()
        sleep(8)
        return


# Protect one person each night from 1 attack, if the target is attacked then both you and the killer will die.
def guard_ability(player):
    # IMMUNITY DEPENDENCIES: None
    # STATUS DEPENDENCIES: "Guarded"
    # TRAIT DEPENDENCIES: None
    player.target.visitors.append(player)
    if "Guarded" in player.target.status.keys():
        # This target is already under guard by someone else, add us to the list
        player.target.status["Guarded"].append(player)
    else:
        # Nobody else is guarding this target yet
        temp_dict = {"Guarded": [player]}
        player.target.status.update(temp_dict)
        # The action was completed without issue


# Protect yourself from attacks each night.
def bulletproof_vest_ability(player):
    # IMMUNITY DEPENDENCIES: None
    # STATUS DEPENDENCIES: None
    # TRAIT DEPENDENCIES:
    if player.role.uses > 0:
        temp_dict = {"Vested": player}
        player.status.update(temp_dict)
        # Subtract one use from the players uses
        player.role.uses -= 1
        # TODO: Remove uses from this section, it should be handled by the commit_action() function in main
        player.info.append("You can use your vest for {0} more night(s)".format(player.role.uses))
        # The action was completed without issue
    else:
        # The user is out of vests and should never have reached this function
        return


def role_block_ability(player):
    # IMMUNITY DEPENDENCIES: None
    # STATUS DEPENDENCIES: "Vested"
    # TRAIT DEPENDENCIES: "Kills Role Blockers"
    # Check for presence of trait dependencies
    player.target.visitors.append(player)
    for item in player.target.role.traits:
        if item == "Kills Role Blockers":
            # This role blocker is now the target of the serial killer
            player.target.target = player
            # The role block will fail and this player will die, nothing else needs to be done
            return
    # Erase the targets target, effectively role-blocking them
    player.target.target = None
    # Check for status dependencies
    if "Vested" in player.target.status.keys():
        del player.target.status["Vested"]
        player.target.role.uses += 1
        # TODO: Remove uses from this section, it should be handled by the commit_action() function in main
        player.target.info.append("\033[45mAn attractive person visited you tonight, distracting you until the morning. You have been role-blocked!\033[49m")
    else:
        player.target.target = "NULL"
        player.target.info.append("\033[45mAn attractive person visited you tonight, distracting you until the morning. You have been role-blocked!\033[49m")


# Attempt to kill one person each night.
def murder_ability(player):
    # IMMUNITY DEPENDENCIES: "Night Immunity"
    # STATUS DEPENDENCIES: "Guarded", "Vested"
    # TRAIT DEPENDENCIES: None
    # Check through the player's immunities
    player.target.visitors.append(player)
    for immunity in player.target.role.immunities:
        if immunity == "Night Immune":
            # This person could not be killed this way
            player.info.append("\033[45mYour target is night immune tonight, and cannot be killed this way!\033[49m")
            return
    # This person was guarded and now both you and one of the guards are dead
    if "Guarded" in player.target.status.keys():
        bodyguard_list = player.target.status["Guarded"]
        # Select one of the multiple possible bodyguards that will give their lives to save the target
        bodyguard_list_length = len(bodyguard_list)
        if bodyguard_list_length > 1:
            # There is more than one bodyguard, pick a random one to kill
            selected_bodyguard_number = random.randrange(0,(bodyguard_list_length))
            selected_bodyguard = bodyguard_list[selected_bodyguard_number]
            print("\033[41mYou hear the violent, harsh rapport of an old fashioned shootout.\033[49m")
            gunFight1.play()
            sleep(7)
            selected_bodyguard.alive = False
            player.alive = False
            selected_bodyguard.info.append("\033[41mYour target was attacked last night! You and the assailant were both slain in the shootout!\033[49m")
            player.info.append("\033[41mYour target was protected by a bodyguard! You and the bodyguard were both slain in the shootout!\033[49m")
            bodyguard_list.remove(selected_bodyguard)
            # Notify remaining bodyguards that their target was protected by someone else
            for item in bodyguard_list:
                item.info.append("\033[42mYour target was attacked last night, however someone else moved to engage the killer before you could!\033[49m")
        else:
            selected_bodyguard = bodyguard_list[0]
            # There is only one bodyguard
            print("\033[41mYou hear the violent, harsh rapport of an old fashioned shootout.\033[49m")
            gunFight1.play()
            sleep(7)
            selected_bodyguard.alive = False
            player.alive = False
            selected_bodyguard.info.append("\033[41mYour target was attacked last night! You and the assailant were both slain in the shootout!\033[49m")
            player.info.append("\033[41mYour target was protected by a bodyguard! You and the bodyguard were both slain in the shootout!\033[49m")
    elif "Vested" in player.target.status.keys():
        # The player was wearing a bulletproof vest that protected them from harm,
        player.target.info.append("\033[42mSomeone shot you on your porch last night, however your bulletproof vest miraculously absorbed all the damage!\033[49m")
        print("\033[41mYou hear sounds of combat in this quiet town.\033[49m")
        play_kill_sound(player)
        return
    else:
        # This person is now dead and will remain that way unless healed
        if player.role == "Serial Killer":
            print("\033[41mYou hear the sickening combination of rapid knife cuts and gunfire.\033[49m")
            play_kill_sound(player)
        else:
            print("\033[41mYou hear sounds of combat in this quiet town.\033[49m")
            play_kill_sound(player)
        player.target.alive = False
        player.target.info.append("\033[41mYou have been killed in the night. Your cold body will be found in the morning.\033[49m")
        if player.role.alignment == "Town" or player.role.alignment == "Mafia":
            player.target.info.append("Though you are dead, you can still win if your team achieves victory.")
    # The action was completed without issue


# Protect one person each night from 1 attack. If the target is attacked 1 time, they will be healed.
# The victim will know they've been healed.
def heal_ability(player):
    # IMMUNITY DEPENDENCIES: "Heal Immune"
    # STATUS DEPENDENCIES: None
    # TRAIT DEPENDENCIES: None
    player.target.visitors.append(player)
    for immunity in player.target.role.immunities:
        if immunity == "Heal Immune":
            # This person cannot be healed
            player.info.append("\033[45mYour target is heal immune tonight, and couldn't be healed even if they were attacked.\033[49m")
            return
        if player.target.living == True:
            # The healer's target was not harmed enough to require healing.
            player.info.append("\033[42mYour target did not require healing last night.\033[49m")
            return
        else:
            # The healer's target is currently dead.
            player.target.alive = True
            player.target.info.append("\033[42mYou were brutally attacked and left for dead, but a stranger arrived and nursed you back to health.\033[49m")
            player.info.append("\033[42mYour target was brutally attacked last night. You were able to anonymously nurse them back to health.\033[49m")
    # The action was completed without issue


# Check the affiliation of one player each night. Does NOT bypass detect immunity
def check_affiliation_ability(player):
    # IMMUNITY DEPENDENCIES: "Detect Immune"
    # STATUS DEPENDENCIES: None
    # TRAIT DEPENDENCIES: None
    player.target.visitors.append(player)
    for immunity in player.target.role.immunities:
        if immunity == "Detect Immune":
            # This person cannot be detected this way
            player.info.append("\033[42mYour target tonight is not suspicious.\033[49m")
            return
    if player.target.role.alignment == "Town":
        player.info.append("\033[42mYour target tonight is not suspicious.\033[49m")
    else:
        # #!Change this once mafia and other neut roles are defined
        player.info.append("\033[41mYour target tonight is not a member of the town!\033[49m")


def watch_ability(player):
    # IMMUNITY DEPENDENCIES: None
    # STATUS DEPENDENCIES: None
    # TRAIT DEPENDENCIES: None
    tonights_visitors = "\033[45mYour target tonight was visited by "
    number_of_visitors = len(player.target.visitors)
    if number_of_visitors > 0:
        for visitor in player.target.visitors:
            if number_of_visitors > 1:
                tonights_visitors  = (tonights_visitors +  visitor.name + ", ")
                number_of_visitors -= 1
            else:
                tonights_visitors = (tonights_visitors + ("and " + visitor.name + ".\033[49m"))
                number_of_visitors = 0
                player.info.append(tonights_visitors)
                print(tonights_visitors)
        player.target.visitors.append(player)
    else:
        tonights_visitors = (tonights_visitors + " nobody.\033[49m")
        player.info.append(tonights_visitors)
        player.target.visitors.append(player)


# Build a dictionary of which (string based) abilities in role class attributes correspond with with functions
dispatch = {
    "Guard": guard_ability,
    "Bulletproof Vest": bulletproof_vest_ability,
    "Role-block": role_block_ability,
    "Murder": murder_ability,
    "Heal": heal_ability,
    "Check Affiliation": check_affiliation_ability,
    "Watch": watch_ability
}