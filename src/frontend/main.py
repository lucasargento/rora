import os
import sys
import importlib
from pathlib import Path
import streamlit as st

# Ensure project root in sys.path so `src.*` imports work when launched from different CWDs
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


st.set_page_config(page_title="R.O.R.A Frontend", layout="wide")

# --- Sidebar: API Key and Model Selection
with st.sidebar:
    st.header("Configuración")
    api_key_input = st.text_input(
        "OpenAI API Key",
        type="password",
        placeholder="sk-...",
        help="Se usará para inicializar el agente",
    )
    model_name = st.text_input(
        "Modelo",
        value="o3-mini-2025-01-31",
        help="Nombre del modelo a usar por el agente",
    )
    if st.button("Guardar credenciales"):
        if not api_key_input:
            st.warning("Ingresá una API Key válida")
        else:
            os.environ["OPENAI_API_KEY"] = api_key_input
            # Invalidate existing agent to recreate with new key
            st.session_state.agent = None
            st.success("API Key guardada en variable de entorno OPENAI_API_KEY")


# --- Main: Chat UI and Agent Execution
st.title("R.O.R.A: Reasoning Operations Research Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:
    st.session_state.agent = None

if "running" not in st.session_state:
    st.session_state.running = False

def ensure_agent():
    if st.session_state.agent is None:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            st.error("Configurá la OpenAI API Key en la barra lateral.")
            return None
        try:
            # Lazy import here to avoid importing modules that require API key before set
            try:
                from src.agent.agent import build_agent
            except ModuleNotFoundError:
                from agent.agent import build_agent
            st.session_state.agent = build_agent(api_key=api_key, model=model_name)
        except Exception as e:
            st.error(f"Error creando el agente: {e}")
            return None
    return st.session_state.agent


submitted = False
if not st.session_state.running:
    with st.form("problem_form"):
        problem_name = st.text_input("Nombre del problema", value="demo_problem")
        problem_statement = st.text_area(
            "Descripción del problema",
            height=160,
            placeholder="Ej: Minimizar 3x + 2y sujeto a x + y >= 10, x >= 0, y >= 0",
        )
        expected_output = st.text_area(
            "Salida esperada (opcional)",
            height=120,
            placeholder="Ej: x = 0, y = 10; objetivo = 20",
        )
        submitted = st.form_submit_button("Ejecutar agente")
else:
    st.info("RORA is thinking…")

if submitted:
    st.session_state.running = True
    agent = ensure_agent()
    if agent is not None:
        # Reset conversation to show only the latest run
        st.session_state.messages = []
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": problem_statement.strip(),
        })

        # Initial state for the agent
        initial_state = {
            "problem_statement": problem_statement.strip(),
            "problem_name": problem_name.strip() or "demo_problem",
            "expected_output": expected_output.strip(),
            "coherent": True,
            "execution_error": False,
        }

        # Execute agent (non-streaming invocation). We'll display key state fields as messages.
        try:
            with st.spinner("RORA is thinking…"):
                final_state = agent.invoke(initial_state)

            # Collect intermediate results if present and append to messages
            for key in [
                ("math_result", "📐 Formulación matemática"),
                ("code_result", "💻 Implementación (código)"),
                ("validation_result", "🔍 Validación de código"),
                ("execution_result", "🚀 Ejecución"),
                ("reflection_status", "🪞 Reflexión"),
            ]:
                field, title = key
                value = final_state.get(field)
                if value:
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"{title}:\n\n{value}",
                    })

        except Exception as e:
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"❌ Error ejecutando el agente: {e}",
            })
        finally:
            st.session_state.running = False


# --- Render conversation
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(message["content"]) 


