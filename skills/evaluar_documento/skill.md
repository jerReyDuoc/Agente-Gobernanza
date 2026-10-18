# Skill: Evaluar Documento de Cumplimiento Normativo

## Propósito
Analizar un documento (consentimiento, política de privacidad, aviso legal, etc.) y determinar
si cumple con la Ley 21.719 de Chile y los principios de la ISO 42001.

## Marco normativo de referencia
- **Ley 21.719** (Protección de Datos Personales, Chile)
- **ISO 42001** (Sistema de Gestión de Inteligencia Artificial)

## Checklist de evaluación

### A. Principios de la Ley 21.719
1. **Consentimiento**: Debe ser libre, informado, específico e inequívoco. No puede ser tácito ni
   presumido por silencio.
2. **Finalidad**: Debe estar determinada, explícita y legítima. Prohibido "cualquier finalidad".
3. **Proporcionalidad**: Solo se recogen datos adecuados y necesarios para la finalidad.
4. **Información al titular**: Debe mencionar el responsable del tratamiento, la base legal,
   los plazos de conservación y los derechos ARCOP.
5. **Derechos ARCOP**: Debe informar al titular sobre sus derechos de Acceso, Rectificación,
   Cancelación, Oposición y Portabilidad, y cómo ejercerlos.
6. **Revocabilidad**: El titular debe poder revocar el consentimiento en cualquier momento.

### B. Principios de la ISO 42001
1. **Transparencia**: El sistema de IA debe ser explicable y auditable.
2. **Supervisión humana**: Debe existir control humano sobre decisiones automatizadas.
3. **Gestión de riesgos**: Se debe identificar el nivel de riesgo del tratamiento de datos.
4. **Seguridad**: Medidas técnicas y organizativas que garanticen confidencialidad e integridad.

## Metodología
1. Leer el documento completo.
2. Verificar cada ítem del checklist (A y B).
3. Asignar una puntuación de 0 a 10.
4. Emitir un veredicto: CUMPLE / CUMPLE PARCIALMENTE / NO CUMPLE.
5. Entregar recomendaciones concretas y accionables.

## Formato de salida esperado (JSON)
```json
{
  "veredicto": "CUMPLE | CUMPLE PARCIALMENTE | NO CUMPLE",
  "puntuacion": "X/10",
  "hallazgos_ley_21719": {
    "consentimiento": "OK / FALLA: motivo",
    "finalidad": "OK / FALLA: motivo",
    "proporcionalidad": "OK / FALLA: motivo",
    "informacion_titular": "OK / FALLA: motivo",
    "derechos_arcop": "OK / FALLA: motivo",
    "revocabilidad": "OK / FALLA: motivo"
  },
  "hallazgos_iso_42001": {
    "transparencia": "OK / FALLA: motivo",
    "supervision_humana": "OK / FALLA: motivo",
    "gestion_riesgos": "OK / FALLA: motivo",
    "seguridad": "OK / FALLA: motivo"
  },
  "recomendaciones": ["lista de mejoras concretas"]
}