--
-- Table definitions for the tournament project.
--

-- Before importing this file, create a database called 'tournament'

CREATE TABLE tournaments (id SERIAL PRIMARY KEY,
                          name TEXT);


CREATE TABLE players (id SERIAL PRIMARY KEY,
                      name TEXT);


CREATE TABLE tournament_players (player INT REFERENCES players (id),
                                 tournament INT REFERENCES tournaments (id),
                                 PRIMARY KEY (player, tournament));


CREATE TABLE matches (id SERIAL PRIMARY KEY,
                      tournament INT REFERENCES tournaments (id),
                      winner INT REFERENCES players (id),
                      loser INT REFERENCES players (id));


CREATE VIEW player_matches AS
SELECT matches.tournament, players.id, players.name, matches.winner, matches.loser
FROM players JOIN matches
ON players.id = matches.winner
OR players.id = matches.loser;


CREATE VIEW standings AS
SELECT tournament_players.tournament, players.id, players.name, count(player_matches.*) AS matches, wins
FROM tournament_players LEFT JOIN players 
ON player = players.id
LEFT JOIN player_matches
ON players.id = player_matches.id
LEFT JOIN (SELECT players.id, count(winner) AS wins 
           FROM players LEFT JOIN matches
           ON players.id = winner
           GROUP BY players.id) as winners
ON players.id = winners.id
GROUP BY tournament_players.tournament, players.id, players.name, wins
ORDER BY tournament_players.tournament, wins DESC;