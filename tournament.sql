-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
--
-- Via Vladimir Vyazovetskov
-- http://erhosen.github.io/

CREATE TABLE game(
	id SERIAL PRIMARY KEY,
	name TEXT,
	wins INTEGER DEFAULT 0,
	matches INTEGER DEFAULT 0
);