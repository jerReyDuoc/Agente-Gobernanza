from agent_app.agent import agente_app

# Configurar un ID de sesión para la memoria
config = {"configurable": {"thread_id": "sesion_prueba_1"}}

# Simular una conversación
print("--- PRUEBA 1: Consultar estado ARCOP ---")
respuesta = agente_app.invoke(
    {"messages": [("user", "Hola, ¿puedes revisar si el titular 1 tiene solicitudes ARCOP pendientes?")]},
    config=config
)
print(respuesta["messages"][-1].content)

print("\n--- PRUEBA 2: Generar documento ---")
respuesta = agente_app.invoke(
    {"messages": [("user", "Genera un consentimiento para Ana Gomez para fines de marketing")]},
    config=config
)
print(respuesta["messages"][-1].content)