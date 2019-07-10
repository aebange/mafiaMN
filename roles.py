from classes import Role

# Define Town Roles
citizen = Role(
    "Citizen",  # Name (What the role is called)
    "Town",  # Affiliation (How the role wins)
    ["Town Government"],  # Type (What the role does)
    "None",  # Abilities (What the role can do at night) TODO: Change this back to bulletproof vest
    3,  # Uses (How many times the ability can be used)
    ["None"],  # Immunities (What the role cant be killed or detected by at night)
    ["None"],  # Traits (Special details about the role)
    "a regular person who believes in truth and justice.",  # Summary (A lore-based description of the role)
    "The Citizen has a Bulletproof Vest that can be used to save them from death only ONCE each night. If you are attacked by multiple people however, you will die. Be conservative as your vest may have limited uses!",
    0)  # Role Priority

bodyguard = Role(
    "Bodyguard",
    "Town",
    ["Town Protective"],
    "Guard",
    666,
    ["None"],
    ["None"],
    "a war veteran who secretly makes a living by selling protection.",
    "The bodyguard can guard one person each night. If that person is attacked while you are protecting them, both you and the attacker will die. The person you are protecting however will be spared - EVEN if they aren't town.",
    0)  # Role Priority

lookout = Role(
    "Lookout",
    "Town",
    ["Town Investigative"],
    "Watch",
    666,
    ["None"],
    ["Self-Target", "Ignore Detection Immunity"],
    "a war veteran who secretly makes a living by selling protection.",
    "The lookout can stake out at one person's house each night to see who visits them. Remember, not only evil players may be visiting other's houses.",
    3)  # Role Priority

escort = Role(
    "Escort",
    "Town",
    ["Town Protective"],
    "Role-block",
    666,
    ["None"],
    ["None"],
    "a scantily-clad street worker, working in secret.",
    "The escort can visit one person's house each night, giving them such a good time that they are role-blocked for that night and cannot complete any actions.",
    0)  # Role Priority

doctor = Role(
    "Doctor",
    "Town",
    ["Town Protective"],
    "Heal",
    666,
    ["None"],
    ["Attack Alert"],
    "a secret surgeon skilled in trauma care.",
    "The doctor can guard one person each night. If that person is attacked while you are protecting them, you will heal them fully. You can only heal them once though, and multiple attackers will succeed in their mission.",
    2)  # Role Priority

sheriff = Role(
    "Sheriff",
    "Town",
    ["Town Investigative"],
    "Check Affiliation",
    666,
    ["None"],
    ["None"],
    "a member of law enforcement, forced into hiding because of the threat of murder.",
    "The sheriff can investigate one person's house each night, identifying who they are affiliated with. Beware however, for you will be a prime target for murder once you reveal your findings to your colleagues.",
    3)  # Role Priority

mayor = Role(
    "Mayor",
    "Town",
    ["Town Government", "Town Investigative"],
    "None", # TODO: Add functionality to day reveal
    1,
    ["Heal Immune"],
    ["None"],
    "the governor of the town, hiding in anonymity to avoid assassination.",
    "The mayor has no night abilities, but can reveal himself during the day. Revealing increases the value of your vote significantly and confirms to the other players that you are indeed the mayor. Use this power to lead the town, but use it carefully, you will be a big target for the evil players.",
    3)  # Role Priority

vigilante = Role(
    "Vigilante",
    "Town",
    ["Town Killing"],
    "Murder",
    2,
    ["Heal Immune"],
    ["None"],
    "a dirty ex-cop who will ignore the law to enact justice.",
    "The vigilante can choose to murder one person each night. This will not kill anyone who has night immunity - like the Serial Killer, but can work on weaker roles. This ability can kill town members too. Be conservative with your gun, you only have so many bullets.",
    1)  # Role Priority

# Define Neutral Roles
serial_killer = Role(
    "Serial Killer",
    "Serial Killer",
    ["Neutral Killing"],
    "Murder",
    666,
    ["Detect Immune", "Night Immune"],
    ["Kills Role Blockers"],
    "a deranged criminal who hates the world.",
    "The serial killer can choose to murder one person each night. You are night-immune and can only die by suicide or hanging during the day. Try to target roles who will lead the town to discovering you first.",
    1)  # Role Priority

# Define Mafia Roles
godfather = Role(
    "Godfather",
    "Mafia",
    ["Mafia Killing"],
    "Murder",
    666,
    ["Detect Immune", "Night Immune"],
    ["Kills Role Blockers"],
    "the leader of the town's organized mafia syndicate.",
    "The Godfather may vote on who he should go kill each night. Unlike other mafia roles whose votes count for one, his vote counts for three. The Godfather should try to lead his companions to victory by directing their actions.",
    1)  # Role Priority

agent = Role(
    "Agent",
    "Mafia",
    ["Mafia Support"],
    "Watch",
    666,
    ["None"],
    ["Self-Target", "Ignore Detection Immunity"],
    "one of the many Caporegime the GodFather employs, this shady individual gathers information for the Mafia.",
    "The objective of the Agent is to help the mafia identify key enemy players by watching a person each night to see who visits them. The Agent may vote on who he believes should be killed each night by the Godfather.",
    3)  # Role Priority

consort = Role(
    "Consort",
    "Mafia",
    ["Mafia Support"],
    "Role-block",
    666,
    ["None"],
    ["None"],
    "a street working dancer serving the orders of organized crime.",
    "The consort can visit one person's house each night, role-blocking them for the evening. The consort may vote on who he believes should be killed each night by the Godfather.",
    0)  # Role Priority

# Included roles
##townRolesList = [citizen, bodyguard, lookout, escort, doctor, sheriff, mayor, vigilante]
townRolesList = [vigilante, vigilante, vigilante, vigilante]
neutralRolesList = [serial_killer]
##mafiaRolesList = [godfather, godfather, godfather]
mafiaRolesList = [godfather, agent, consort]