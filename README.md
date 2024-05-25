# Instalação e Configuração do Ambiente Virtual (venv)

## Pré-requisitos
- Python 3.6 ou superior (preferencialmente 3.10)
- pip (gerenciador de pacotes do Python)

### Instruções para Ubuntu 20.04

1. **Instalar o Python 3 e pip (se ainda não estiverem instalados):**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip

2. **Instalar o módulo venv (se ainda não estiver instalado):**

    ```bash
    sudo apt install python3-venv

3. **Criar o ambiente virtual:**
Navegue até o diretório do seu projeto e execute:

    ```bash
    python3 -m venv venv

4. **Ativar o ambiente virtual:**

    ```bash
    source venv/bin/activate

5. **Instalar as dependências a partir do requirements.txt:** Certifique-se de que o arquivo requirements.txt está no diretório do projeto e execute:

    ```bash
    pip install -r requirements.txt

6. **Desativar o ambiente virtual (quando necessário):**

    ```bash
    deactivate

7. **Instalar o env do agente DRL:**

    ```bash
    pip install -e coinbot-env

### Instruções para Windows 11

**Prefira utilizar o PyCharm, que deve controlar todos os passos abaixo**

1. **Instalar o Python 3 e pip (se ainda não estiverem instalados):**
        Baixe e instale o Python 3 a partir do site oficial: Python.org.
        Durante a instalação, marque a opção "Add Python to PATH".

2. **Criar o ambiente virtual:**
    Navegue até o diretório do seu projeto e execute:

    ```bash
    python -m venv venv

3. **Ativar o ambiente virtual:**

    ```cmd
    .\venv\Scripts\activate

4. **Instalar as dependências a partir do requirements.txt:**
Certifique-se de que o arquivo requirements.txt está no diretório do projeto e execute:

    ```cmd
    pip install -r requirements.txt

5. **Desativar o ambiente virtual (quando necessário):**

    ```cmd
    deactivate

6. **Instalar o env do agente DRL:**

    ```bash
    pip install -e coinbot-env