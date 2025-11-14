Amazon Bedrock — Orquestación Multi-Agente (Demo)

Demo para probar la orquestación multi-agente sobre Amazon Bedrock usando agentes especializados y un orquestador. Incluye prompts y bases de conocimiento de ejemplo en español, junto con un starter en Python para ejecutarlo localmente.

🚀 Características

- Orquestación entre un agente coordinador y agentes especializados (p. ej. dominios funcionales).
- Prompts y bases de conocimiento de ejemplo (carpetas Prompts/Spanish y Knowledge Bases/Spanish).
- App mínima en Python (app.py) y configuración centralizada (config.py). citeturn0view0
- Dependencias declaradas en requirements.txt. citeturn0view0

🧭 Flujo funcional (alto nivel)

- Usuario → envía consulta.
- Orquestador → analiza intención y delega.
- Agentes especializados → consultan su conocimiento y responden.
- Orquestador → compone y devuelve la respuesta final.

📁 Estructura del repositorio
.
├─ app.py                    # App mínima para interactuar con el orquestador
├─ config.py                 # Variables/IDs y parámetros de configuración
├─ requirements.txt          # Dependencias de Python
├─ Prompts/
│   └─ Spanish/              # Prompts de ejemplo (ES)
└─ Knowledge Bases/
    └─ Spanish/              # Contenido de ejemplo para RAG (ES)


✅ Requisitos previos

- Cuenta de AWS con acceso a Amazon Bedrock en la región elegida.
- Python 3.12
- Credenciales AWS configuradas localmente (aws configure) con permisos para:
  - bedrock:* (o al menos bedrock:InvokeModel, bedrock:InvokeAgent, bedrock:Retrieve, etc.)
  - Acceso al almacén vectorial si usas Knowledge Bases (p. ej. OpenSearch Serverless / Aurora / S3 según tu setup).
  - (Opcional) Agents for Bedrock creados y Knowledge Bases asociadas.

🔧 Instalación
# 1) Clonar
git clone https://github.com/johnbulla/amazon-bedrock-multiagent-orchestration
cd amazon-bedrock-multiagent-orchestration

# 2) Crear entorno
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3) Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

🔐 Variables de entorno / Configuración

Define en tu entorno (o ajusta config.py) los IDs / ARNs necesarios:

export AWS_REGION=us-east-1
export BEDROCK_AGENT_ID=AGENT_ID_ORQUESTADOR
export BEDROCK_AGENT_ALIAS_ID=ALIAS_ID

En config.py puedes centralizar:

Región/endpoint de Bedrock
IDs/aliases de los agentes

▶️ Ejecución
streamlit run app.pypython app.py


🧩 Personalización

- Prompts: edita los archivos de Prompts/Spanish para el orquestador y cada agente.
- Conocimiento: añade/actualiza documentos en Knowledge Bases/Spanish y reindexa en tu KB de Bedrock.

🔒 IAM (ejemplo mínimo orientativo)

Ajusta a tu realidad de seguridad (principio de menor privilegio).

{
  "Version": "2012-10-17",
  "Statement": [
    { "Effect": "Allow", "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeAgent",
        "bedrock:Retrieve",
        "bedrock:RetrieveAndGenerate"
      ], "Resource": "*" },
    { "Effect": "Allow", "Action": [
        "bedrock:StartAgentSession",
        "bedrock:InvokeFlow"
      ], "Resource": "*" }
  ]
}


📄 Licencia

Este proyecto se publica tal cual con fines de demostración; añade aquí la licencia que prefieras (MIT/Apache-2.0, etc.).
