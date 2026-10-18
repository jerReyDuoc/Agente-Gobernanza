import sqlite3
import os

DB_PATH = "empresa_gobernanza.db"

def crear_base_datos():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # ============================================
    # TABLA 1: TITULARES (Personas cuyos datos tratamos)
    # ============================================
    cursor.execute('''
    CREATE TABLE titulares (
        id INTEGER PRIMARY KEY,
        nombre TEXT,
        email TEXT,
        ciudad TEXT,
        consentimiento_otorgado BOOLEAN,
        fecha_alta DATE DEFAULT CURRENT_DATE
    )
    ''')

    # ============================================
    # TABLA 2: TRATAMIENTOS (Actividades de tratamiento - ISO 42001)
    # ============================================
    cursor.execute('''
    CREATE TABLE tratamientos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        finalidad TEXT,
        base_legal TEXT,
        categoria_datos TEXT,
        nivel_riesgo TEXT,
        estado_evaluacion TEXT
    )
    ''')

    # ============================================
    # TABLA 3: SOLICITUDES ARCOP
    # ============================================
    cursor.execute('''
    CREATE TABLE solicitudes_arcop (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titular_id INTEGER,
        tipo_derecho TEXT,
        estado TEXT,
        fecha_solicitud DATE DEFAULT CURRENT_DATE,
        fecha_resolucion DATE,
        observaciones TEXT,
        FOREIGN KEY(titular_id) REFERENCES titulares(id)
    )
    ''')


    # ============================================
    # TABLA 4: REGISTRO RoPA (Record of Processing Activities)
    # ============================================
    cursor.execute('''
    CREATE TABLE ropa_registros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_tratamiento TEXT NOT NULL,
        categoria_datos TEXT NOT NULL,
        finalidad TEXT NOT NULL,
        tabla_origen TEXT NOT NULL,
        estado_solicitud TEXT NOT NULL,
        fecha_registro DATE DEFAULT CURRENT_DATE,
        observaciones TEXT
    )
    ''')

    # ============================================
    # DATOS DE EJEMPLO
    # ============================================
    
    # Titulares (personas)
    titulares = [
        ("Juan Pérez",   "juan.perez@email.com",    "Santiago",   True),
        ("María López",  "maria.lopez@email.com",   "Valparaíso", False),
        ("Ana Gómez",    "ana.gomez@email.com",     "Concepción", True),
        ("Carlos Rojas", "carlos.rojas@email.com",  "Santiago",   True),
        ("Sofía Martínez","sofia.martinez@email.com","La Serena", False),
        ("Diego Silva",  "diego.silva@email.com",   "Antofagasta",True),
        ("Valentina Torres","valen.torres@email.com","Santiago", True),
    ]
    cursor.executemany(
        "INSERT INTO titulares (nombre, email, ciudad, consentimiento_otorgado) VALUES (?, ?, ?, ?)",
        titulares
    )

    # Tratamientos (actividades de tratamiento)
    tratamientos = [
        ("Marketing por email", 
         "Envío de newsletters y promociones comerciales",
         "Consentimiento", "Identificación, contacto", "Medio", "Aprobado"),
        ("Análisis de comportamiento de clientes",
         "Segmentación para personalización de ofertas",
         "Interés legítimo", "Datos de uso, preferencias", "Alto", "Pendiente"),
        ("Gestión de Recursos Humanos",
         "Administración de contratos y nóminas de empleados",
         "Obligación legal", "Datos laborales, financieros", "Alto", "Aprobado"),
        ("Videovigilancia de instalaciones",
         "Seguridad de oficinas y control de acceso",
         "Interés legítimo", "Imagen, datos biométricos", "Alto", "En revisión"),
        ("Atención al cliente (call center)",
         "Gestión de consultas y reclamos",
         "Consentimiento", "Identificación, grabaciones de voz", "Medio", "Aprobado"),
    ]
    cursor.executemany(
        "INSERT INTO tratamientos (nombre, finalidad, base_legal, categoria_datos, nivel_riesgo, estado_evaluacion) VALUES (?, ?, ?, ?, ?, ?)",
        tratamientos
    )

    # Solicitudes ARCOP históricas
    solicitudes = [
        (1, "Acceso",       "Resuelta",  "2025-03-15", "2025-03-20", "Se entregó reporte completo al titular."),
        (2, "Cancelación",  "Pendiente", "2025-04-10", None,         "En proceso de verificación de identidad."),
        (3, "Rectificación","Resuelta",  "2025-04-05", "2025-04-08", "Se corrigió el email del titular."),
        (1, "Oposición",    "Pendiente", "2025-04-18", None,         "Revisando base legal del tratamiento."),
        (4, "Portabilidad", "Resuelta",  "2025-02-10", "2025-02-18", "Datos exportados en formato JSON."),
        (6, "Acceso",       "Pendiente", "2025-04-22", None,         "Solicitud recibida, en cola."),
    ]
    cursor.executemany(
        "INSERT INTO solicitudes_arcop (titular_id, tipo_derecho, estado, fecha_solicitud, fecha_resolucion, observaciones) VALUES (?, ?, ?, ?, ?, ?)",
        solicitudes
    )

    # Registros RoPA de ejemplo (actas formales)
    ropa = [
        ("Marketing por email",
         "Identificación, contacto",
         "Envío de newsletters y promociones comerciales",
         "titulares",
         "Aprobado",
         "Registro formal conforme al art. 14 de la Ley 21.719."),
        ("Análisis de comportamiento",
         "Datos de uso, preferencias",
         "Segmentación para personalización de ofertas",
         "titulares",
         "En revisión",
         "Pendiente evaluación de impacto (EIPD) por uso de IA."),
    ]
    cursor.executemany(
        "INSERT INTO ropa_registros (nombre_tratamiento, categoria_datos, finalidad, tabla_origen, estado_solicitud, observaciones) VALUES (?, ?, ?, ?, ?, ?)",
        ropa
    )
    conn.commit()
    conn.close()
    
    print("✅ Base de datos creada y poblada con éxito.")
    print(f"   - {len(titulares)} titulares")
    print(f"   - {len(tratamientos)} actividades de tratamiento")
    print(f"   - {len(solicitudes)} solicitudes ARCOP")
    print(f"   - {len(ropa)} registros RoPA")

if __name__ == "__main__":
    crear_base_datos()