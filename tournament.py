#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#
# Via Vladimir Vyazovetskov
# http://erhosen.github.io/

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("UPDATE game SET wins=0, matches=0;");
    DB.commit()
    DB.close()

def deletePlayers():
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("DELETE from game;");
    DB.commit()
    DB.close()

def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("SELECT count(*) as num FROM game;")
    result = int(cursor.fetchone()[0])
    DB.close()
    return result

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("INSERT INTO game (name) VALUES (%s);", (name,))
    DB.commit()
    DB.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("SELECT * FROM game ORDER BY wins DESC;")
    result = cursor.fetchall()
    DB.close()
    return result

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("UPDATE game SET matches=matches+1, wins=wins+1 WHERE id = {0}".format(winner)) # winner
    cursor.execute("UPDATE game SET matches=matches+1 WHERE id = {0}".format(loser)) # loser
    DB.commit()
    DB.close()
  
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    result = []
    players = playerStandings()
    for i in range(0, len(players), 2):
        result.append(
                (players[i][0], players[i][1], players[i+1][0], players[i+1][1])
            )
    return result
