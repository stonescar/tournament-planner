#!/usr/bin/env python
#
# play.py -- a simple example of how the module can be used
#

import os
import bleach
from blessings import Terminal
from tournament import (connect, deleteMatches, newTournament,
                        registerPlayer, assignPlayers, playerStandings,
                        reportMatch, swissPairings, randomPairings)


def showPlayerStandings(t):
    """Prints a table of player standings. Gives error message if no players"""
    global message
    standings = playerStandings(t)
    if standings:
        os.system('cls' if os.name == 'nt' else 'clear')
        t = Terminal()
        print """\n\n\n
        TOURNAMENT STANDINGS
        =========================================================================
        |  #  |  id  |                   name                  | wins | matches |
        -------------------------------------------------------------------------"""
        place = 0
        for row in standings:
            place += 1
            id = len(str(row[0]))
            name = len(str(row[1]))
            wins = len(str(row[2]))
            match = len(str(row[3]))
            print "        | %s%s | %s%s | %s%s | %s%s | %s%s |" % (
                " "*(3-len(str(place))), place,
                " "*(4-id), row[0],
                " "*(39-name), row[1],
                " "*(4-wins), row[2],
                " "*(7-match), row[3])
        print "        =========================================================================\n" # NOQA
        raw_input('Press ENTER to continue')
        message = ""
    else:
        message = "There are no players assigned to this tournament"


def printSwiss(t):
    """Prints the player pairings after the Swiss model"""
    global message
    pairings = swissPairings(t)
    if pairings:
        c = 0
        os.system('cls' if os.name == 'nt' else 'clear')
        print """\n\n
                    -----------------------------------------
                         SWISS PAIRINGS FOR NEXT ROUND:
                    ------------------- o -------------------
                                        |"""
        for pair in pairings:
            c += 1
            id1, name1, id2, name2 = pair
            p1, p2 = ("%s (ID: %s)" % (name1, id1),
                      "%s (ID: %s)" % (name2, id2))
            print "%s%s   V S   %s" % (" "*(36-len(p1)), p1, p2)
            print "                                        |"
        print "                                  ----- o -----\n\n"
        raw_input('Press ENTER to continue')
        message = ""
    else:
        message = "There are no players assigned to this tournament"


def printRandom(t):
    """Prints random pairs of players. Usefull for first round"""
    global message
    pairings = randomPairings(t)
    if pairings:
        c = 0
        os.system('cls' if os.name == 'nt' else 'clear')
        print """\n\n
                    -----------------------------------------
                         RANDOM PAIRINGS FOR NEXT ROUND:
                    ------------------- o -------------------
                                        |"""
        for pair in pairings:
            c += 1
            id1, name1, id2, name2 = pair
            p1, p2 = ("%s (ID: %s)" % (name1, id1),
                      "%s (ID: %s)" % (name2, id2))
            print "%s%s   V S   %s" % (" "*(36-len(p1)), p1, p2)
            print "                                        |"
        print "                                  ----- o -----\n\n"
        raw_input('Press ENTER to continue')
        message = ""
    else:
        message = "There are no players assigned to this tournament"


def get_t_name(t):
    """Returns the player's name from id, if found"""
    t = bleach.clean(t)
    db, c = connect()
    c.execute("SELECT name FROM tournaments WHERE id = %s", (t,))
    if c.rowcount > 0:
        name = c.fetchone()[0]
        db.close()
        return name
    else:
        db.close()


