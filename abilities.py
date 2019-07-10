import random
from time import sleep

from colorama import Back

from file_directory import *
from globalVars import *

standardKillDescriptorList = ["You hear shots ring through the streets...",
                              "Sounds of combat echo through this quiet town...",
                              "You hear harsh gunshots drown out a muffled scream...",
                              ]

serialKillDescriptorList = ["You hear a sickening combination of rapid knife cuts and gunfire in the night...",
                            "The silence of the night is disturbed by an intermixing of cuts, screams, and laughter..."]

standardCorpseDescriptorList = ["Their body was battered and had multiple bone fractures. They were shot at close range.",
                                "They were riddled with bullets from a close range.",
                                "They were shot at a close range.",
                                "Their body was littered with bruises and marks, and a bullet was found in their chest.",
                                "There were signs of a struggle in their home, ultimately leading to their death by gun wound."
                                ]

vigilanteCorpseDescriptorList = ["Bullets from a powerful pistol were found precisely buried into the victims major organs - the work of a professional.",
                                 "A single bullet hole was found in the back of the victim's skull, they didn't know what hit them.",
                                 "The victim clearly had no time to defend themselves, they were found dead in their bathroom - shot through the wall by a powerful pistol."
                                 ]

serialKillerCorpseDescriptorList = ["Knife cuts were found all over their body, they bled to death slowly.",
                                    "Several bullet wounds and slashing cuts were found on the victim.",
                                    "A large dagger was found buried in their back.",
                                    "The victims limbs were almost severed from their body by deep knife cuts into their skin."
                                    ]

# TODO: Fix the color formatting on event notifiers, they're horrible right now

# UNRELATED TO ABILITIES
def play_kill_sound(player):
    mafia_kill_sound = random.choice(mafiaKillSounds)
    serial_kill_sound = random.choice(serialKillSounds)
    arson_kill_sound = random.choice(arsonKillSounds)
    # NOTE: BODYGUARD IS EXCLUDED FROM THIS FUNCTION
    if player.role.name == "Serial Killer":
        print(Back.RED + random.choice(serialKillDescriptorList) + Back.RESET)
        player.target.death_description = random.choice(serialKillerCorpseDescriptorList)
        serial_kill_sound.play()
        sleep(5)
        return
    elif player.role.name == "Godfather":
        print(Back.RED + random.choice(standardKillDescriptorList) + Back.RESET)
        player.target.death_description = random.choice(standardCorpseDescriptorList)
        mafia_kill_sound.play()
        sleep(8)
        return
    elif player.role.name == "Vigilante":
        print(Back.RED + random.choice(standardKillDescriptorList) + Back.RESET)
        player.target.death_description = random.choice(vigilanteCorpseDescriptorList)
        mafia_kill_sound.play()
        sleep(8)
        return
    elif player.role.name == "Arson":
        # TODO: Add kill and corpse descriptors for arsonist
        arson_kill_sound.play()
        sleep(12)
        return
    else:
        print("ERROR: ROLE HAS NO KILL DESCRIPTORS!")
        sleep(8)
        input()


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
    temp_dict = {"Vested": player}
    player.status.update(temp_dict)
    player.info.append("You can use your vest for {0} more night(s)".format(player.uses))
    # The action was completed without issue


