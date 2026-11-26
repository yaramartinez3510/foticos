-- Esquema local de PARTZONE para XAMPP / MariaDB.
-- CREATE IF NOT EXISTS conserva las tablas y registros que ya existan.

CREATE DATABASE IF NOT EXISTS partzone
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_spanish_ci;

USE partzone;

CREATE TABLE IF NOT EXISTS usuario (
  id INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(150) NOT NULL,
  correo VARCHAR(150) NOT NULL,
  telefono VARCHAR(20) NOT NULL,
  clave VARCHAR(255) NOT NULL,
  perfil CHAR(1) NOT NULL DEFAULT 'U',
  PRIMARY KEY (id),
  UNIQUE KEY correo (correo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

CREATE TABLE IF NOT EXISTS tipo_autoparte (
  id_tipo INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(150) NOT NULL,
  descripcion VARCHAR(150) NOT NULL,
  PRIMARY KEY (id_tipo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

CREATE TABLE IF NOT EXISTS autoparte (
  id_autoparte INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(150) NOT NULL,
  marca VARCHAR(150) NOT NULL,
  descripcion VARCHAR(300) NOT NULL,
  precio FLOAT NOT NULL,
  stock INT NOT NULL,
  id_tipo INT NOT NULL,
  imagen VARCHAR(255) NOT NULL,
  PRIMARY KEY (id_autoparte),
  KEY id_tipo (id_tipo),
  CONSTRAINT autoparte_ibfk_1 FOREIGN KEY (id_tipo)
    REFERENCES tipo_autoparte (id_tipo) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

CREATE TABLE IF NOT EXISTS pedido (
  id_pedido INT NOT NULL AUTO_INCREMENT,
  fecha DATE NOT NULL,
  estado VARCHAR(150) NOT NULL,
  total FLOAT NOT NULL,
  id_usuario INT NOT NULL,
  PRIMARY KEY (id_pedido),
  KEY id_usuario (id_usuario),
  CONSTRAINT pedido_ibfk_1 FOREIGN KEY (id_usuario)
    REFERENCES usuario (id) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

CREATE TABLE IF NOT EXISTS clasifica (
  id_clasifica INT NOT NULL AUTO_INCREMENT,
  id_tipo INT NOT NULL,
  id_autoparte INT NOT NULL,
  id_usuario INT NOT NULL,
  PRIMARY KEY (id_clasifica),
  KEY id_tipo (id_tipo),
  KEY id_autoparte (id_autoparte),
  KEY id_usuario (id_usuario),
  CONSTRAINT clasifica_ibfk_1 FOREIGN KEY (id_usuario)
    REFERENCES usuario (id) ON UPDATE CASCADE,
  CONSTRAINT clasifica_ibfk_2 FOREIGN KEY (id_tipo)
    REFERENCES tipo_autoparte (id_tipo) ON UPDATE CASCADE,
  CONSTRAINT clasifica_ibfk_3 FOREIGN KEY (id_autoparte)
    REFERENCES autoparte (id_autoparte) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

CREATE TABLE IF NOT EXISTS cotiene (
  id_contiene INT NOT NULL AUTO_INCREMENT,
  id_autoparte INT NOT NULL,
  id_pedido INT NOT NULL,
  cantidad INT NOT NULL,
  precio_unitario FLOAT NOT NULL,
  PRIMARY KEY (id_contiene),
  KEY id_autoparte (id_autoparte),
  KEY id_pedido (id_pedido),
  CONSTRAINT cotiene_ibfk_1 FOREIGN KEY (id_pedido)
    REFERENCES pedido (id_pedido) ON UPDATE CASCADE,
  CONSTRAINT cotiene_ibfk_2 FOREIGN KEY (id_autoparte)
    REFERENCES autoparte (id_autoparte) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

CREATE TABLE IF NOT EXISTS realiza (
  id_realiza INT NOT NULL AUTO_INCREMENT,
  id_usuario INT NOT NULL,
  id_pedido INT NOT NULL,
  perfil VARCHAR(150) NOT NULL,
  PRIMARY KEY (id_realiza),
  KEY id_pedido (id_pedido),
  KEY id_usuario (id_usuario),
  CONSTRAINT realiza_ibfk_1 FOREIGN KEY (id_usuario)
    REFERENCES usuario (id) ON UPDATE CASCADE,
  CONSTRAINT realiza_ibfk_2 FOREIGN KEY (id_pedido)
    REFERENCES pedido (id_pedido) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

CREATE TABLE IF NOT EXISTS aviso_disponibilidad (
  id_aviso INT NOT NULL AUTO_INCREMENT,
  correo VARCHAR(150) NOT NULL,
  marca VARCHAR(100) NOT NULL,
  modelo VARCHAR(100) NOT NULL,
  id_usuario INT NULL,
  fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_aviso),
  KEY id_usuario (id_usuario),
  CONSTRAINT aviso_disponibilidad_ibfk_1 FOREIGN KEY (id_usuario)
    REFERENCES usuario (id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;
