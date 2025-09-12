import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from pathlib import Path

# Carregar variáveis de ambiente
env_path = r"C:\Users\Felip\Code\estudo\Machine_Learning_IA\bootcamp-dio\Projetos_BOOTCAMP_DIo\projeto9-checador-seguranca\src\.env"
load_dotenv(env_path)

# Configurar cliente
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("AZURE_OPENAI_VERSION")
)

# Testar conexão
try:
    deployments = client.models.list()
    print("Conexão bem-sucedida! Modelos disponíveis:")
    for deployment in deployments:
        print(f"- {deployment.id}")
except Exception as e:
    print(f"Erro na conexão: {e}")