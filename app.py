import streamlit as st
import streamlit.components.v1 as components
from agent_app.agent import agente_app
import uuid

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(page_title="Agente de Gobernanza IA", page_icon="🛡️", layout="wide")

st.title("🛡️ Agente de Gobernanza de Datos e IA")
st.markdown("""
Este agente está diseñado para asistir en el cumplimiento de la **Ley 21.719** de Protección de Datos Personales y la norma **ISO 42001**.
Puedes pedirle que:
- Genere documentos de consentimiento.
- Consulte o registre derechos ARCOP.
- Evalúe documentos legales.
""")

# ==========================================
# 2. GESTIÓN DE LA MEMORIA (Sesión)
# ==========================================
# Generamos un ID de hilo único para la sesión (Memoria a corto plazo)
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

# Guardamos el historial de mensajes visuales
if "messages" not in st.session_state:
    st.session_state.messages = []

# Configuración para LangGraph
config = {"configurable": {"thread_id": st.session_state.thread_id}}

# ==========================================
# 3. MOSTRAR HISTORIAL DE CHAT
# ==========================================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["type"] == "html":
            # Si es un documento HTML, lo renderizamos de forma bonita
            components.html(message["content"], height=400, scrolling=True)
        else:
            st.markdown(message["content"])

# ==========================================
# 4. ENTRADA DEL USUARIO Y RESPUESTA
# ==========================================
if prompt := st.chat_input("Ej: Genera un consentimiento para Juan Perez para fines de marketing..."):
    
    # Mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt, "type": "text"})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Mostrar respuesta del agente
    with st.chat_message("assistant"):
        with st.spinner("El agente está razonando y usando herramientas..."):
            # Invocar al agente de LangGraph
            respuesta = agente_app.invoke(
                {"messages": [("user", prompt)]},
                config=config
            )
            
            # Obtener el último mensaje (la respuesta final del agente)
            mensaje_final = respuesta["messages"][-1].content
            
            # Verificar si la respuesta contiene código HTML (para el consentimiento)
            if "```html" in mensaje_final:
                # Extraer solo el HTML
                html_puro = mensaje_final.split("```html")[1].split("```")[0].strip()
                
                # Mostrar explicación en texto
                explicacion = mensaje_final.split("```html")[0]
                st.markdown(explicacion)
                
                # Renderizar el HTML
                st.success("Documento generado exitosamente:")
                components.html(html_puro, height=400, scrolling=True)
                
                # Guardar en el estado para que persista
                st.session_state.messages.append({"role": "assistant", "content": explicacion, "type": "text"})
                st.session_state.messages.append({"role": "assistant", "content": html_puro, "type": "html"})
            else:
                # Si es texto normal, solo mostrarlo
                st.markdown(mensaje_final)
                st.session_state.messages.append({"role": "assistant", "content": mensaje_final, "type": "text"})