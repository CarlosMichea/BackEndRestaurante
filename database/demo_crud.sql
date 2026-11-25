-- ============================================================================
-- Demostración de CRUD directo en MariaDB (phpMyAdmin)
-- Base de datos: restaurante_db
-- Tabla generada por Django: platos_plato
-- ============================================================================

USE restaurante_db;

-- 1. READ (SELECT): Consultar todos los platos ordenados alfabéticamente
SELECT
    id,
    nombre,
    categoria,
    precio,
    stock,
    tiempo_preparacion,
    es_vegetariano,
    disponible,
    fecha_creacion
FROM platos_plato
ORDER BY nombre ASC;

-- Consultar platos disponibles filtrados por categoría
SELECT id, nombre, precio, stock
FROM platos_plato
WHERE disponible = 1 AND categoria = 'fondo';

-- 2. CREATE (INSERT): Insertar un nuevo plato directamente en la tabla
INSERT INTO platos_plato (
    nombre,
    descripcion,
    categoria,
    precio,
    stock,
    tiempo_preparacion,
    es_vegetariano,
    disponible,
    imagen_url,
    fecha_creacion,
    fecha_actualizacion
) VALUES (
    'Machas a la parmesana',
    'Machas frescas gratinadas al horno con queso parmesano, mantequilla y vino blanco.',
    'entrada',
    9200,
    10,
    15,
    0,
    1,
    '',
    NOW(),
    NOW()
);

-- Verificar el plato recién insertado
SELECT * FROM platos_plato WHERE nombre = 'Machas a la parmesana';

-- 3. UPDATE: Actualizar el precio, stock y fecha_actualizacion del plato creado
UPDATE platos_plato
SET
    precio = 9900,
    stock = 0,
    disponible = 0,
    fecha_actualizacion = NOW()
WHERE nombre = 'Machas a la parmesana';

-- Verificar los cambios aplicados
SELECT id, nombre, precio, stock, disponible, fecha_actualizacion
FROM platos_plato
WHERE nombre = 'Machas a la parmesana';

-- 4. DELETE: Eliminar el plato de prueba
DELETE FROM platos_plato
WHERE nombre = 'Machas a la parmesana';

-- Confirmar que el registro fue eliminado
SELECT COUNT(*) AS total_platos FROM platos_plato;
