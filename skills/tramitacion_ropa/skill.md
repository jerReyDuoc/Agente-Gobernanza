# Skill: Tramitación de Registro RoPA

## Propósito
Crear el Registro de Actividades de Tratamiento (RoPA) exigido por el art. 14 de la
Ley 21.719 y la cláusula 7.5 de la ISO 42001. El RoPA documenta formalmente cada
actividad de tratamiento de datos que realiza la organización.

## Datos obligatorios del acta
1. **Nombre del tratamiento**: Identificador único de la actividad.
2. **Categoría del dato**: Tipos de datos personales tratados (ej. "identificación, contacto").
3. **Finalidad**: Propósito legítimo y específico del tratamiento.
4. **Tabla de origen**: Tabla de la base de datos donde residen los datos (ej. `titulares`).
5. **Estado de la solicitud**: Aprobado / En revisión / Rechazado.

## Reglas operativas
1. Si falta alguno de los 5 campos obligatorios, PREGUNTA al usuario antes de generar el acta.
2. Nunca inventes datos: si el usuario no especifica la categoría, pídesela.
3. Al generar el acta:
   a. Insertar el registro en la tabla `ropa_registros` (persistencia).
   b. Renderizar la plantilla HTML con los datos.
   c. Devolver el HTML completo al usuario.
4. El acta debe incluir la fecha de generación y referencia normativa.

## Formato de salida esperado
1. Confirmación de registro exitoso (texto plano).
2. Documento HTML renderizable del acta.

## Referencias normativas
- Ley 21.719, art. 14: Registro de actividades de tratamiento.
- ISO 42001, cláusula 7.5: Información documentada.