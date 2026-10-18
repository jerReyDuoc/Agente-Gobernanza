-- =====================================================
-- Skill: Gestión de Derechos ARCOP
-- Consultas SQL completas para gestionar el ciclo de vida
-- =====================================================

-- 1. INSERTAR nueva solicitud ARCOP
INSERT INTO solicitudes_arcop (titular_id, tipo_derecho, estado, observaciones)
VALUES ({titular_id}, '{tipo_derecho}', 'Pendiente', '{observaciones}');

-- 2. CONSULTAR todas las solicitudes de un titular
SELECT id, tipo_derecho, estado, fecha_solicitud, fecha_resolucion, observaciones
FROM solicitudes_arcop
WHERE titular_id = {titular_id}
ORDER BY fecha_solicitud DESC;

-- 3. CONSULTAR solicitudes pendientes (todas)
SELECT s.id, t.nombre, s.tipo_derecho, s.fecha_solicitud
FROM solicitudes_arcop s
JOIN titulares t ON s.titular_id = t.id
WHERE s.estado IN ('Pendiente', 'En verificación', 'En proceso')
ORDER BY s.fecha_solicitud ASC;

-- 4. ACTUALIZAR estado a resuelta
UPDATE solicitudes_arcop
SET estado = 'Resuelta',
    fecha_resolucion = CURRENT_DATE,
    observaciones = '{observaciones}'
WHERE id = {solicitud_id};

-- 5. ALERTAR solicitudes que exceden el plazo legal (15 días hábiles)
SELECT s.id, t.nombre, t.email, s.tipo_derecho, s.fecha_solicitud,
       julianday(CURRENT_DATE) - julianday(s.fecha_solicitud) AS dias_transcurridos
FROM solicitudes_arcop s
JOIN titulares t ON s.titular_id = t.id
WHERE s.estado != 'Resuelta'
  AND julianday(CURRENT_DATE) - julianday(s.fecha_solicitud) > 15;

-- 6. ESTADÍSTICAS generales para reporte de cumplimiento
SELECT estado, COUNT(*) as total
FROM solicitudes_arcop
GROUP BY estado;