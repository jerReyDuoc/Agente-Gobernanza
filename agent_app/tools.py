import sqlite3
import os
from langchain_core.tools import tool

# Ruta a la base de datos (asegúrate de que se ejecute desde la raíz del proyecto)
DB_PATH = "empresa_gobernanza.db"

def verificar_db():
    """Verifica que la BD exista y tenga todas las tablas necesarias.
    Si falta algo, la regenera automáticamente."""
    import sqlite3
    tablas_requeridas = {"titulares", "tratamientos", "solicitudes_arcop", "ropa_registros"}
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tablas_actuales = {row[0] for row in cursor.fetchall()}
        conn.close()
        
        if not tablas_requeridas.issubset(tablas_actuales):
            print(f"⚠️ BD incompleta. Faltan: {tablas_requeridas - tablas_actuales}")
            print("🔧 Regenerando base de datos...")
            # Importar y ejecutar el seed
            import sys
            from pathlib import Path
            sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
            from data.seed import crear_base_datos
            crear_base_datos()
    except Exception as e:
        print(f"Error verificando DB: {e}")

# Ejecutar la verificación al importar el módulo
verificar_db()
# ==========================================
# HERRAMIENTA 1: GESTIÓN ARCOP (Base de Datos)
# ==========================================
@tool
def registrar_solicitud_arcop(titular_id: int, tipo_derecho: str) -> str:
    """Registra una nueva solicitud de derecho ARCOP (Acceso, Rectificación, Cancelación, Oposición, Portabilidad) en la base de datos de la empresa.
    
    Args:
        titular_id: El ID numérico del titular de los datos.
        tipo_derecho: El tipo de derecho a ejercer (ej. 'Acceso', 'Cancelacion').
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO solicitudes_arcop (titular_id, tipo_derecho, estado) VALUES (?, ?, 'Pendiente')",
            (titular_id, tipo_derecho)
        )
        conn.commit()
        conn.close()
        return f"Éxito: Solicitud ARCOP de tipo '{tipo_derecho}' registrada para el titular ID {titular_id}."
    except Exception as e:
        return f"Error al registrar la solicitud: {str(e)}"

@tool
def consultar_solicitudes_arcop(titular_id: int) -> str:
    """Consulta el estado de las solicitudes ARCOP de un titular específico en la base de datos.
    
    Args:
        titular_id: El ID numérico del titular de los datos.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, tipo_derecho, estado, fecha_solicitud FROM solicitudes_arcop WHERE titular_id = ?", (titular_id,))
        resultados = cursor.fetchall()
        conn.close()
        
        if not resultados:
            return f"No se encontraron solicitudes ARCOP para el titular ID {titular_id}."
        
        respuesta = f"Solicitudes encontradas para el titular {titular_id}:\n"
        for row in resultados:
            respuesta += f"- ID Solicitud: {row[0]}, Derecho: {row[1]}, Estado: {row[2]}, Fecha: {row[3]}\n"
        return respuesta
    except Exception as e:
        return f"Error al consultar la base de datos: {str(e)}"

# ==========================================
# HERRAMIENTA 2: GENERACIÓN DE DOCUMENTOS
# ==========================================
@tool
def generar_documento_consentimiento(nombre_titular: str, finalidad: str) -> str:
    """Genera un documento legal de consentimiento informado en formato HTML, basado en la Ley 21.719.
    
    Args:
        nombre_titular: Nombre completo de la persona que otorga el consentimiento.
        finalidad: El propósito para el cual se tratarán los datos.
    """
    try:
        # Leer la plantilla base
        ruta_plantilla = os.path.join("skills", "generar_consentimiento", "plantilla.html")
        with open(ruta_plantilla, "r", encoding="utf-8") as file:
            plantilla = file.read()
        
        # Reemplazar variables
        documento_final = plantilla.replace("{{nombre}}", nombre_titular).replace("{{finalidad}}", finalidad)
        return f"Documento generado con éxito. Aquí está el código HTML:\n\n{documento_final}"
    except Exception as e:
        return f"Error al generar el documento: {str(e)}"

