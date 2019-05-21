from colorama import Fore, Back

# Define alignment objectives
objectiveList = ["lynch all criminals and evildoers to restore justice to the town.",  # Town Alignment
                 "lynch and murder all of those who would oppose the mafia.",  # Mafia Alignment
                 "be the last person left alive.",  # Serial Killer Alignment
                 "survive until a victor has emerged."]  # Any Alignment


# Create the class structure for players
class Player:
    def __init__(self, name, number, role, living, status, last_will, target, info, visitors, death_info, uses):
        # (String) Used for storing this person's name
        self.name = name
        # (Integer) Used for storing when this person should be prompted for information (in progressive order)
        self.number = number
        # (Class Object) Used for storing this person's assigned role
        self.role = role
        # (Boolean) Used for storing whether or not this person is dead or alive
        self.living = living
        # (Dictionary) Used for storing any added effects made to this person each night
        self.status = status
        # (String) Used for storing the last wishes of a user (displayed on death)
        self.last_will = last_will
        # (Class Object) Used for storing who the user targeted each night
        self.target = target
        # (List of Strings) Used for storing feedback regarding the nights activities (Whether or not they failed, someone healed them, etc)
        self.info = info
        # (List of Objects) Used for keeping track of who visited this person during the night
        self.visitors = visitors
        # (String) Used for storing information on how the user died/was found by authorities.
        self.death_info = death_info
        # (Integer) Used for storing how many uses this person has left on their ability. 666 = infinite
        self.uses = uses


# Create the class structure for roles
class Role:
    def __init__(self, name, alignment, type, night_abilities, uses, immunities, traits, description, hint,
                 priority):
        # (String) Used for storing the name of this role
        self.name = name
        # (String) Used for storing the affiliation of this role
        self.alignment = alignment
        # (List of Strings) Used for storing the classification of this role (Investigative, Killing, Protective, etc)
        self.type = type
        # (String) Used for storing what this role can do at night
        self.night_abilities = night_abilities
        # (Integer) Used for storing how many nights this role can use their night_abilities, 666 = infinite
        self.uses = uses
        # (List of Strings) Used for storing any immunities to night_abilities this role may have
        self.immunities = immunities
        # (List of Strings) Used for storing any weird exceptions made for this role
        self.traits = traits
        # (String) Used for displaying to the user a description of who they are as this role
        self.description = description
        # (String) Used for displaying to the user hints regarding how to play as this role
        self.hint = hint
        # (Integer) Used for identifying when this role's night actions should be processed by the engine
        self.priority = priority
        # (String) Used for displaying to the user how they win the game
        self.objective = "Awaiting instantiation in def summary line 59..."
        # (Colorama Object) Used for identifying how this role's name should be printed to the screen
        self.color = Fore.WHITE
        # (Colorama Object) Used for identifying how this role's name should be printed to the screen
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
            print(
                "ERROR: INVALID self.alignment OF '%s' HAS ATTEMPTED TO PASS THROUGH def summary(self)!" % str(
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
