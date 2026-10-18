-- =====================================================
-- Skill: Tramitación RoPA
-- =====================================================

-- 1. INSERTAR un nuevo registro RoPA
INSERT INTO ropa_registros (
    nombre_tratamiento, categoria_datos, finalidad,
    tabla_origen, estado_solicitud, observaciones
)
VALUES (
    '{nombre_tratamiento}', '{categoria_datos}', '{finalidad}',
    '{tabla_origen}', '{estado_solicitud}', '{observaciones}'
);

-- 2. CONSULTAR todos los registros RoPA
SELECT id, nombre_tratamiento, categoria_datos, finalidad,
       tabla_origen, estado_solicitud, fecha_registro
FROM ropa_registros
ORDER BY fecha_registro DESC;

-- 3. CONSULTAR un registro específico por ID
SELECT * FROM ropa_registros WHERE id = {id};

-- 4. CONSULTAR registros por estado (para auditoría)
SELECT id, nombre_tratamiento, estado_solicitud
FROM ropa_registros
WHERE estado_solicitud = '{estado}';