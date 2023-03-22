-- BELT REVIEW

-- SELECT Queries
SELECT * FROM users;
SELECT * FROM recipes;

-- GEt all the recipes and their chef
SELECT * FROM recipes 
JOIN users
ON recipes.user_id = users.id;

-- INSERT Queries
INSERT INTO recipes (name, description, instructions, date, under_thirty, user_id)
VALUES ("Arroz", "Arroz blanco", "Boil pot of water, add rice, add oil and salt. cover for 30 mins", NOW(), 0, 1);

INSERT INTO recipes (name, description, instructions, date, under_thirty, user_id)
VALUES ("Habichuela", "frijoles", "10 mins", NOW(), 1, 2);

INSERT INTO users (first_name, last_name, email,

INSERT INTO recipes 
JOIN users
ON users.id = parties.user_id
WHERE id

UPDATE recipes 
SET name = " ", 
description = %()s, 
instructions = %()s,
under_thirty = %()s, 
date = %()s
WHERE id = %()s; 