# Prevent a user from completing their night ability action
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
        player.target.uses += 1
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
            player.info.append(player.target.name + " \033[45m" + " is night immune tonight, and cannot be killed this way!\033[49m")
            return
    # This target was guarded and now both you and one of the guards will die
    if "Guarded" in player.target.status.keys():
        bodyguard_list = player.target.status["Guarded"]
        # Select one of the multiple possible bodyguards that will give their lives to save the target
        bodyguard_list_length = len(bodyguard_list)
        if bodyguard_list_length > 1:
            # There is more than one bodyguard guarding the target, pick a random one to kill
            selected_bodyguard_number = random.randrange(0, bodyguard_list_length)
            selected_bodyguard = bodyguard_list[selected_bodyguard_number]
            print("\033[41mYou hear the violent, harsh rapport of an old fashioned shootout.\033[49m")
            gunFight1.play()
            sleep(7)
            selected_bodyguard.living = False
            deathList.append(selected_bodyguard)
            player.living = False
            deathList.append(player)
            selected_bodyguard.info.append(player.target.name + " \033[41m"+ "was attacked last night! You and the assailant were both slain in the shootout!\033[49m")
            player.info.append(player.target.name + " \033[41m" + "was protected by a bodyguard! You and the bodyguard were both slain in the shootout!\033[49m")
            bodyguard_list.remove(selected_bodyguard)
            # Notify remaining bodyguards that their target was protected by someone else
            for item in bodyguard_list:
                item.info.append(player.target.name + " \033[42m" + "was attacked last night, however someone else moved to engage the killer before you could!\033[49m")
        else:
            selected_bodyguard = bodyguard_list[0]
            # There is only one bodyguard protecting the target
            print("\033[41mYou hear the violent, harsh rapport of an old fashioned shootout.\033[49m")
            gunFight1.play()
            sleep(7)
            selected_bodyguard.living = False
            deathList.append(selected_bodyguard)
            player.living = False
            deathList.append(player)
            # No bodyguards are protecting this target anymore, remove status
            del player.target.status["Guarded"]
            selected_bodyguard.info.append(player.target.name + " \033[41m" + "was attacked last night! You and the assailant were both slain in the shootout!\033[49m")
            player.info.append(player.target.name + " \033[41m" +"was protected by a bodyguard! You and the bodyguard were both slain in the shootout!\033[49m")
    elif "Vested" in player.target.status.keys():
        # The target was wearing a bulletproof vest that protected them from harm
        player.target.info.append("\033[42mSomeone shot you on your porch last night, however your bulletproof vest miraculously absorbed all the damage!\033[49m")
        play_kill_sound(player)
        return
    elif not player.target.living:
        # The target is already dead
        player.info.append("\033[45mYou found " + player.target.name + "'s corpse alone in their home, they were already killed before you arrived!\033[49m")
        return
    else:
        # The target wasn't protected or immune and is now dead unless healed
        if player.role.name == "Serial Killer":
            play_kill_sound(player)
        else:
            play_kill_sound(player)
        player.target.living = False
        deathList.append(player.target)
        player.target.info.append("\033[41mYou have been killed in the night. Your cold body will be found in the morning.\033[49m")
        if player.target.role.alignment == "Town" or player.role.alignment == "Mafia":
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
            player.info.append(player.target.name + "\033[45m" +" is heal immune tonight, and couldn't be healed even if they were attacked.\033[49m")
            return
        if player.target.living:
            # The healer's target was not harmed enough to require healing.
            player.info.append(player.target.name + "\033[42m" + " did not require healing last night.\033[49m")
            return
        else:
            # The healer's target is currently dead.
            player.target.living = True
            deathList.remove(player.target)
            player.target.info.append("\033[42mYou were brutally attacked and left for dead, but a stranger arrived and nursed you back to health.\033[49m")
            player.info.append(player.target.name + "\033[42m" +" was brutally attacked last night. You were able to anonymously nurse them back to health.\033[49m")
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
            player.info.append(player.target.name + " \033[42m" +"is not suspicious.\033[49m")
            return
    if player.target.role.alignment == "Town":
        player.info.append(player.target.name + " \033[42m" +"is not suspicious.\033[49m")
    else:
        # #!Change this once mafia and other neut roles are defined
        player.info.append(player.target.name + " \033[41m" + "is not a member of the town!\033[49m")


def watch_ability(player):
    # IMMUNITY DEPENDENCIES: None
    # STATUS DEPENDENCIES: None
    # TRAIT DEPENDENCIES: None
    tonights_visitors = player.target.name + " \033[45m" + "was visited tonight by "
    number_of_visitors = len(player.target.visitors)
    if number_of_visitors == 1:
        for visitor in player.target.visitors:
            tonights_visitors = (tonights_visitors + (visitor.name + ".\033[49m"))
            player.info.append(tonights_visitors)
    elif number_of_visitors > 0:
        for visitor in player.target.visitors:
            if number_of_visitors > 1:
                tonights_visitors = (tonights_visitors + visitor.name + ", ")
                number_of_visitors -= 1
            else:
                tonights_visitors = (tonights_visitors + ("and " + visitor.name + ".\033[49m"))
                number_of_visitors = 0
                player.info.append(tonights_visitors)
        player.target.visitors.append(player)
    else:
        tonights_visitors = (tonights_visitors + "nobody.\033[49m")
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