# ==========================================
# HERRAMIENTA 3: EVALUACIÓN NORMATIVA (RAG Simulado)
# ==========================================
@tool
def buscar_en_regulaciones(consulta: str) -> str:
    """Busca información específica sobre la Ley 21.719 o la ISO 42001 en la base de conocimiento local.
    Úsala cuando necesites saber qué exige la ley o la norma sobre un tema particular (ej. 'plazos', 'consentimiento', 'seguridad').
    
    Args:
        consulta: El tema o palabra clave a buscar (ej. 'derechos del titular', 'plazos de respuesta').
    """
    # Para simplificar, simularemos una base de conocimiento RAG con un diccionario.
    # En un proyecto real, aquí conectarías a ChromaDB o FAISS.
    conocimiento = {
        "plazos": "Según la Ley 21.719, el responsable debe responder a las solicitudes ARCOP en un plazo máximo de 15 días hábiles.",
        "consentimiento": "La Ley 21.719 exige que el consentimiento sea libre, informado, específico e inequívoco. No puede ser tácito.",
        "iso 42001": "La ISO 42001 exige un sistema de gestión de IA (SGIA) que incluya evaluación de riesgos, transparencia y supervisión humana.",
        "seguridad": "Se deben implementar medidas técnicas y organizativas para garantizar la confidencialidad, integridad y disponibilidad de los datos."
    }
    
    consulta_lower = consulta.lower()
    resultados = [v for k, v in conocimiento.items() if k in consulta_lower]
    
    if resultados:
        return "Información encontrada:\n" + "\n".join(resultados)
    else:
        return "No se encontró información específica en la base de conocimiento local. Por favor, utiliza tus conocimientos generales sobre la Ley 21.719 e ISO 42001."

