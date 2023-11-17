import os

# Caminho para o executável do Python
python_executable = "python" if os.name == 'nt' else "python3"

# Criação do ambiente virtual
os.system(f"{python_executable} -m venv venv")

# Ativação do ambiente virtual (verifique o sistema operacional)
if os.name == 'nt':
    os.system("venv\\Scripts\\activate")
else:
    os.system("source venv/bin/activate")

# Instalar os pacotes
os.system(f"{python_executable} -m pip install requests")
os.system(f"{python_executable} -m pip install datetime")
os.system(f"{python_executable} -m pip install python-dotenv")
os.system(f"{python_executable} -m pip install openai")
os.system(f"{python_executable} -m pip install reportlab")
os.system(f"{python_executable} -m pip install pypdf")