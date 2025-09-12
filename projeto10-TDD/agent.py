import os
from langchain.llms import AzureOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv()

# Configuração do Azure OpenAI
llm = AzureOpenAI(
    deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    model_name="gpt-35-turbo-instruct",
    temperature=0.3,
)

template = """
Você é um assistente de IA especializado em escrever testes unitários em Python usando pytest.
Dado o seguinte código Python, gere testes unitários para ele.

Código:
{code}

Instruções:
- Escreva testes unitários usando pytest.
- Inclua testes para casos de sucesso e de falha, quando aplicável.
- Retorne apenas o código Python do teste, sem nenhum texto adicional.
- O arquivo de teste deve começar com 'import pytest'.
- Cada função de teste deve começar com 'def test_...'.

Testes:
"""

prompt = PromptTemplate(template=template, input_variables=["code"])

chain = LLMChain(llm=llm, prompt=prompt)

def generate_tests(code):
    """
    Gera testes unitários para o código Python fornecido
    """
    response = chain.run(code=code)
    return response

def save_tests(code, filename):
    """
    Salva os testes em um arquivo
    """
    # Extrai o nome da função do arquivo original
    base_name = os.path.basename(filename).replace('.py', '')
    test_filename = f"test_{base_name}.py"
    
    with open(test_filename, 'w') as f:
        f.write(code)
    
    return test_filenames