@tool
def listar_tratamientos() -> str:
    """Lista todas las actividades de tratamiento de datos registradas en la empresa,
    junto con su base legal, nivel de riesgo y estado de evaluación (ISO 42001).
    Úsala cuando el usuario pregunte por el inventario de tratamientos o el nivel de riesgo.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, finalidad, base_legal, nivel_riesgo, estado_evaluacion FROM tratamientos")
        resultados = cursor.fetchall()
        conn.close()
        
        if not resultados:
            return "No hay actividades de tratamiento registradas."
        
        respuesta = "Actividades de tratamiento registradas:\n"
        for row in resultados:
            respuesta += f"- [ID {row[0]}] {row[1]}\n"
            respuesta += f"  Finalidad: {row[2]}\n"
            respuesta += f"  Base legal: {row[3]}\n"
            respuesta += f"  Nivel de riesgo: {row[4]}\n"
            respuesta += f"  Estado evaluación: {row[5]}\n\n"
        return respuesta
    except Exception as e:
        return f"Error al listar tratamientos: {str(e)}"


# ==========================================
# HERRAMIENTA 5: OBTENER CRITERIOS DE EVALUACIÓN
# ==========================================
@tool
def obtener_criterios_evaluacion() -> str:
    """Devuelve el checklist oficial de criterios para evaluar documentos legales
    contra la Ley 21.719 y la ISO 42001.
    
    Úsala ÚNICAMENTE para cargar los criterios. Después de recibirlos, analiza tú
    mismo el documento del usuario aplicando cada ítem, y entrega el veredicto en
    tu respuesta final (no vuelvas a llamar herramientas para evaluar).
    
    No requiere parámetros.
    """
    try:
        ruta_skill = os.path.join("skills", "evaluar_documento", "skill.md")
        with open(ruta_skill, "r", encoding="utf-8") as f:
            criterios = f.read()
        return criterios
    except Exception as e:
        return f"Error al cargar los criterios de evaluación: {str(e)}"

# ==========================================
# HERRAMIENTA 6: GENERAR ACTA RoPA
# ==========================================
@tool
def generar_acta_ropa(
    nombre_tratamiento: str,
    categoria_datos: str,
    finalidad: str,
    tabla_origen: str,
    estado_solicitud: str
) -> str:
    """Genera un Acta de Registro de Actividades de Tratamiento (RoPA) conforme a la
    Ley 21.719 (art. 14) e ISO 42001 (cláusula 7.5). Registra la actividad en la
    base de datos y devuelve el acta en formato HTML.
    
    IMPORTANTE: Requiere los 5 parámetros. Si el usuario no los proporciona todos,
    NO llames a esta herramienta: pregúntale primero por los que faltan.
    
    Args:
        nombre_tratamiento: Nombre identificador del tratamiento (ej. "Marketing por email").
        categoria_datos: Tipos de datos tratados (ej. "identificación, contacto").
        finalidad: Propósito legítimo del tratamiento.
        tabla_origen: Tabla de la BD donde residen los datos (ej. "titulares").
        estado_solicitud: Estado del registro (Aprobado, En revisión, Rechazado).
    """
    try:
        # 1. Insertar en la base de datos
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO ropa_registros 
               (nombre_tratamiento, categoria_datos, finalidad, tabla_origen, estado_solicitud, observaciones)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (nombre_tratamiento, categoria_datos, finalidad, tabla_origen, estado_solicitud,
             "Registro generado por el agente de gobernanza.")
        )
        nuevo_id = cursor.lastrowid
        conn.commit()
        
        # 2. Recuperar la fecha de registro generada
        cursor.execute("SELECT fecha_registro FROM ropa_registros WHERE id = ?", (nuevo_id,))
        fecha_registro = cursor.fetchone()[0]
        conn.close()
        
        # 3. Leer la plantilla HTML
        ruta_plantilla = os.path.join("skills", "tramitacion_ropa", "plantilla.html")
        with open(ruta_plantilla, "r", encoding="utf-8") as f:
            plantilla = f.read()
        
        # 4. Reemplazar placeholders
        acta_html = (plantilla
            .replace("{{id}}", str(nuevo_id))
            .replace("{{fecha_registro}}", str(fecha_registro))
            .replace("{{nombre_tratamiento}}", nombre_tratamiento)
            .replace("{{categoria_datos}}", categoria_datos)
            .replace("{{finalidad}}", finalidad)
            .replace("{{tabla_origen}}", tabla_origen)
            .replace("{{estado_solicitud}}", estado_solicitud)
            .replace("{{observaciones}}", "Registro generado por el agente de gobernanza.")
        )
        
        return (
            f"✅ Acta RoPA registrada exitosamente con ID {nuevo_id}.\n\n"
            f"Aquí tienes el documento HTML:\n\n```html\n{acta_html}\n```"
        )
    except Exception as e:
        return f"Error al generar el acta RoPA: {str(e)}"


# ==========================================
# HERRAMIENTA 7: CONSULTAR REGISTROS RoPA
# ==========================================
@tool
def consultar_registros_ropa() -> str:
    """Lista todos los registros RoPA (Actas de Registro de Actividades de Tratamiento)
    almacenados en la base de datos, con su estado y fecha de registro.
    Úsala cuando el usuario pregunte por el registro RoPA, el inventario formal
    de tratamientos o las actas generadas.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nombre_tratamiento, categoria_datos, finalidad,
                   tabla_origen, estado_solicitud, fecha_registro
            FROM ropa_registros
            ORDER BY fecha_registro DESC
        """)
        resultados = cursor.fetchall()
        conn.close()
        
        if not resultados:
            return "No hay registros RoPA generados aún."
        
        respuesta = f"📋 Registros RoPA encontrados ({len(resultados)}):\n\n"
        for row in resultados:
            respuesta += (
                f"[ID {row[0]}] {row[1]}\n"
                f"  Categoría: {row[2]}\n"
                f"  Finalidad: {row[3]}\n"
                f"  Tabla origen: {row[4]}\n"
                f"  Estado: {row[5]}\n"
                f"  Fecha: {row[6]}\n\n"
            )
        return respuesta
    except Exception as e:
        return f"Error al consultar los registros RoPA: {str(e)}"

# Lista de herramientas para exportar al agente
herramientas_agente = [
    registrar_solicitud_arcop,
    consultar_solicitudes_arcop,
    generar_documento_consentimiento,
    buscar_en_regulaciones,
    listar_tratamientos,
    obtener_criterios_evaluacion,
    generar_acta_ropa,          
    consultar_registros_ropa,   
]