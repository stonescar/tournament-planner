# Tournament planner

Tournament planner is a tool for planning and keeping scores of game or sports tournaments. It uses a Swiss pairing system where players compete against others on their same level, based on results in the tournament.

## About
The program uses PostgreSQL, Virtual Box, Vagrant, Psychopg2 and Python 2.7 to create a back-end solution for managing a tournament after the Swiss model. In a Swiss model tournament players do not get knocked out, but in each round they play agains players who have the same amount of wins as they have.

## Requirements
To use the module, you first need to install the following:
* [Python2.7](http://python.org)
* [Virtual Box](https://www.virtualbox.org/wiki/Downloads)
* [Vagrant](https://www.vagrantup.com/downloads.html)
* [GIT](https://git-scm.com/downloads) _(Recommended)_

## Installation
1. Install all software listed above.
2. In GIT, cd to your project folder and type<br>
    `git clone https://github.com/udacity/fullstack-nanodegree-vm`
3. Inside the vagrant folder, clone this repository<br>
    `git clone https://github.com/stonescar/tournament-planner`
4. Type `vagrant up` to boot your virtual machine (This might take a while...)
5. When the VM is booted, log in with `vagrant ssh`
6. cd to the tournament planner folder with `cd /vagrant/tournament-planner`
7. To build the database, type `psql`, then `\i tournament.sql`
8. Press `CTRL+D` to exit psql
9. You can now run the example program with `python play.py` or build your project and import tournament.py

## The files
| Filename | Description |
|-|-|
| tournament.py | Contains the functions to create new tournaments, add players, report matches, views standings etc. This is the file you must import to your project. |
| tournament.sql | Contains all the database, table and view schemas |
| tournament-test.py | A file to test the functionality in `tournament.py` |
| play.py | An example of how the `tournament.py` file can be used. |
| LICENSE | License file for this project |
| README.md | This readme file |

## Functions
A short description of the functions in `tournament.py`. Se the docstrings for more detailed information.
* __connect()__: Sets up and returns a database connection. Edit this to fit your database
* __deleteTournaments()__: Deletes _ALL_ tournaments
* __deleteTournament(id)__: Deletes a tournament
* __deleteMatches(tournament)__: Deletes all matches, or just all matches for a given tournament
* __deletePlayers()__: Deletes _ALL_ players
* __newTournament(name)__: Creates a new tournament
* __countPlayers(tournament)__: Counts _ALL_ players in the database, or just those assigned to a given tournament
* __registerPlayer(name)__: Adds a new player to the database
* __assignPlayers(tournament, *players)__: Assigns a list of players to a tournament
* __quicktournament(t_name, *players)__: Creates a new tournament and adds assigns players to it
* __playerStandings(tournament)__: Returns a list of all players in a tournament, sorted by wins
* __reportMatch(tournament, winner, loser)__: Report the outcome of a match
* __swissPairings(tournament)__: Returns a list of pairs of players based on the Swiss model
* __randomPairings(tournament)__: Returns a lis of random pairs of players

## The database schema
Listed below are the tables the data is stored in and the views that have been created to retreieve the data easily. For each table or view is an example table showing how the tables and views could look like. Values in tables in parentheses shows the value that the foreign key points to.

### Tables
##### players
Holds the unique `id` of the player as a primary key, and the player's `name` as a text value.

| id | name |
|-|-|
| 1 | Steinar |
| 2 | Mike |
| 3 | Rachel |
| 4 | Steve |
| 5 | Molly |
| 6 | Janet |
| 7 | Peter |

#### tournaments
Holds the unique `id` of the tournament as a primary key, and the tournament `name` as a text value:

| id | name |
|-|-|
| 1 | myTournament |
| 2 | Tournament 2 |

#### tournament_players
Assigns players to tournaments. `player` references to the `id` field in the players table, and `tournament` references to the `id` in the tournaments table. This way a user can be in many different tournaments.

| tournament | player |
|-|-|
| 1 _(myTournament)_ | 1 _(Steinar)_ |
| 1 _(myTournament)_ | 2 _(Mike)_ |
| 1 _(myTournament)_ | 3 _(Rachel)_ |
| 1 _(myTournament)_ | 4 _(Steve)_ |
| 2 _(Tournament 2)_ | 3 _(Rachel)_ |
| 2_(Tournament 2)_ | 5 _(Molly)_ |
| 2_(Tournament 2)_ | 6 _(Janet)_ |
| 2_(Tournament 2)_ | 7 _(Peter)_ |

#### matches
Stores results of matches in all tournaments. Hold the unique `id` of the match as a primary key, `tournament` references to the `id` field in the tournament table and tells which tournement the match was part of, while `winner` and `loser` references to the `id` field in the players table representing the two players in the match, where the winner of the match is set as `winner`.

| id | tournament | winner | loser |
|-|-|-|-|
| 1 | 1 _(myTournament)_ | 1 _(Steinar)_ | 4 _(Steve)_ |
| 2 | 1 _(myTournament)_ | 3 _(Rachel)_ | 2 _(Mike)_ |
| 3 | 1 _(myTournament)_ | 1 _(Steinar)_ | 3 _(Rachel)_ |
| 4 | 1 _(myTournament)_ | 2 _(Mike)_ | 4 _(Steve)_ |
| 5 | 2 _(Tournament 2)_ | 3 _(Rachel)_ | 7 _(Peter)_ |
| 6 | 2 _(Tournament 2)_ | 6 _(Janet)_ | 5 _(Molly)_ |

### Views
#### player_matches
Temporary view that lists _all_ matches for all players. So all the matches a player has played will be listed in this view and connected to his id and name. `tournament` references to the `id` field of the tournaments table for later sorting and selecting. `id` and `name` references to the player's id and name in the players table. `winner` and `loser` holds the ids of the player in the match, with `winner` showing who won.
This view is only used for further selecting, sorting and grouping, i.e. in the standings view.

| tournament | id | name | winner | loser |
|-|-|-|-|-|
| 1 _(myTournament)_ | 1 | Steinar | 1 | 4 _(Steve)_ |
| 1 _(myTournament)_ | 1 | Steinar | 1 | 3 _(Rachel)_ |
| 1 _(myTournament)_ | 2 | Mike | 2 | 4 _(Steve)_ |
| 1 _(myTournament)_ | 2 | Mike | 3 _(Rachel)_ | 2 |
| 1 _(myTournament)_ | 3 | Rachel | 1 _(Steinar)_ | 3 |
| 1 _(myTournament)_ | 3 | Rachel | 3 | 2 _(Mike)_ |
| ... | ... | ... | ... | ... |
| 2 _(Tournament 2)_ | 3 | Rachel | 3 | 7 _(Peter)_ |
| ... | ... | ... | ... | ... |

#### standings
Shows the current standings of all tournaments. Lists all players, sorted by number of wins. Includes `tournament` (`id` of tournament), `id` (player's `id`), `name` (player's `name`), `matches` (the total number of matches the player has played) and `wins` (the total number of matches the player has won. Use `...WHERE tournament = [tournament-id]` to only show standings for one tournament.

| tournament | id | name | matches | wins |
|-|-|-|-|-|
| 1 _(myTournament)_ | 1 | Steinar | 2 | 2 |
| 1 _(myTournament)_ | 3 | Rachel | 2 | 1 |
| 1 _(myTournament)_ | 2 | Mike | 2 | 1 |
| 1 _(myTournament)_ | 1 | Steve | 2 | 0 |
| 2 _(Tournament 2)_ | 3 | Rachel | 1 | 1 |
| 2 _(Tournament 2)_ | 6 | Janet | 1 | 1 |
| 2 _(Tournament 2)_ | 7 | Peter | 1 | 0 |
| 2 _(Tournament 2)_ | 5 | Molly | 1 | 0 |

## Licensing
This project is licensed under the [MIT License](LICENSE).
