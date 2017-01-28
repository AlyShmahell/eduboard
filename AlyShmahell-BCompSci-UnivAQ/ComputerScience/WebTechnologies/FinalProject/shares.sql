CREATE TABLE shares(
`shareholderid` VARCHAR(767) NOT NULL,
`stocksymbol` VARCHAR(10) NOT NULL,
`stockcount` INT(30) NOT NULL,
PRIMARY KEY (`shareholderid`,`stocksymbol`)
);
