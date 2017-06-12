# Tournament planner

Tournament planner is a tool for planning and keeping scores of game or sports tournaments. It uses a Swiss pairing system where players compete agains others on their same level, based on results in the tournament.

## Functionality
The 

## The database schema
Listed below are the tables the data is stored in and the views that hav been created to retreieve the data easily. For each table or view is an example table showing how the tables and views could look like. Values in tables in parentheses shows the value that the foreign key points to.

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
| 2 _(Tournament 2)_ | 3 | Rachel | 3 | 7 _(Peter)_
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