print "\x1b[8;35;90t"  # Resize terminal window
message = "Welcome to the tournament planner!"
t_id = None
t_name = ""
while 1:
    os.system('cls' if os.name == 'nt' else 'clear')
    active_t = "Current tournament: %s (ID: %s)" % (t_name, t_id) if t_id else ""
    print("""

     ______                                       __         __
    /_  __/__  __ _________  ___ ___ _  ___ ___  / /_  ___  / /__ ____  ___  ___ ____
     / / / _ \/ // / __/ _ \/ _ `/  ' \/ -_) _ \/ __/ / _ \/ / _ `/ _ \/ _ \/ -_) __/
    /_/  \___/\_,_/_/ /_//_/\_,_/_/_/_/\__/_//_/\__/ / .__/_/\_,_/_//_/_//_/\__/_/
                                                    /_/
    %s

        %s



        1) New tournament
        2) Add new player
        3) Report match result
        4) Show standings
        5) Generate Swiss pairings
        6) Generate random pairings
        7) Load tournament
        8) Reset tournament
        9) Exit

            ?+menu item for help (Ex: '?5')


    """ % (active_t, message))
    selection = raw_input('Select a menu item: ')

    if selection == '1':  # New tournament
        t_name = raw_input('Tournament name: ')
        t_id = newTournament(t_name)
        message = "%s created" % t_name

    elif selection == '2':  # Add new player
        if t_id:
            name = raw_input('Player name: ')
            p = registerPlayer(name)
            assignPlayers(t_id, p)
            message = "%s (ID: %s) registered" % (name, p)
        else:
            message = "Load or start a new tournament first"

    elif selection == '3':  # Report match result
        if t_id:
            winner = raw_input('Enter ID of winner: ')
            loser = raw_input('Enter ID of loser: ')
            reportMatch(t_id, winner, loser)
            message = "Match result reported"
        else:
            message = "Load or start a new tournament first"

    elif selection == '4':  # Show standings
        if t_id:
            showPlayerStandings(t_id)
        else:
            message = "Load or start a new tournament first"

    elif selection == '5':  # Generate Swiss pairings
        if t_id:
            printSwiss(t_id)
        else:
            message = "Load or start a new tournament first"

    elif selection == '6':  # Generate random pairings
        if t_id:
            printRandom(t_id)
        else:
            message = "Load or start a new tournament first"

    elif selection == '7':  # Load tournament
        t = raw_input('Enter valid tournament ID: ')
        name = get_t_name(t)
        if name:
            t_id = t
            t_name = name
            message = "%s (ID: %s) loaded" % (t_name, t_id)
        else:
            message = "Tournament ID not valid"

    elif selection == '8':  # Reset tournament
        if t_id:
            confirm = raw_input('This will delete all matches, but '
                                'keep players. Enter \'Y\' to confirm: ')
            if confirm == 'Y' or confirm == 'y':
                deleteMatches(t_id)
                message = "Tournament has been reset"
            else:
                message = ""
        else:
            message = "Load or start a new tournament first"

    elif selection == '9':  # Exit
        os.system('cls' if os.name == 'nt' else 'clear')
        print """


     ________             __          ___                __          _           __
    /_  __/ /  ___ ____  / /__ ___   / _/__  ____  ___  / /__ ___ __(_)__  ___ _/ /
     / / / _ \/ _ `/ _ \/  '_/(_-<  / _/ _ \/ __/ / _ \/ / _ `/ // / / _ \/ _ `/_/
    /_/ /_//_/\_,_/_//_/_/\_\/___/ /_/ \___/_/   / .__/_/\_,_/\_, /_/_//_/\_, (_)
                                                /_/          /___/       /___/


                                      20(c)17
                                  Steinar Utstrand

        """
        exit()
    elif selection == '?1':
        os.system('cls' if os.name == 'nt' else 'clear')
        print """\n\n\n
    1) New tournament

       Creates a new tournament. You have to start a new tournament before you
       can add players, view standings or report match results.

       Tournaments are automatically saved and can be loaded at any time.
       Please take note of the tournament ID for future loading.
       Give the tournament which ever name you like.
       \n\n"""
        raw_input('Press ENTER to coninue')
        message = ""

    elif selection == '?2':
        os.system('cls' if os.name == 'nt' else 'clear')
        print """\n\n\n
    2) Add new player

       Adds a new player to the current tournament. Players will appear in
       standings and are available for match reporting.

       New players recieve a unique ID, which will be shown when the player
       is added. Please take note of this ID, as this is what you'll enter
       when reporting match results. If you don't remember the players' IDs,
       they are listed in the standings.
       \n\n"""
        raw_input('Press ENTER to coninue')
        message = ""

    elif selection == '?3':
        os.system('cls' if os.name == 'nt' else 'clear')
        print """\n\n\n
    3) Report match result

       Adds the result of a match to the tournament database. Enter the unique
       ID of the winning player, followed by the ID of the losing player.

       If you don't remember the players' IDs, they are listed in the standings.
       \n\n"""
        raw_input('Press ENTER to coninue')
        message = ""

    elif selection == '?4':
        os.system('cls' if os.name == 'nt' else 'clear')
        print """\n\n\n
    4) Show standings

       Lists all players registered in the current tournament. The list is
       sorted by wins, so that the player on top is the leader/winner of
       the tournament.

       Columns include:
            #:          The player's rank
            id:         The player's unique ID
            name:       The player's name
            wins:       The player's total amount of wins
            matches:    The total amount of matches the player have played
       \n\n"""
        raw_input('Press ENTER to coninue')
        message = ""

    elif selection == '?5':
        os.system('cls' if os.name == 'nt' else 'clear')
        print """\n\n\n
    5) Generate Swiss pairings

       Shows pairings for the next round based on the Swiss model.

       The Swiss model pairs players based on their reults so far in the
       tournament. Each player will play someone with the same or almost
       the same amount of wins.

       For the first round of the tournament, the random pairing is recommended
       \n\n"""
        raw_input('Press ENTER to coninue')
        message = ""

    elif selection == '?6':
        os.system('cls' if os.name == 'nt' else 'clear')
        print """\n\n\n
    6) Generate random pairings

       Shows random pairings for the next round of the tournament.

       This is usefull for the first round of the tournament, when you
       don't have any data for the Swiss model.
       \n\n"""
        raw_input('Press ENTER to coninue')
        message = ""

    elif selection == '?7':
        os.system('cls' if os.name == 'nt' else 'clear')
        print """\n\n\n
    7) Load tournament

       Loads a previously created tournament. All players and match results
       will also be loaded.

       Enter the unique ID of the tournament you want to load.

       To start the loaded tournament over, reset the tournament after it's
       loaded. This will clear the matches, but keep the players.
       \n\n"""
        raw_input('Press ENTER to coninue')
        message = ""

    elif selection == '?8':
        os.system('cls' if os.name == 'nt' else 'clear')
        print """\n\n\n
    8) Reset tournament

       Deletes all matches, but keeps the players, so that the tournament
       can be started over from scratch.
       \n\n"""
        raw_input('Press ENTER to coninue')
        message = ""

    elif selection == '?9':
        os.system('cls' if os.name == 'nt' else 'clear')
        print """\n\n\n
    9) Exit

       Exits the tournament planner. All data will be stored in the database.
       To load a tournament the next time you open the program, please note the
       tournament's ID.
       \n\n"""
        raw_input('Press ENTER to coninue')
        message = ""

    elif selection == 'hi':
        message = "Hello! :)"

    elif selection == '':
        message = ""
    else:
        message = "That is not an option"
