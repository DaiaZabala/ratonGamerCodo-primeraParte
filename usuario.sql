-- Transacción
START TRANSACTION;

-- Crear la tabla usuario
CREATE TABLE usuario (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL,
  apellido VARCHAR(50) NOT NULL,
  nombre_usuario VARCHAR(50) NOT NULL,
  correo VARCHAR(100) NOT NULL,
  contraseña VARCHAR(100) NOT NULL,
  sexo VARCHAR(10) NOT NULL,
  pais VARCHAR(50) DEFAULT NULL,
  imagen VARCHAR(200) DEFAULT NULL,
  rol VARCHAR(8) NOT NULL
);

-- Volcado de datos para la tabla usuario
INSERT INTO usuario (nombre, apellido, nombre_usuario, correo, contrasena, sexo, pais, imagen, rol) VALUES
('daiana', 'zabala', 'anto1', 'anto@gmail.com', '130395Dai', 'Mujer', 'Argentina', 'undefined', '1'),
('lucas', 'Huenchiman', 'lucas', 'Lucas@gmail.com', '130395Lh', 'Hombre', 'Argentina', 'young-man-dressed-casual-city-sitting.jpg', '1'),
('Mateo', 'Safer', 'mateoS', 'mateo@gmail.com', '130395Ma', 'Hombre', 'Argentina', 'close-up-man-making-peace-sign-smile.jpg', '2'),
('JORGE', 'Gomez', 'jorgito', 'jorgeG@gmail.com', '130395Jg', 'Hombre', 'Argentina', 'middle-age-friends-having-fun.jpg', '2'),
('Gabriela', 'Vazquez', 'Gabi', 'gabi@gmail.com', '130395Gv', 'Hombre', 'Argentina', 'medium-shot-smiley-woman-desert.jpg', '1'),
('Estefania', 'Martinez', 'Estefi', 'estefi@gmail.com', '130395Em', 'Mujer', 'Argentina', 'pensive-caucasian-girl-with-straight-brown-hair-chilling-home-white-fascinating-woman-posing-her-apartment.jpg', '2'),
('justi', 'portel', 'justi', 'justi@gmail.com', '12345Justi', 'Mujer', 'Argentina', 'IMG_20221108_194801186.jpg', '2'),
('juan', 'q', 'juanq', 'juanq@gmail.com', 'juanQ12345', 'masculino', 'Argentina', '', '1'),
('dio', 'zava', 'dioz', 'dioz@gmail.com', '130395Dioz', 'Hombre', 'Argentina', 'IMG_20221108_194801186.jpg', '2'),
('victor', 'victor', 'victor', 'vic@gmail.com', '130395Dai', 'Mujer', 'Argentina', 'IMG_20221108_194801186.jpg', '2'),
('victor', 'vic', 'vio', 'vio@gmail.com', '130395Dai', 'Mujer', 'Argentina', 'IMG_20221108_194801186.jpg', '2');

-- Crear índices
CREATE UNIQUE INDEX usuario_nombre_usuario_idx ON usuario (nombre_usuario);
CREATE UNIQUE INDEX usuario_correo_idx ON usuario (correo);

-- Finalizar transacción
COMMIT;
