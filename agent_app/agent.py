import os
from typing import Annotated, TypedDict
from dotenv import load_dotenv

# Importaciones de LangGraph y LangChain
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import SystemMessage

# --- CAMBIO IMPORTANTE: Usamos Groq ---
from langchain_groq import ChatGroq

# Importar nuestras herramientas y prompts locales
from agent_app.tools import herramientas_agente
from agent_app.prompts import SUPERVISOR_SYSTEM_PROMPT

# Cargar variables de entorno (API KEY)
load_dotenv()

# ==========================================
# 1. DEFINIR EL ESTADO DEL GRAFO (Memoria)
# ==========================================
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# ==========================================
# 2. CONFIGURAR EL MODELO Y HERRAMIENTAS
# ==========================================
# --- CAMBIO IMPORTANTE: Inicializamos ChatGroq ---
llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)

# Le "enseñamos" las herramientas al modelo
llm_con_herramientas = llm.bind_tools(herramientas_agente)

# ==========================================
# 3. DEFINIR LOS NODOS (Sin cambios)
# ==========================================
def nodo_agente(state: AgentState):
    """Nodo principal: El LLM razona y decide qué hacer."""
    messages = [SystemMessage(content=SUPERVISOR_SYSTEM_PROMPT)] + state["messages"]
    respuesta = llm_con_herramientas.invoke(messages)
    return {"messages": [respuesta]}

nodo_herramientas = ToolNode(herramientas_agente)

# ==========================================
# 4. FUNCIÓN DE ENRUTAMIENTO (Sin cambios)
# ==========================================
def ruta_condicional(state: AgentState):
    """Decide si el agente usa una herramienta o responde al usuario."""
    ultimo_mensaje = state["messages"][-1]
    
    if ultimo_mensaje.tool_calls:
        return "herramientas"
    else:
        return END

# ==========================================
# 5. CONSTRUIR EL GRAFO (Sin cambios)
# ==========================================
workflow = StateGraph(AgentState)
workflow.add_node("agente", nodo_agente)
workflow.add_node("herramientas", nodo_herramientas)

workflow.set_entry_point("agente")
workflow.add_conditional_edges(
    "agente",
    ruta_condicional,
    {
        "herramientas": "herramientas",
        END: END
    }
)
workflow.add_edge("herramientas", "agente")

# ==========================================
# 6. COMPILAR CON MEMORIA (Sin cambios)
# ==========================================
memoria = MemorySaver()
agente_app = workflow.compile(checkpointer=memoria)