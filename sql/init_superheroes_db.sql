-- Script para inicializar la base de datos de superhéroes
-- Este script crea todas las tablas necesarias y algunas relaciones básicas

-- Eliminar la base de datos si existe
DROP DATABASE IF EXISTS superheroes;

-- Crear la base de datos
CREATE DATABASE superheroes;

-- Usar la base de datos
USE superheroes;

-- Tabla de géneros
CREATE TABLE gender (
    id INT AUTO_INCREMENT PRIMARY KEY,
    gender VARCHAR(50) NOT NULL
);

-- Tabla de colores (para ojos, cabello y piel)
CREATE TABLE colour (
    id INT AUTO_INCREMENT PRIMARY KEY,
    colour VARCHAR(50) NOT NULL
);

-- Tabla de razas
CREATE TABLE race (
    id INT AUTO_INCREMENT PRIMARY KEY,
    race VARCHAR(100) NOT NULL
);

-- Tabla de alineaciones (buenos, malos, neutrales)
CREATE TABLE alignment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    alignment VARCHAR(50) NOT NULL
);

-- Tabla de editoriales
CREATE TABLE publisher (
    id INT AUTO_INCREMENT PRIMARY KEY,
    publisher_name VARCHAR(100) NOT NULL
);

-- Tabla de atributos
CREATE TABLE attribute (
    id INT AUTO_INCREMENT PRIMARY KEY,
    attribute_name VARCHAR(100) NOT NULL
);

-- Tabla de superpoderes
CREATE TABLE superpower (
    id INT AUTO_INCREMENT PRIMARY KEY,
    power_name VARCHAR(100) NOT NULL
);

-- Tabla principal de superhéroes
CREATE TABLE superhero (
    id INT AUTO_INCREMENT PRIMARY KEY,
    superhero_name VARCHAR(100) NOT NULL,
    full_name VARCHAR(200),
    gender_id INT,
    eye_colour_id INT,
    hair_colour_id INT,
    skin_colour_id INT,
    race_id INT,
    publisher_id INT,
    alignment_id INT,
    height_cm FLOAT,
    weight_kg FLOAT,
    FOREIGN KEY (gender_id) REFERENCES gender(id),
    FOREIGN KEY (eye_colour_id) REFERENCES colour(id),
    FOREIGN KEY (hair_colour_id) REFERENCES colour(id),
    FOREIGN KEY (skin_colour_id) REFERENCES colour(id),
    FOREIGN KEY (race_id) REFERENCES race(id),
    FOREIGN KEY (publisher_id) REFERENCES publisher(id),
    FOREIGN KEY (alignment_id) REFERENCES alignment(id)
);

-- Tabla de relación entre superhéroes y poderes
CREATE TABLE hero_power (
    hero_id INT,
    power_id INT,
    PRIMARY KEY (hero_id, power_id),
    FOREIGN KEY (hero_id) REFERENCES superhero(id),
    FOREIGN KEY (power_id) REFERENCES superpower(id)
);

-- Tabla de relación entre superhéroes y atributos
CREATE TABLE hero_attribute (
    hero_id INT,
    attribute_id INT,
    PRIMARY KEY (hero_id, attribute_id),
    FOREIGN KEY (hero_id) REFERENCES superhero(id),
    FOREIGN KEY (attribute_id) REFERENCES attribute(id)
);

-- Insertar algunos datos básicos en las tablas principales

-- Géneros
INSERT INTO gender (gender) VALUES 
('Male'), 
('Female'), 
('Non-Binary'), 
('Genderfluid'), 
('Unknown');

-- Colores básicos
INSERT INTO colour (colour) VALUES 
('Red'), ('Blue'), ('Green'), ('Yellow'), ('Black'), 
('White'), ('Brown'), ('Grey'), ('Purple'), ('Orange'), 
('Pink'), ('Silver'), ('Gold'), ('Multicolor'), ('None');

-- Razas
INSERT INTO race (race) VALUES 
('Human'), ('Alien'), ('Mutant'), ('God/Eternal'), ('Android'), 
('Cyborg'), ('Demon'), ('Animal'), ('Unknown'), ('Other');

-- Alineaciones
INSERT INTO alignment (alignment) VALUES 
('Good'), ('Bad'), ('Neutral'), ('Unknown');

-- Editoriales principales
INSERT INTO publisher (publisher_name) VALUES 
('Marvel Comics'), ('DC Comics'), ('Dark Horse Comics'), 
('Image Comics'), ('Vertigo'), ('Wildstorm'), ('IDW Publishing');

-- Algunos atributos de superhéroes
INSERT INTO attribute (attribute_name) VALUES 
('Intelligent'), ('Strong'), ('Fast'), ('Durable'), ('Energy Projection'), 
('Fighting Skills'), ('Leadership'), ('Strategic Mind'), ('Immortal'), ('Magical');

-- Algunos superpoderes básicos
INSERT INTO superpower (power_name) VALUES 
('Super Strength'), ('Flight'), ('Super Speed'), ('Invulnerability'), 
('Telekinesis'), ('Telepathy'), ('Energy Blasts'), ('Healing Factor'), 
('Invisibility'), ('Shape-shifting'), ('Time Manipulation'), ('Magic');

-- Insertar algunos superhéroes de ejemplo
INSERT INTO superhero (superhero_name, full_name, gender_id, eye_colour_id, hair_colour_id, skin_colour_id, race_id, publisher_id, alignment_id, height_cm, weight_kg) VALUES 
('Superman', 'Clark Kent', 1, 2, 5, 6, 2, 2, 1, 191, 107),
('Spider-Man', 'Peter Parker', 1, 5, 5, 6, 1, 1, 1, 178, 76),
('Wonder Woman', 'Diana Prince', 2, 2, 5, 6, 4, 2, 1, 183, 74),
('Batman', 'Bruce Wayne', 1, 2, 5, 6, 1, 2, 1, 188, 95),
('Iron Man', 'Tony Stark', 1, 5, 5, 6, 1, 1, 1, 185, 102),
('Hulk', 'Bruce Banner', 1, 3, 5, 3, 3, 1, 3, 244, 635),
('Black Widow', 'Natasha Romanoff', 2, 3, 1, 6, 1, 1, 1, 170, 59),
('Joker', 'Unknown', 1, 3, 3, 6, 1, 2, 2, 185, 80);

-- Asignar poderes a los superhéroes
INSERT INTO hero_power (hero_id, power_id) VALUES 
(1, 1), (1, 2), (1, 3), (1, 4), -- Superman
(2, 1), (2, 3), -- Spider-Man
(3, 1), (3, 2), (3, 4), -- Wonder Woman
(4, 6), -- Batman (sin superpoderes pero habilidades)
(5, 2), (5, 7), -- Iron Man
(6, 1), (6, 4), (6, 8), -- Hulk
(7, 3), (7, 6), -- Black Widow
(8, 10); -- Joker

-- Asignar atributos a los superhéroes
INSERT INTO hero_attribute (hero_id, attribute_id) VALUES 
(1, 2), (1, 3), (1, 4), -- Superman
(2, 1), (2, 3), (2, 6), -- Spider-Man
(3, 2), (3, 6), (3, 7), -- Wonder Woman
(4, 1), (4, 6), (4, 8), -- Batman
(5, 1), (5, 7), (5, 8), -- Iron Man
(6, 2), (6, 4), -- Hulk
(7, 3), (7, 6), -- Black Widow
(8, 1); -- Joker