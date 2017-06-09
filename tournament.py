#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach
from random import randrange


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteTournaments():
    """Remove all the tournament records from the database"""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM tournaments")
    db.commit()
    db.close()


def deleteTournament(id):
    """Delete a certain tournament from the tournaments table

    This will permanently delete a tournament from the database,
    including all matches and player assignments.

    Args:
      id: the id of the tournament to be deleted
    """
    id = bleach.clean(id)
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM matches WHERE tournament = %s", (id,))
    c.execute("DELETE FROM tournament_players WHERE tournament = %s", (id,))
    c.execute("DELETE FROM tournaments WHERE id = %s", (id,))
    db.commit()
    db.close()


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM matches")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM tournament_players")
    c.execute("DELETE FROM players")
    db.commit()
    db.close()


def newTournament(name):
    """Creates a new tournament and returns the id

    Args:
      name: the name of the tournament

    Returns:
      the new tournament's id
    """
    name = bleach.clean(name)
    db = connect()
    c = db.cursor()
    c.execute("""INSERT INTO tournaments (name)
                 VALUES (%s) RETURNING id""", (name,))
    t_id = c.fetchone()[0]
    db.commit()
    db.close()
    return t_id


def countPlayers(tournament=None):
    """Returns the number of players currently registered.

    Args:
      tournament (optional): return the number of players only
                             for the given tournament
    """
    db = connect()
    c = db.cursor()
    if tournament:
        tournament = bleach.clean(tournament)
        c.execute("""SELECT count(*) FROM tournament_players
                     WHERE tournament = %s""", (tournament,))
    else:
        c.execute("SELECT count(*) FROM players")
    count = c.fetchone()[0]
    db.close()
    return count


def registerPlayer(name):
    """Adds a player to the tournament database and returns the id.

    Args:
      name: the name of the player

    Returns:
      the id of the new player
    """
    name = bleach.clean(name)
    db = connect()
    c = db.cursor()
    c.execute("""INSERT INTO players (name)
                 VALUES (%s) RETURNING id""", (name,))
    p_id = c.fetchone()[0]
    db.commit()
    db.close()
    return p_id


def assignPlayers(tournament, *players):
    """Assigns a list of players to a tournament

    Args:
      tournament: the id of the tournament the players will be assigned to
      *players: the id of the players to assign to tournament, each given as
                its own argument or as a list.
                Ex1: assignPlayers(t1, p1, p2, p3, p4, ...)
                Ex2: assignPlayers(t1, [p1, p2, p3, p4, ...])
    """
    tournament = bleach.clean(tournament)
    db = connect()
    c = db.cursor()
    if type(players[0]) is list and len(players) == 1:
        players = players[0]
    for p in players:
        p = bleach.clean(p)
        c.execute("""INSERT INTO tournament_players (tournament, player)
                     VALUES (%s, %s)""", (tournament, p,))
    db.commit()
    db.close()


def quickTournament(t_name, *players):
    """Creates a new tournament, register players
    and assign players to the tournament

    Args:
      t_name: the name of the tournament
      *players: the name of the players, each given as its own argument
                Ex: quickTournament("myTournament", "player1", "player2", ...)

    Returns:
      the id of the new tournament
    """
    t = newTournament(t_name)
    p = []
    for player in players:
        p.append(registerPlayer(player))
    assignPlayers(t, p)
    return t


def playerStandings(tournament):
    """Returns a list of the players and their win records, sorted by wins.

    Args:
      tournament: id of the tournament to return standings for

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    tournament = bleach.clean(tournament)
    db = connect()
    c = db.cursor()
    c.execute("""SELECT id, name, wins, matches FROM standings
                 WHERE tournament = %s""", (tournament,))
    standings = [(int(row[0]), str(row[1]),
                  int(row[2]), int(row[3])) for row in c.fetchall()]
    db.close()
    return standings


def reportMatch(tournament, winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      tournament: the id of the tournament the match belongs to
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    tournament = bleach.clean(tournament)
    winner = bleach.clean(winner)
    loser = bleach.clean(loser)
    db = connect()
    c = db.cursor()
    c.execute("""INSERT INTO matches (tournament, winner, loser)
                 VALUES (%s, %s, %s)""", (tournament, winner, loser,))
    db.commit()
    db.close()


def swissPairings(tournament):
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Args:
      tournament: the id of the tournament to pair players for

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    tournament = bleach.clean(tournament)
    db = connect()
    c = db.cursor()
    c.execute("""SELECT id, name FROM standings
                 WHERE tournament = %s""", (tournament,))
    players = [(int(row[0]), str(row[1])) for row in c.fetchall()]
    pairs = []
    while players:
        p1 = players.pop(0)
        p2 = players.pop(0)
        pairs.append(p1+p2)
    return pairs


def randomPairings(tournament):
    """Returns a list of random pairs of players for the first round of tournament

    For the first round of the tournament, the players are paired randomly

    Args:
      tournament: the id of the tournament to pair players for

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    tournament = bleach.clean(tournament)
    db = connect()
    c = db.cursor()
    c.execute("""SELECT id, name FROM standings
                 WHERE tournament = %s""", (tournament,))
    players = [(int(row[0]), str(row[1])) for row in c.fetchall()]
    pairs = []
    while players:
        p1 = players.pop(randrange(len(players)))
        p2 = players.pop(randrange(len(players)))
        pairs.append(p1+p2)
    return pairs
