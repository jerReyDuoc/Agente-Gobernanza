# Habilidad: Generar Documento de Consentimiento (Ley 21.719)

## Descripción
Esta habilidad permite generar un documento legal de consentimiento para el tratamiento de datos personales, alineado con los estándares de la Ley 21.719 de Chile.

## Instrucciones para el Agente
1. Solicita el nombre del titular y la finalidad del tratamiento.
2. Utiliza la plantilla HTML base (`plantilla.html`).
3. Reemplaza las variables `{{nombre}}` y `{{finalidad}}` con los datos proporcionados por el usuario.
4. Devuelve el código HTML resultante.