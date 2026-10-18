-- =====================================================
-- Skill: Evaluar Documento
-- Consultas de contexto para enriquecer la evaluación
-- =====================================================

-- 1. Obtener los tratamientos de mayor riesgo (para verificar si el documento
--    cubre los tratamientos críticos de la empresa)
SELECT id, nombre, finalidad, nivel_riesgo
FROM tratamientos
WHERE nivel_riesgo = 'Alto'
ORDER BY nombre;

-- 2. Obtener titulares que NO han otorgado consentimiento
--    (si el documento los menciona, debe explicar cómo obtenerlo)
SELECT id, nombre, email
FROM titulares
WHERE consentimiento_otorgado = 0;

-- 3. Historial de solicitudes ARCOP (para verificar si el documento informa
--    correctamente cómo ejercer los derechos)
SELECT tipo_derecho, COUNT(*) as cantidad
FROM solicitudes_arcop
GROUP BY tipo_derecho
ORDER BY cantidad DESC;