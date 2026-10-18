# Skill: Gestión de Derechos ARCOP

## Propósito
Gestionar el ciclo de vida completo de las solicitudes de derechos ARCOP que los titulares
ejercen sobre sus datos personales, en cumplimiento de la Ley 21.719.

## ¿Qué es ARCOP?
- **A - Acceso**: El titular puede solicitar y obtener copia de los datos que la empresa tiene sobre él.
- **R - Rectificación**: El titular puede corregir datos inexactos o incompletos.
- **C - Cancelación**: El titular puede pedir la eliminación de sus datos cuando ya no sean necesarios.
- **O - Oposición**: El titular puede oponerse al tratamiento de sus datos por motivos legítimos.
- **P - Portabilidad**: El titular puede solicitar sus datos en un formato estructurado y reutilizable.

## Plazos legales (Ley 21.719)
- **Plazo de respuesta**: 15 días hábiles desde la recepción de la solicitud.
- **Prórroga excepcional**: 15 días adicionales por complejidad, con notificación al titular.
- **Silencio administrativo**: Si no se responde en plazo, se entiende acogida la solicitud.

## Estados del flujo de trabajo
1. **Pendiente**: Solicitud recibida, aún no procesada.
2. **En verificación**: Se está validando la identidad del titular.
3. **En proceso**: Se está ejecutando la acción (eliminar, rectificar, etc.).
4. **Resuelta**: La solicitud fue completada y notificada al titular.
5. **Rechazada**: No se pudo acoger por motivos legales justificados.

## Reglas operativas
1. Siempre verificar que el `titular_id` exista antes de registrar una solicitud.
2. Registrar la fecha de solicitud automáticamente (default CURRENT_DATE).
3. Al resolver, actualizar `fecha_resolucion` con la fecha actual.
4. Documentar en `observaciones` el motivo del rechazo o el detalle de la resolución.
5. Alertar si una solicitud lleva más de 15 días sin resolver (posible incumplimiento legal).

## Cómo procesar cada tipo de derecho
- **Acceso** → Generar reporte completo de datos del titular (tratamientos, historial).
- **Rectificación** → Solicitar documento de respaldo y actualizar la tabla `titulares`.
- **Cancelación** → Eliminar/anonymizar datos, salvo obligación legal de conservación.
- **Oposición** → Evaluar la base legal; si es interés legítimo, se puede acoger.
- **Portabilidad** → Exportar datos en JSON o CSV estructurado.