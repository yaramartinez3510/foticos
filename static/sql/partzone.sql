-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 26-10-2026 a las 16:27:37
-- Versión del servidor: 8.0.44
-- Versión de PHP: 7.4.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `partzone`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `autoparte`
--

CREATE TABLE `autoparte` (
  `id_autoparte` int NOT NULL,
  `nombre` varchar(150) COLLATE utf8mb4_spanish_ci NOT NULL,
  `marca` varchar(150) COLLATE utf8mb4_spanish_ci NOT NULL,
  `descripcion` varchar(300) COLLATE utf8mb4_spanish_ci NOT NULL,
  `precio` float NOT NULL,
  `stock` int NOT NULL,
  `id_tipo` int NOT NULL,
  `imagen` varchar(20) COLLATE utf8mb4_spanish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clasifica`
--

CREATE TABLE `clasifica` (
  `id_clasifica` int NOT NULL,
  `id_tipo` int NOT NULL,
  `id_autoparte` int NOT NULL,
  `id_usuario` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cotiene`
--

CREATE TABLE `cotiene` (
  `id_contiene` int NOT NULL,
  `id_autoparte` int NOT NULL,
  `id_pedido` int NOT NULL,
  `cantidad` int NOT NULL,
  `precio_unitario` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedido`
--

CREATE TABLE `pedido` (
  `id_pedido` int NOT NULL,
  `fecha` date NOT NULL,
  `estado` varchar(150) COLLATE utf8mb4_spanish_ci NOT NULL,
  `total` float NOT NULL,
  `id_usuario` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `realiza`
--

CREATE TABLE `realiza` (
  `id_realiza` int NOT NULL,
  `id_usuario` int NOT NULL,
  `id_pedido` int NOT NULL,
  `perfil` varchar(150) COLLATE utf8mb4_spanish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_autoparte`
--

CREATE TABLE `tipo_autoparte` (
  `id_tipo` int NOT NULL,
  `nombre` varchar(150) COLLATE utf8mb4_spanish_ci NOT NULL,
  `descripcion` varchar(150) COLLATE utf8mb4_spanish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `id` int NOT NULL,
  `nombre` varchar(150) CHARACTER SET utf32 COLLATE utf32_spanish_ci NOT NULL,
  `correo` varchar(150) CHARACTER SET utf32 COLLATE utf32_spanish_ci NOT NULL,
  `clave` varchar(200) CHARACTER SET utf32 COLLATE utf32_spanish_ci NOT NULL,
  `perfil` char(1) CHARACTER SET utf32 COLLATE utf32_spanish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf32 COLLATE=utf32_spanish_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`id`, `nombre`, `correo`, `clave`, `perfil`) VALUES
(1, 'Yara Victoria Martinez Sanchez', 'ya.sanc27@gmail.com', 'scrypt:32768:8:1$gdK4vbpskpiDwO3D$200291364e0e2c1b75905a4176ba5cf1bf35fa86ffcec0264d5fe63c0efe25ff6e5fcd322131f308d5b50a78ca2c8c6735ad9d68a697015db206f693c0e87c47', 'U');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `autoparte`
--
ALTER TABLE `autoparte`
  ADD PRIMARY KEY (`id_autoparte`),
  ADD KEY `id_tipo` (`id_tipo`);

--
-- Indices de la tabla `clasifica`
--
ALTER TABLE `clasifica`
  ADD PRIMARY KEY (`id_clasifica`),
  ADD KEY `id_tipo` (`id_tipo`),
  ADD KEY `id_autoparte` (`id_autoparte`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `cotiene`
--
ALTER TABLE `cotiene`
  ADD PRIMARY KEY (`id_contiene`),
  ADD KEY `id_autoparte` (`id_autoparte`),
  ADD KEY `id_pedido` (`id_pedido`);

--
-- Indices de la tabla `pedido`
--
ALTER TABLE `pedido`
  ADD PRIMARY KEY (`id_pedido`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `realiza`
--
ALTER TABLE `realiza`
  ADD PRIMARY KEY (`id_realiza`),
  ADD KEY `id_pedido` (`id_pedido`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `tipo_autoparte`
--
ALTER TABLE `tipo_autoparte`
  ADD PRIMARY KEY (`id_tipo`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `correo` (`correo`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `autoparte`
--
ALTER TABLE `autoparte`
  MODIFY `id_autoparte` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `clasifica`
--
ALTER TABLE `clasifica`
  MODIFY `id_clasifica` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `cotiene`
--
ALTER TABLE `cotiene`
  MODIFY `id_contiene` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `pedido`
--
ALTER TABLE `pedido`
  MODIFY `id_pedido` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `realiza`
--
ALTER TABLE `realiza`
  MODIFY `id_realiza` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `tipo_autoparte`
--
ALTER TABLE `tipo_autoparte`
  MODIFY `id_tipo` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `autoparte`
--
ALTER TABLE `autoparte`
  ADD CONSTRAINT `autoparte_ibfk_1` FOREIGN KEY (`id_tipo`) REFERENCES `tipo_autoparte` (`id_tipo`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `clasifica`
--
ALTER TABLE `clasifica`
  ADD CONSTRAINT `clasifica_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `clasifica_ibfk_2` FOREIGN KEY (`id_tipo`) REFERENCES `tipo_autoparte` (`id_tipo`) ON UPDATE CASCADE,
  ADD CONSTRAINT `clasifica_ibfk_3` FOREIGN KEY (`id_autoparte`) REFERENCES `autoparte` (`id_autoparte`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `cotiene`
--
ALTER TABLE `cotiene`
  ADD CONSTRAINT `cotiene_ibfk_1` FOREIGN KEY (`id_pedido`) REFERENCES `pedido` (`id_pedido`) ON UPDATE CASCADE,
  ADD CONSTRAINT `cotiene_ibfk_2` FOREIGN KEY (`id_autoparte`) REFERENCES `autoparte` (`id_autoparte`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `pedido`
--
ALTER TABLE `pedido`
  ADD CONSTRAINT `pedido_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `realiza`
--
ALTER TABLE `realiza`
  ADD CONSTRAINT `realiza_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `realiza_ibfk_2` FOREIGN KEY (`id_pedido`) REFERENCES `pedido` (`id_pedido`) ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
