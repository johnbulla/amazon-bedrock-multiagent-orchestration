import streamlit as st
import boto3
import uuid
from botocore.exceptions import ClientError
from config import (
    REGION,
    AGENT_ID,
    AGENT_ALIAS_ID,
    AWS_PROFILE,
    USE_DEFAULT_AWS_CHAIN,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY
)

st.set_page_config(page_title="Multi-agents Amazon Bedrock", page_icon="🤖", layout="centered")

# ---------- Helpers ----------
def get_bedrock_client():
    """
    Crea y devuelve el cliente de Bedrock Agent Runtime.
    Prioridad:
      1) Perfil (AWS_PROFILE)
      2) Accesos explícitos (AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY)
      3) Cadena de credenciales por defecto
    """
    if AWS_PROFILE:
        # Usa un perfil de ~/.aws/credentials y ~/.aws/config
        session = boto3.Session(profile_name=AWS_PROFILE, region_name=REGION)
        client = session.client("bedrock-agent-runtime")
    elif AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
        client = boto3.client(
            "bedrock-agent-runtime",
            region_name=REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
    else:
        # Usa la default credential chain (variables de entorno, IAM role, etc.)
        client = boto3.client("bedrock-agent-runtime", region_name=REGION)

    return client  # <— ¡imprescindible!
def invoke_agent(client, agent_id, alias_id, prompt, session_id):
    response = client.invoke_agent(
        agentId=agent_id,
        agentAliasId=alias_id,
        enableTrace=True,
        sessionId=session_id,
        inputText=prompt,
    )

    completion_text = ""
    for event in response.get("completion", []):
        if "chunk" in event:
            chunk = event["chunk"]
            completion_text += chunk["bytes"].decode()
            yield completion_text
        elif "trace" in event:
            pass

    # Si no llegó nada, emite un placeholder
    if not completion_text:
        yield "(Sin respuesta del agente)"

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Hola! Soy tu agente en Bedrock. ¿En qué puedo ayudarte hoy?"}
    ]

st.title("🤖 Sistema Multiagente con Amazon Bedrock")
st.caption("🚀 AWS Commuity Day España 2025")

# Sidebar config
with st.sidebar:
    st.header("⚙️ Configuración")
    st.text_input("Región", value=REGION, disabled=True)
    st.text_input("Agent ID", value=AGENT_ID, disabled=True, type="password")
    st.text_input("Alias ID", value=AGENT_ALIAS_ID, disabled=True, type="password")
    st.text_input("Session ID", value=st.session_state.session_id, disabled=True)
    st.divider()
    st.markdown(
       "@John Bulla"
   )

# Render mensajes previos
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
         st.markdown(msg["content"])

# Input del usuario
if prompt := st.chat_input("Escribe tu pregunta acerca de las políticas corporativas..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        accumulated = ""
        try:
            client = get_bedrock_client()
            for partial in invoke_agent(
                client,
                AGENT_ID,
                AGENT_ALIAS_ID,
                prompt,
                st.session_state.session_id,
           ):
                accumulated = partial
                placeholder.markdown(accumulated)
        except ClientError as e:
            accumulated = f"Error del cliente: {str(e)}"
            placeholder.error(accumulated)
        except Exception as e:
            accumulated = f"Ocurrió un error: {str(e)}"
            placeholder.error(accumulated)

# Guardar respuesta final
    st.session_state.messages.append(
        {"role": "assistant", "content": accumulated or "(sin contenido)"}
    )

# Pie de página
st.markdown("---")
st.caption("Demo · Amazon Bedrock Multi Agent")