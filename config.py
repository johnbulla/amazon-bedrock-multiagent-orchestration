
"""
Configuración de la app.
"""

# Región del servicio Bedrock
REGION = "us-east-1"

# Identificadores del Agente Orquestador
AGENT_ID = "AGENT_ID"       # <-- Cambia por tu AgentId
AGENT_ALIAS_ID = "AGENT_ALIAS_ID"  # <-- Cambia por tu AgentAliasId

# Si quieres forzar un perfil local (~/.aws/credentials), pon el nombre aquí.
# Si prefieres la credential chain por defecto, deja AWS_PROFILE = None o USE_DEFAULT_AWS_CHAIN = True.
AWS_PROFILE = None  # por ejemplo: "default" o "my-sso-profile"

AWS_ACCESS_KEY_ID = "AWS_ACCESS_KEY_ID" # <-- Agrega tu AWS Access Key ID
AWS_SECRET_ACCESS_KEY = "AWS_SECRET_ACCESS_KEY" # <-- Agrega tu AWS Access Key ID

# Usa la credential chain por defecto de boto3 (env, shared config, IAM role), ignorando AWS_PROFILE
USE_DEFAULT_AWS_CHAIN = True
