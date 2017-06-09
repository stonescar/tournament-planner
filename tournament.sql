-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP VIEW standings;
DROP VIEW player_matches;
DROP TABLE matches;
DROP TABLE players;

CREATE TABLE players (id SERIAL PRIMARY KEY,
                      name TEXT);


CREATE TABLE matches (id SERIAL PRIMARY KEY,
                      winner INT REFERENCES players (id),
                      loser INT REFERENCES players (id));

INSERT INTO players (name) VALUES ('Steinar');
INSERT INTO players (name) VALUES ('Harald');
INSERT INTO players (name) VALUES ('John');
INSERT INTO players (name) VALUES ('Peter');

INSERT INTO matches (winner, loser) VALUES (1, 2);
INSERT INTO matches (winner, loser) VALUES (3, 4);
INSERT INTO matches (winner, loser) VALUES (1, 3);
INSERT INTO matches (winner, loser) VALUES (4, 2);
INSERT INTO matches (winner, loser) VALUES (1, 4);
INSERT INTO matches (winner, loser) VALUES (3, 2);

CREATE VIEW player_matches AS
SELECT players.id, players.name, matches.winner, matches.loser
FROM players JOIN matches
ON players.id = matches.winner
OR players.id = matches.loser;

CREATE VIEW standings AS
SELECT players.id, players.name, count(player_matches.*) AS matches, wins
FROM players LEFT JOIN player_matches
ON players.id = player_matches.id
LEFT JOIN (SELECT players.id, count(winner) AS wins 
           FROM players LEFT JOIN matches
           ON players.id = winner
           GROUP BY players.id) as winners
ON players.id = winners.id
GROUP BY players.id, players.name, wins
ORDER BY wins DESC;