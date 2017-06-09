#!/usr/bin/env python
#
# Test cases for tournament.py
# These tests are not exhaustive, but they should cover the majority of cases.


from tournament import (deleteMatches, deletePlayers, deleteTournaments,
                        newTournament, countPlayers, registerPlayer,
                        assignPlayers, playerStandings, reportMatch,
                        swissPairings, randomPairings, quickTournament)


def testCount():
    """
    Test for initial player count,
             player count after 1 and 2 players registered,
             player count after 4 players reg and 2 assigned
             player count after players deleted.
    """
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deletion, countPlayers should return zero.")
    print ("1.  countPlayers() returns 0 after "
           "initial deletePlayers() execution.")
    registerPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError("After one player registers, countPlayers() should "
                         "be 1. Got {c}".format(c=c))
    print "2.  countPlayers() returns 1 after one player is registered."
    registerPlayer("Jace Beleren")
    c = countPlayers()
    if c != 2:
        raise ValueError("After two players register, countPlayers() should "
                         "be 2. Got {c}".format(c=c))
    print "3.  countPlayers() returns 2 after two players are registered."

    t1 = newTournament("Tournament 1")
    p1 = registerPlayer("Steinar Utstrand")
    p2 = registerPlayer("Donald Duck")
    assignPlayers(t1, p1, p2)
    c = countPlayers()
    if c != 4:
        raise ValueError("Even players not assigned to "
                         "tournament should be counted.")
    print ("4.  countPlayers() returns 4 when 2 of 4 players are assigned "
           "to tournament.")
    c = countPlayers(t1)
    if c != 2:
        raise ValueError("countPlayers(t_id) should only count players "
                         "assigned to given tournament")
    print ("5.  countPlayers(t_id) returns 2 when 2 of 4 players are assigned "
           "to given tournament id")

    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError(
            "After deletion, countPlayers should return zero.")
    print ("6.  countPlayers() returns zero after registered players are "
           "deleted.\n7.  Player records successfully deleted.")


def testStandingsBeforeMatches():
    """
    Test to ensure players are properly represented in standings prior
    to any matches being reported.
    """
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    t1 = newTournament("Test tournament")
    p1 = registerPlayer("Melpomene Murray")
    p2 = registerPlayer("Randy Schwartz")
    registerPlayer("Lucky Luke")
    registerPlayer("Charlie Brown")
    assignPlayers(t1, p1, p2)
    standings = playerStandings(t1)
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even "
                         "before they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only assigned players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError("Newly registered players should have no matches "
                         "or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in "
                         "standings, even if they have no matches played.")
    print ("8.  Newly registered players appear in the "
           "standings with no matches.")


def testReportMatches():
    """
    Test that matches are reported properly.
    Test to confirm matches are deleted properly.
    """
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    t1 = quickTournament("Tournament 2", "Bruno Walton", "Boots O'Neal",
                         "Cathy Burton", "Diane Grant")
    standings = playerStandings(t1)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(t1, id1, id2)
    reportMatch(t1, id3, id4)
    standings = playerStandings(t1)
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero "
                             "wins recorded.")
    print "9.  After a match, players have updated standings."
    deleteMatches()
    standings = playerStandings(t1)
    if len(standings) != 4:
        raise ValueError("Match deletion should not change number of players "
                         "in standings.")
    for (i, n, w, m) in standings:
        if m != 0:
            raise ValueError("After deleting matches, players should have "
                             "zero matches recorded.")
        if w != 0:
            raise ValueError("After deleting matches, players should have "
                             "zero wins recorded.")
    print ("10. After match deletion, player standings are properly reset.\n"
           "11. Matches are properly deleted.")


def testPairings():
    """
    Test that pairings are generated properly
    both before and after match reporting.
    Test random pairings
    """
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    t1 = quickTournament("Tournament 3", "Twilight Sparkle", "Fluttershy",
                         "Applejack", "Pinkie Pie", "Rarity", "Rainbow Dash",
                         "Princess Celestia", "Princess Luna")
    standings = playerStandings(t1)
    [id1, id2, id3, id4, id5, id6, id7, id8] = [row[0] for row in standings]
    pairings = swissPairings(t1)
    random = randomPairings(t1)
    if random == pairings:
        random = randomPairings(t1)
        if random == pairings:
            raise ValueError("randomPairings() return same pairings "
                             "as swissPairings()")
    print "12. randomPairings() returns random pairings"
    if len(pairings) != 4:
        raise ValueError("For eight players, swissPairings should return "
                         "4 pairs. Got {pairs}".format(pairs=len(pairings)))
    reportMatch(t1, id1, id2)
    reportMatch(t1, id3, id4)
    reportMatch(t1, id5, id6)
    reportMatch(t1, id7, id8)
    pairings = swissPairings(t1)
    if len(pairings) != 4:
        raise ValueError("For eight players, swissPairings should return "
                         "4 pairs. Got {pairs}".format(pairs=len(pairings)))
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4),
     (pid5, pname5, pid6, pname6), (pid7, pname7, pid8, pname8)] = pairings
    possible_pairs = set([frozenset([id1, id3]), frozenset([id1, id5]),
                          frozenset([id1, id7]), frozenset([id3, id5]),
                          frozenset([id3, id7]), frozenset([id5, id7]),
                          frozenset([id2, id4]), frozenset([id2, id6]),
                          frozenset([id2, id8]), frozenset([id4, id6]),
                          frozenset([id4, id8]), frozenset([id6, id8])
                          ])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4]),
                        frozenset([pid5, pid6]), frozenset([pid7, pid8])])
    for pair in actual_pairs:
        if pair not in possible_pairs:
            raise ValueError("After one match, players with one win "
                             "should be paired.")
    print "13. After one match, players with one win are properly paired."


if __name__ == '__main__':
    testCount()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    print "Success!  All tests pass!"
