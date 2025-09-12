# Analisador de Ameaças de Segurança

<br>

## Detalhes do projeto
#### neste projeto de fim de curso, fizemos um verificador de vulnerabilidades de aplicações web, de forma que identificasse falhas e retronasse ao usuario 

<br><br>


Este projeto é uma ferramenta de análise de ameaças de segurança que utiliza a API da Azure OpenAI para gerar modelos de ameaças baseados na metodologia STRIDE.

## Funcionalidades

- Upload de imagem da arquitetura do sistema
- Análise de ameaças de segurança utilizando IA
- Geração de relatórios em JSON com possíveis ameaças e sugestões de melhorias
- Interface web intuitiva para interação com o sistema

## Tecnologias Utilizadas

### Backend
- Python 3.x
- FastAPI
- Azure OpenAI API
- Uvicorn (servidor ASGI)
- python-dotenv

### Frontend
- HTML5
- CSS3
- JavaScript (Vanilla)

## Como Executar

### Pré-requisitos

- Python 3.8 ou superior
- Conta na Azure com acesso ao serviço OpenAI
- Chave de API e endpoint da Azure OpenAI

### Configuração do Ambiente

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd projeto9-checador-seguranca